# Generated by Django 3.0.10 on 2021-09-07 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('functionalvibesit', '0026_guidequestionary_questionaryfreeassessment_questionaryreceiveoffer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guidequestionary',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]