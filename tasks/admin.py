from django.contrib import admin
from tasks.models import Task, Label, Assignee

class LabelInline(admin.StackedInline):
    model = Label
    extra = 1

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

    list_display = ('summary', 'due', 'completed', 'is_active', 'is_sleeping',
            'is_blocked', 'is_delegated')
    list_editable = ('completed',)
    list_filter = ('due', 'created', 'completed', 'trashed')
    search_fields = ('summary', 'assignee', 'details')

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
