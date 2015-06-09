# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialcircle', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scuser',
            name='profile_image',
            field=models.ImageField(default=b'media/avatar/unknow_user.jpg', upload_to=b'media/avatar/'),
        ),
    ]
