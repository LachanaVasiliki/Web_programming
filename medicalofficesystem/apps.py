# Διαμόρφωση της εφαρμογής "medicalofficesystem"

from django.apps import AppConfig


class MedicalOfficesystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Ορισμός του τύπου του πεδίου auto field για την εφαρμογή
    name = 'medicalofficesystem'  # Ονομασία της εφαρμογής
