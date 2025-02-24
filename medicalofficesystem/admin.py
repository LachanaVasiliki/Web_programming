# Εγγραφή μοντέλων στο admin panel του Django

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _
from .models import User, MedicalOffice, Doctor, Patient, Appointment

admin.site.register(User)  # Εγγραφή του μοντέλου User στο admin panel
# Διαμόρφωση της εμφάνισης του μοντέλου User στο admin
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # Πεδίο για email και password
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),  # Στοιχεία προσωπικών πληροφοριών
        (_('Permissions'), {'fields': ('is_active', 'is_secretary', 'is_superuser',
                                       'groups', 'user_permissions')}),  # Δικαιώματα χρήστη
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),  # Σημαντικές ημερομηνίες
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),  # Πεδίο για την προσθήκη νέου χρήστη
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_secretary')  # Εμφάνιση πεδίων στη λίστα
    search_fields = ('email', 'first_name', 'last_name')  # Πεδία αναζήτησης
    ordering = ('email',)  # Ταξινόμηση κατά email

class MedicalOfficeAdminForm(forms.ModelForm):
    class Meta:
        model = MedicalOffice
        fields = '__all__'  # Εγγραφή όλων των πεδίων του μοντέλου MedicalOffice
        widgets = {
            'doctors': forms.ModelMultipleChoiceField,  # Επιλογή πολλών γιατρούς
        }
        

    # Ορισμός πεδίου για τη σύνδεση γιατρών
    doctors = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(verbose_name='Users', is_stacked=False),
    )

    # Αρχικοποίηση των γιατρών αν υπάρχει ήδη το αντικείμενο
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['doctors'].initial = self.instance.doctor_set.values_list('user', flat=True)

    # Αποθήκευση των αλλαγών στο αντικείμενο
    def save(self, commit=True):

        instance = super().save(commit=False)  # Αποθήκευση χωρίς commit για να κάνουμε περαιτέρω τροποποιήσεις
        instance.save()

        selected_users = self.cleaned_data.get('doctors', [])  # Λήψη των επιλεγμένων γιατρών
        doctors = Doctor.objects.filter(user__in=selected_users, medicaloffices=instance)  # Φιλτράρισμα γιατρών
        existing_doctors = set(doctors.values_list('user', flat=True))  # Παλιότεροι γιατροί
        new_doctors = []  # Νέοι γιατροί

        # Αν προστίθεται νέος γιατρός
        for user in selected_users:
            if user not in existing_doctors:
                doctor, created = Doctor.objects.get_or_create(user=user)  # Δημιουργία ή λήψη γιατρού
                doctor.medicaloffices.add(instance)  # Προσθήκη του γιατρού στο ιατρείο
                new_doctors.append(doctor)

        doctors = Doctor.objects.filter(pk__in=[doctor.pk for doctor in doctors])  # Γιατροί που συνδέονται με το ιατρείο
        new_doctors = Doctor.objects.filter(pk__in=[doctor.pk for doctor in new_doctors])  # Νέοι γιατροί

        # Ενημέρωση γιατρών
        for doctor in doctors.union(new_doctors):
            doctor.medicaloffices.add(instance)

        return instance
    
    # Συνάρτηση για εμφάνιση γιατρών στο admin
    def get_doctors(self, obj):
        doctors = obj.doctors.all()
        return ', '.join(str(doctor) for doctor in doctors)
    
    get_doctors.short_description = 'Doctors'  # Εμφάνιση του τίτλου "Doctors"

# Εγγραφή του admin panel για το μοντέλο MedicalOffice
class MedicalOfficeAdmin(admin.ModelAdmin):
    form = MedicalOfficeAdminForm  # Χρήση της custom φόρμας για το MedicalOffice

admin.site.register(MedicalOffice, MedicalOfficeAdmin)  # Εγγραφή του MedicalOffice στο admin panel
admin.site.register(Patient)  # Εγγραφή του Patient στο admin panel
admin.site.register(Doctor)  # Εγγραφή του Doctor στο admin panel
admin.site.register(Appointment)  # Εγγραφή του Appointment στο admin panel
