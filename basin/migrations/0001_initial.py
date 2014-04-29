# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('trashed', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Assignee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('last_request', models.DateTimeField(blank=True, help_text='Last time you asked this person for something.', null=True)),
                ('last_response', models.DateTimeField(blank=True, help_text='Last time this person responded to you.', null=True)),
                ('trashed', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('summary', models.CharField(blank=True, max_length=144, null=True)),
                ('details', models.TextField(blank=True, null=True)),
                ('due', models.DateTimeField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('project', models.BooleanField(default=False, help_text='Set to True if this is a high-level project (as opposed to a granular action).')),
                ('trashed', models.BooleanField(default=False, help_text="Instead of deleting tasks, simply mark them as 'trashed' here.")),
                ('sleepuntil', models.DateTimeField(blank=True, verbose_name='sleep until', help_text='Put this task to sleep until specified time.', null=True)),
                ('sleepforever', models.BooleanField(default=False, verbose_name='sleep indefinitely', help_text='Put this task to sleep indefinitely.')),
                ('assignee', models.ForeignKey(blank=True, to='basin.Assignee', help_text='Delegate tasks by specifying an assignee.', to_field='id', null=True)),
                ('labels', models.ManyToManyField(blank=True, to='basin.Label')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
