# Generated by Django 3.0.10 on 2020-10-03 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functionalvibesit', '0016_testimonial_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testimonial',
            name='category',
        ),
        migrations.AddField(
            model_name='testimonial',
            name='category',
            field=models.ManyToManyField(to='functionalvibes.TestimonialCategories'),
        ),
    ]
