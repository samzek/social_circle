# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='SCUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(unique=True, max_length=20)),
                ('email', models.CharField(unique=True, max_length=255, verbose_name=b'email address')),
                ('first_name', models.CharField(max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('profile_image', models.ImageField(default=b'images/unknow_user.jpg', upload_to=b'media/avatar/')),
                ('user_bio', models.CharField(max_length=600, blank=True)),
                ('address', models.CharField(max_length=30, null=True, blank=True)),
                ('birth_date', models.DateField()),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user', models.ManyToManyField(related_name='user_rel_+', to=settings.AUTH_USER_MODEL, blank=True)),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('like_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('post_type', models.CharField(default=b'is_text', max_length=20, choices=[(b'is_text', b'Text'), (b'is_video', b'Video'), (b'is_photo', b'Photo')])),
                ('content', models.CharField(default=b'', max_length=600, null=True, blank=True)),
                ('file', models.FileField(upload_to=b'media/%Y/%m/%d', blank=True)),
                ('post_user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='like',
            name='like_post',
            field=models.ForeignKey(to='socialcircle.Post'),
        ),
        migrations.AddField(
            model_name='like',
            name='like_user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
