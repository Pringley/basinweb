from django.contrib import admin
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as ugt
from tasks.models import Task, Label, Assignee

class LabelFilter(admin.SimpleListFilter):
    """Filter by task label."""
    title = ugt('label')
    parameter_name = 'label'

    def lookups(self, request, model_admin):
        return [(label.name, label.name) for label in
                Label.objects.filter(trashed=False)]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return queryset.filter(labels__name=self.value())

class StateFilter(admin.SimpleListFilter):
    """Filter by task state."""
    title = ugt('task state')
    parameter_name = 'state'

    def lookups(self, request, model_admin):
        return (
            ('active', ugt('active tasks')),
            ('sleeping', ugt('sleeping tasks')),
            ('blocked', ugt('blocked tasks')),
            ('delegated', ugt('delegated tasks')),
            ('completed', ugt('completed tasks')),
            ('trashed', ugt('trashed tasks')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'active':
            return (queryset
                    .filter(trashed=False, completed=False)
                    .exclude(sleepforever=True)
                    .exclude(sleepuntil__gte=now())
                    .exclude(assignee__isnull=False)
                    .exclude(blockers__completed=False))
        if self.value() == 'sleeping':
            incomplete = queryset.filter(trashed=False, completed=False)
            return (incomplete.filter(sleepforever=True) |
                    incomplete.filter(sleepuntil__gte=now()))
        if self.value() == 'blocked':
            return queryset.filter(trashed=False, completed=False,
                    blockers__completed=False)
        if self.value() == 'delegated':
            return queryset.filter(trashed=False, completed=False,
                    assignee__isnull=False)
        if self.value() == 'completed':
            return queryset.filter(trashed=False, completed=True)
        if self.value() == 'trashed':
            return queryset.filter(trashed=True)

class TaskAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['summary', 'completed', 'due', 'project', 'labels', 'details'],
        }),
        ('Internal', {
            'fields': ['sleepuntil', 'sleepforever', 'assignee', 'blockers', 'trashed'],
        }),
        ('Timestamp', {
            'fields': ['created', 'modified'],
        }),
    ]
    filter_horizontal = ['labels', 'blockers']
    readonly_fields = ('created', 'modified')
    save_on_top = True

    list_display = ('summary', 'due', 'completed', 'project', 'is_active',
            'is_sleeping', 'is_blocked', 'is_delegated')
    list_editable = ('completed',)
    list_filter = (StateFilter, LabelFilter, 'due', 'created')
    search_fields = ('summary', 'assignee', 'details')
    ordering = ('trashed', 'completed', 'assignee', 'blockers', 'sleepforever',
            'sleepuntil', 'project', 'due', 'created')

class LabelAdmin(admin.ModelAdmin):
    fields = ('name', 'trashed')
    save_on_top = True

    list_display = ('name', 'trashed')
    list_search = ('name',)
    list_filter = ('trashed',)

class AssigneeAdmin(admin.ModelAdmin):
    fields = ('name', 'last_request', 'last_response', 'trashed')
    save_on_top = True

    list_search = ('name',)
    list_display = ('name', 'last_request', 'last_response', 'trashed')
    list_filter = ('last_request', 'last_response', 'trashed')

admin.site.register(Task, TaskAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Assignee, AssigneeAdmin)
