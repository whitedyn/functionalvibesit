# Generated by Django 3.0.10 on 2024-07-26 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functionalvibesit', '0038_guidefile_is_price_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('title', models.CharField(max_length=120)),
                ('order', models.IntegerField(default=0)),
                ('photo', models.ImageField(upload_to='slides')),
                ('subtitle', models.CharField(blank=True, max_length=240, null=True)),
                ('button_text', models.CharField(blank=True, max_length=120, null=True)),
                ('button_link', models.CharField(blank=True, max_length=220, null=True)),
                ('second_button_text', models.CharField(blank=True, max_length=120, null=True)),
                ('second_button_link', models.CharField(blank=True, max_length=220, null=True)),
            ],
            options={
                'verbose_name_plural': 'Slides',
            },
        ),
    ]
