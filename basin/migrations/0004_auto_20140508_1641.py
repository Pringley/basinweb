# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basin', '0003_auto_20140508_1632'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='cslabels',
            new_name='labels',
        ),
    ]
