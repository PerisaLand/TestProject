# Generated by Django 4.1 on 2022-09-03 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('created',), 'verbose_name': 'نظرات', 'verbose_name_plural': 'نظرات'},
        ),
    ]
