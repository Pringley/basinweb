from django.db import models
from django.utils.timezone import now
from django.core.validators import RegexValidator

class TaskQuerySet(models.QuerySet):
    """Custom Manager for Task objects."""

    def valid(self):
        """Return all tasks that haven't been deleted."""
        return self.filter(trashed=False)

    def incomplete(self):
        """Return all valid, incomplete tasks (aka the TODOs)."""
        return self.filter(completed=False, trashed=False)

    def active(self):
        """Return all incomplete tasks that aren't sleeping, blocked, etc."""
        return (self.incomplete()
                # exclude sleeping
                .exclude(sleepforever=True)
                .exclude(sleepuntil__gte=now())
                # exclude delegated
                .filter(delegatedto__exact='')
                # exclude blocked
                .exclude(blockers__completed=False)
                .order_by_due())

    def sleeping(self):
        """Return all incomplete but sleeping tasks."""
        incomplete = self.incomplete()
        return (incomplete.filter(sleepforever=True) |
                incomplete.filter(sleepuntil__gte=now())).order_by_wakeup()

    def blocked(self):
        """Return all incomplete but blocked tasks."""
        return self.incomplete().filter(blockers__completed=False)

    def delegated(self):
        """Return all incomplete but delegated tasks."""
        return self.incomplete().exclude(delegatedto__exact='')

    def completed(self):
        """Return all valid, complete tasks."""
        return self.filter(completed=True, trashed=False)

    def trashed(self):
        """Return all tasks in the trash."""
        return self.filter(trashed=True)

    def state(self, state):
        """Filter by a given state."""
        if state == 'active':
            return self.active()
        elif state == 'sleeping':
            return self.sleeping()
        elif state == 'blocked':
            return self.blocked()
        elif state == 'delegated':
            return self.delegated()
        elif state == 'completed':
            return self.completed()
        elif state == 'trashed':
            return self.trashed()
        else:
            return self.none()

    def order_by_wakeup(self):
        """Order by sleep wakeup date."""
        return self.annotate(not_sleepuntil=models.Count('sleepuntil')).order_by('sleepforever',
            '-not_sleepuntil', 'sleepuntil')

    def order_by_due(self):
        """Order by due date, with non-due items last."""
        return self.annotate(not_due=models.Count('due')).order_by('-not_due', 'due')

class Task(models.Model):
    """A todo item, such as 'take out trash'."""
    objects = TaskQuerySet.as_manager()

    summary = models.CharField(max_length=144, blank=True)
    details = models.TextField(blank=True)
    due = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    # Labels are stored (denormalized) in a single text field, separated by
    # commas.
    labels = models.TextField(blank=True,
        help_text="Comma-separated labels",
        validators=[
        RegexValidator('^\s*([A-Za-z0-9_\-]+)(\s*,\s*[A-Za-z0-9_\-]+)*(\s*,\s*)?$',
            code='not-alnum-csv',
            message='labels must be alphanumeric, comma-separated')
    ])

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # Allow tasks to be marked as high-level projects.
    project = models.BooleanField(default=False,
            help_text="Set to True if this is a high-level project "
                      "(as opposed to a granular action).")

    # Instead of deleting tasks, simply mark them as "trashed".
    trashed = models.BooleanField(default=False,
            help_text="Instead of deleting tasks, simply mark them "
                      "as 'trashed' here.") 

    # Deferred tasks are "sleeping". The "sleepuntil" field tells the task when
    # to wake back up. To defer a task indefinitely, set sleepforever=True.
    sleepuntil = models.DateTimeField("sleep until", null=True, blank=True,
            help_text="Put this task to sleep until specified time.")
    sleepforever = models.BooleanField("sleep indefinitely", default=False,
            help_text="Put this task to sleep indefinitely.")

    # Tasks can be "blocked" on other tasks. Blocked tasks have a non-empty set
    # of "blockers".
    blockers = models.ManyToManyField('self', related_name='blocking',
            symmetrical=False, blank=True,
            help_text="Select any other tasks preventing this from completion.")

    # Delegated tasks have a non-empty "delegatedto" field.
    delegatedto = models.CharField(max_length=128, blank=True,
            help_text="Delegate tasks by specifying an delegatedto.")

    def is_active(self):
        """Check if the task is active (non-sleeping, etc)."""
        return not (self.completed or self.trashed or self.is_delegated()
                or self.is_sleeping() or self.is_blocked())
    is_active.boolean = True
    is_active.short_description = 'Active?'

    def is_sleeping(self):
        """Check if the task is sleeping/deferred."""
        return self.sleepforever or (self.sleepuntil is not None
                and now() < self.sleepuntil)
    is_sleeping.boolean = True
    is_sleeping.short_description = 'Sleeping?'

    def is_blocked(self):
        """Check if the task is blocked/waiting."""
        return bool(self.blockers.filter(completed=False))
    is_blocked.boolean = True
    is_blocked.short_description = 'Blocked?'

    def is_delegated(self):
        """Check if the task is assigned to someone else."""
        return bool(self.delegatedto)
    is_delegated.boolean = True
    is_delegated.short_description = 'Delegated?'

    def __str__(self):
        return self.summary
