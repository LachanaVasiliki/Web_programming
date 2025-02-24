from django.urls import path
from . import views

from project import settings
from django.conf.urls.static import static

app_name = "medicalofficesystem"

urlpatterns = [
    path('', views.index, name='index'),  # Αρχική σελίδα
    path('medicaloffices/', views.medicaloffices, name='view_medical_offices'),  # Λίστα ιατρικών γραφείων
    path('signup/', views.signup, name='signup'),  # Σελίδα εγγραφής χρήστη
    path('login/', views.login_view, name='login'),  # Σελίδα σύνδεσης χρήστη
    path('profile/', views.profile, name='profile'),  # Προφίλ χρήστη
    path('logout/', views.logout_view, name='logout'),  # Αποσύνδεση χρήστη
    path("complete_profile/", views.complete_profile, name="complete_profile"),

    path('patients/', views.list_patients, name='list_patients'),  # Λίστα ασθενών
    path('patients/add/', views.add_patient, name='add_patient'),  # Προσθήκη νέου ασθενούς
    path('patients/edit/<int:amka>/', views.edit_patient, name='edit_patient'),  # Επεξεργασία στοιχείων ασθενούς
    path("medical_history/<int:amka>/", views.view_medical_history, name="view_medical_history"),  # Ιατρικό ιστορικό ασθενούς
    path('medical_record/<int:record_id>/', views.medical_record_detail, name='medical_record_detail'),  # Λεπτομέρειες ιατρικού αρχείου
    path('medical_record/add/<int:amka>/', views.add_medical_record, name='add_medical_record'),  # Προσθήκη νέου ιστορικού
    path('medical_record/delete/<int:amka>/<int:record_id>/', views.delete_medical_record, name='delete_medical_record'),  # Διαγραφή ιστορικού
    
    path('appointments/', views.list_appointments, name='list_appointments'),  # Λίστα ραντεβού
    path("book_appointment/", views.book_appointment, name="book_appointment"),  # Δημιουργία νέου ραντεβού
    path('appointments/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),  # Λεπτομέρειες ραντεβού
    path('appointments/<int:appointment_id>/download/', views.download_appointment, name='download_appointment'),  # Λήψη αρχείου ραντεβού
    path('user_appointments/', views.view_user_appointment, name='view_user_appointment'),
    path('download_appointment/<int:appointment_id>/', views.download_appointment, name='download_appointment'),

    path('medicaloffice/<int:medicaloffice_id>/', views.medicaloffice_details, name='medicaloffice_details'),  # Λεπτομέρειες ιατρικού γραφείου
    path('medicaloffice/<int:medicaloffice_id>/view_appointments/', views.view_medicaloffice_appointments, name='view_med_appointment'),  # Προβολή ραντεβού στο ιατρικό γραφείο
]

# Προαιρετικό  ##################################
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #για τα στατικά στοιχεία στην αναππτυξη
