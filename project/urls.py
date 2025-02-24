from django.contrib import admin
from django.urls import include, path

# Ρυθμίσεις δρομολόγησης URL (URL routing settings)
urlpatterns = [
    path('admin/', admin.site.urls),  # Διαχειριστικό πάνελ (Admin Panel)
    path('', include("medicalofficesystem.urls"))  # Εφαρμογή συστήματος ιατρείου (Include URLs from the medicalofficesystem app)
]
