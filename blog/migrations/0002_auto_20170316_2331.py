# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-03-16 15:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-index', 'id'], 'verbose_name': '分类', 'verbose_name_plural': '分类'},
        ),
        migrations.AlterField(
            model_name='article',
            name='desc',
            field=models.CharField(max_length=1000, verbose_name='文章描述'),
        ),
    ]