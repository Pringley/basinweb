from django.db import models
from django.utils.timezone import now

class Label(models.Model):
    """A task label, such as 'school' or 'work'."""
    name = models.CharField(max_length=50)
    trashed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Assignee(models.Model):
    """Someone to whom you can delegate tasks."""
    name = models.CharField(max_length=100)

    last_request = models.DateTimeField(null=True, blank=True,
            help_text='Last time you asked this person for something.')
    last_response = models.DateTimeField(null=True, blank=True,
            help_text='Last time this person responded to you.')

    trashed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

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
                .exclude(assignee__isnull=False)
                # exclude blocked
                .exclude(blockers__completed=False))

    def sleeping(self):
        """Return all incomplete but sleeping tasks."""
        incomplete = self.incomplete()
        return (incomplete.filter(sleepforever=True) |
                incomplete.filter(sleepuntil__gte=now()))

    def blocked(self):
        """Return all incomplete but blocked tasks."""
        return self.incomplete().filter(blockers__completed=False)

    def delegated(self):
        """Return all incomplete but delegated tasks."""
        return self.incomplete().filter(assignee__isnull=False)

    def completed(self):
        """Return all valid, complete tasks."""
        return self.filter(completed=True, trashed=False)

    def trashed(self):
        """Return all tasks in the trash."""
        return self.filter(trashed=True)

    def order_by_due(self):
        """Order by due date, with non-due items last."""
        return self.annotate(not_due=models.Count('due')).order_by('-not_due', 'due')

class Task(models.Model):
    """A todo item, such as 'take out trash'."""
    objects = TaskQuerySet.as_manager()

    summary = models.CharField(max_length=144, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    due = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    labels = models.ManyToManyField(Label, related_name='tasks', blank=True)

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

    # Delegated tasks have a non-null "assignee" reference.
    assignee = models.ForeignKey(Assignee, null=True, blank=True,
            related_name='tasks',
            help_text="Delegate tasks by specifying an assignee.")

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
        return self.assignee is not None
    is_delegated.boolean = True
    is_delegated.short_description = 'Delegated?'

    def __str__(self):
        return self.summary
