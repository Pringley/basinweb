from django.contrib import admin
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as ugt

from basin.models import Task

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
            return queryset.active()
        if self.value() == 'sleeping':
            return queryset.sleeping()
        if self.value() == 'blocked':
            return queryset.blocked()
        if self.value() == 'delegated':
            return queryset.delegated()
        if self.value() == 'completed':
            return queryset.completed()
        if self.value() == 'trashed':
            return queryset.filter(trashed=True)

class TaskAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['summary', 'completed', 'due', 'project', 'details', 'labels'],
        }),
        ('Internal', {
            'fields': ['sleepuntil', 'sleepforever', 'delegatedto', 'blockers', 'trashed'],
        }),
        ('Timestamp', {
            'fields': ['created', 'modified'],
        }),
    ]
    filter_horizontal = ['blockers']
    readonly_fields = ('created', 'modified')
    save_on_top = True

    list_display = ('summary', 'due', 'completed', 'project', 'is_active',
            'is_sleeping', 'is_blocked', 'is_delegated')
    list_editable = ('completed',)
    list_filter = (StateFilter, 'due', 'created')
    search_fields = ('summary', 'delegatedto', 'details')
    ordering = ('trashed', 'completed', 'delegatedto', 'blockers', 'sleepforever',
            'sleepuntil', 'project', 'due', 'created')

admin.site.register(Task, TaskAdmin)
