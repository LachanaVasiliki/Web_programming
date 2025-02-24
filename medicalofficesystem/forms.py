# Φόρμες για εγγραφή χρηστών και υποβολή παραστάσεων

from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from .models import Patient, Appointment, MedicalRecord, AppointmentSlot

from .models import User, Appointment

class RegistrationForm(UserCreationForm):
    # Φόρμα εγγραφής χρήστη με πεδία για email, όνομα, επώνυμο και τηλέφωνο
    email = forms.EmailField(label = "Email")  # Πεδίο για το email του χρήστη
    first_name = forms.CharField(label = "First name")  # Πεδίο για το όνομα
    last_name = forms.CharField(label = "Last name")  # Πεδίο για το επώνυμο
    phone = PhoneNumberField()  # Πεδίο για τον αριθμό τηλεφώνου
    
    class Meta:
        model = User  # Ορίζουμε το μοντέλο User για την φόρμα
        fields = ["first_name", "last_name", "email", "phone"]  # Πεδία που θα εμφανιστούν στη φόρμα

    def save(self, commit=True):
        user = super().save(commit=False)  
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.phone = self.cleaned_data["phone"]
        
        if commit:
            user.save()  

        return user
    
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient  # Ορίζουμε το μοντέλο Patient για τη φόρμα
        fields = ['amka']  # Πεδία που θα εμφανιστούν στη φόρμα
        #fields = ["amka", "full_name", "date_of_birth", "contact_info"]
        
    def save(self, user=None, commit=True):
        patient = super().save(commit=False)  # Λήψη του χρήστη χωρίς να γίνει commit
        if user:
            patient.user = user  
        if commit:
            patient.save()  # Αποθήκευση του χρήστη στη βάση
        return patient
    



class AppointmentForm(forms.ModelForm):
    available_slots = forms.ModelChoiceField(
        queryset=AppointmentSlot.objects.filter(is_available=True),
        empty_label="Επέλεξε ένα από τα διαθέσιμα ραντεβού",
        label="Διαθέσιμα ραντεβού"
    )

    class Meta:
        model = Appointment  # Ορίζουμε το μοντέλο Appointment για τη φόρμα
        fields = ["doctor", "available_slots"]  # Πεδία που θα εμφανιστούν στη φόρμα για ραντεβού

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if "doctor" in self.data:
            try:
                doctor_id = int(self.data.get("doctor"))
                self.fields["available_slots"].queryset = AppointmentSlot.objects.filter(doctor_id=doctor_id, is_available=True)
            except (ValueError, TypeError):
                pass


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord  # Ορίζουμε το μοντέλο MedicalRecord για τη φόρμα
        fields = ["patient", "doctor", "diagnosis", "treatment", 'appointment']  # Πεδία που θα εμφανιστούν στη φόρμα για το ιατρικό αρχείο
        widgets = {
            'appointment': forms.Select(attrs={'class': 'form-control', 'style': 'width: 200px;'}),  # Αν υπάρχει πεδίο για appointment
        }
