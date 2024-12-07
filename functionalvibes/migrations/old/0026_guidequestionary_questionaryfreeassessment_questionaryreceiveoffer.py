# Generated by Django 3.0.10 on 2021-09-07 23:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('functionalvibesit', '0025_auto_20210227_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionaryFreeAssessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionaryReceiveOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='GuideQuestionary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=18, null=True)),
                ('maximize_effectiveness_of_my_training', models.BooleanField(default=False)),
                ('get_back_in_shape', models.BooleanField(default=False)),
                ('learn_how_to_exercise_on_my_own', models.BooleanField(default=False)),
                ('need_motivation_and_accountability', models.BooleanField(default=False)),
                ('have_a_specific_injury_or_condition', models.BooleanField(default=False)),
                ('have_a_specific_goal_sport_or_event', models.BooleanField(default=False)),
                ('want_supervision_and_support', models.BooleanField(default=False)),
                ('agree_to_receive_other_communications', models.BooleanField(default=False)),
                ('get_a_free_assessment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='functionalvibes.QuestionaryFreeAssessment')),
                ('receive_an_offer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='functionalvibes.QuestionaryReceiveOffer')),
            ],
            options={
                'verbose_name': '04 Questionary',
                'verbose_name_plural': '04 Questionaries',
            },
        ),
    ]
