# Generated by Django 3.0.10 on 2020-09-30 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functionalvibesit', '0008_testimonial_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonial',
            name='reviewer',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
