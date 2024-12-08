# Generated by Django 3.2.25 on 2024-06-17 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functionalvibesit', '0032_auto_20210911_1708'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('order', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=250)),
                ('body', models.TextField()),
            ],
            options={
                'ordering': ['order', '-id', 'title'],
            },
        ),
    ]