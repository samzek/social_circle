# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=50, null=True, blank=True)),
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
                ('content', models.CharField(max_length=600, null=True)),
                ('is_photo', models.BooleanField(default=False)),
                ('is_video', models.BooleanField(default=False)),
                ('is_text', models.BooleanField(default=False)),
                ('post_cat', models.ForeignKey(to='socialcircle.Cat')),
            ],
        ),
        migrations.CreateModel(
            name='SCUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=20)),
                ('email', models.CharField(unique=True, max_length=255, verbose_name=b'email address')),
                ('first_name', models.CharField(max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('user_bio', models.CharField(max_length=600, blank=True)),
                ('password', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=30, null=True, blank=True)),
                ('birth_date', models.DateTimeField(blank=True)),
                ('user', models.ManyToManyField(related_name='user_rel_+', to='socialcircle.SCUser', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='post_user',
            field=models.ManyToManyField(to='socialcircle.SCUser'),
        ),
        migrations.AddField(
            model_name='like',
            name='like_post',
            field=models.ForeignKey(to='socialcircle.Post'),
        ),
        migrations.AddField(
            model_name='like',
            name='like_user',
            field=models.ForeignKey(to='socialcircle.SCUser'),
        ),
    ]
