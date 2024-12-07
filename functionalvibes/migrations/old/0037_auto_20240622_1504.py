# Generated by Django 3.2.25 on 2024-06-22 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functionalvibesit', '0036_post_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-post_date'], 'verbose_name': 'Post', 'verbose_name_plural': 'Posts'},
        ),
        migrations.AddField(
            model_name='guidequestionary',
            name='source',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(verbose_name='Post body'),
        ),
    ]
