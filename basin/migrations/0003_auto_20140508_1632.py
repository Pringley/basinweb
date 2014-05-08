# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('basin', '0002_task_blockers'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='cslabels',
            field=models.TextField(default='', validators=[django.core.validators.RegexValidator('^\\s*([A-Za-z0-9_\\-]+)(\\s*,\\s*[A-Za-z0-9_\\-]+)*(\\s*,\\s*)?$', code='not-alnum-csv', message='labels must be alphanumeric, comma-separated')], blank=True, help_text='Comma-separated labels'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='delegatedto',
            field=models.CharField(max_length=128, blank=True, default='', help_text='Delegate tasks by specifying an delegatedto.'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='task',
            name='labels',
        ),
        migrations.RemoveField(
            model_name='task',
            name='assignee',
        ),
        migrations.AlterField(
            model_name='task',
            name='summary',
            field=models.CharField(max_length=144, blank=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='details',
            field=models.TextField(blank=True),
        ),
        migrations.DeleteModel(
            name='Label',
        ),
        migrations.DeleteModel(
            name='Assignee',
        ),
    ]
