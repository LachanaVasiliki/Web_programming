# Generated by Django 5.1.5 on 2025-02-12 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicalofficesystem', '0003_appointmentslot_secretary'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentslot',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
