# Generated by Django 3.1 on 2020-09-16 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0003_records'),
    ]

    operations = [
        migrations.AddField(
            model_name='records',
            name='doctor_username',
            field=models.CharField(default='sdk', max_length=100),
        ),
        migrations.AddField(
            model_name='records',
            name='patient_username',
            field=models.CharField(default='skdjks', max_length=100),
        ),
    ]
