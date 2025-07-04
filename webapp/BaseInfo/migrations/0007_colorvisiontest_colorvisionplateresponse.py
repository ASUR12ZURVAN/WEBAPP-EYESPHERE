# Generated by Django 5.1.5 on 2025-05-19 01:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0006_alter_testresult_final_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColorVisionTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_taken', models.DateTimeField(auto_now_add=True)),
                ('normal_correct', models.PositiveIntegerField(default=0)),
                ('red_green_errors', models.PositiveIntegerField(default=0)),
                ('protanopia_indicators', models.PositiveIntegerField(default=0)),
                ('deuteranopia_indicators', models.PositiveIntegerField(default=0)),
                ('severity_level', models.CharField(choices=[('none', 'None'), ('weak', 'Weak'), ('moderate', 'Moderate'), ('strong', 'Strong')], default='none', max_length=10)),
                ('diagnosis_text', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='color_vision_tests', to='BaseInfo.user')),
            ],
        ),
        migrations.CreateModel(
            name='ColorVisionPlateResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plate_number', models.PositiveIntegerField()),
                ('user_answer', models.CharField(max_length=100)),
                ('expected_text', models.CharField(max_length=255)),
                ('result', models.CharField(choices=[('correct', 'Correct'), ('incorrect', 'Incorrect')], max_length=10)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plate_responses', to='BaseInfo.colorvisiontest')),
            ],
        ),
    ]
