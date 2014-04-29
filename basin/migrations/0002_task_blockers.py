# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='blockers',
            field=models.ManyToManyField(blank=True, to='basin.Task'),
            preserve_default=True,
        ),
    ]
