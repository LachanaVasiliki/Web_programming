from .models import MedicalOffice, Appointment, Patient, MedicalRecord, Doctor, AppointmentSlot, Secretary  
from .forms import RegistrationForm, AppointmentForm, PatientForm, MedicalRecordForm  

from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden, FileResponse
from django.http import JsonResponse

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

def index(request):
    return render(request, 'index.html')  # Αρχική σελίδα

def medicaloffices(request):
    medicaloffices = MedicalOffice.objects.all()
    return render(request, 'view_medical_offices.html', {'medicaloffices': medicaloffices})  # Λίστα ιατρικών γραφείων


def signup(request):
    if request.method == 'POST':  # Αν είναι POST αίτηση
        form = RegistrationForm(request.POST)
        if form.is_valid():  # Έγκυρη φόρμα
            user = form.save()  # Δημιουργία χρήστη
            user.role = "patient" # Set default role
            user.save()
            login(request, user)  # Σύνδεση χρήστη
            return redirect("/complete_profile/") 
    else:
        form = RegistrationForm() # Δημιουργία φόρμας εγγραφής
    
    return render(request, "signup.html", {"form": form}) # Εμφάνιση φόρμας εγγραφής

def complete_profile(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(user=request.user)
            return redirect("medicalofficesystem:profile") 
    else:
        form = PatientForm()
    
    return render(request, "complete_profile.html", {"form": form})
 
   

def login_view(request):
    if request.method == 'POST':  # Αν είναι POST αίτηση
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():  # Έγκυρη φόρμα σύνδεσης
            user = form.get_user()  # Λήψη χρήστη
            login(request, user)  # Σύνδεση χρήστη
            return redirect('medicalofficesystem:profile')  # Ανακατεύθυνση στο προφίλ
    else:
        form = AuthenticationForm() # Δημιουργία φόρμας σύνδεσης
    return render(request, 'login.html', {'form': form})  # Εμφάνιση φόρμας σύνδεσης

# Λίστα ασθενών (only accessible by doctors & secretaries)
@login_required
def list_patients(request):
    if request.user.role not in ['doctor', 'secretary']:  # Ελέγχει αν ο χρήστης έχει δικαιώματα
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    search_amka = request.GET.get('search_amka', '')

    if search_amka:
        patients = Patient.objects.filter(amka__icontains=search_amka)  # Case-insensitive
    else:
        patients = Patient.objects.all()  # Λήψη ασθενών από τη βάση δεδομένων
    return render(request, 'list_patients.html', {'patients': patients})  # Εμφάνιση λίστας ασθενών


@login_required
def profile(request):
    user = request.user  # Λήψη δεδομένων χρήστη
    try:
        patient = Patient.objects.get(user=user)  # αν ο χρήστης ειναι ασθενής
        amka = patient.amka
    except Patient.DoesNotExist:
        amka = None

    if not amka:
        amka_message = "AMKA not available."
    else:
        amka_message = None

    medicaloffice = None  # Αρχικοποίηση

    try:
        doctor = Doctor.objects.get(user=user)  # αν ο χρήστης είναι γιατρός
        medicaloffice = doctor.medical_office  # Ο γιατρός έχει ιατρείο
    except Doctor.DoesNotExist:
        pass

    try:
        secretary = Secretary.objects.get(user=user)  # αν ο χρήστης είναι γραμματέας
        medicaloffice = secretary.medical_office
    except Secretary.DoesNotExist:
        pass   # Αν δεν είναι γραμματέας, απλά προχωράμε

    return render(request, 'profile.html', {
        'user': user,
        'amka': amka,
        'amka_message': amka_message,
        'medicaloffice': medicaloffice
    })
    #return render(request, 'profile.html', {'user': user})  # Εμφάνιση προφίλ χρήστη

@login_required
def logout_view(request):
    logout(request)  # Αποσύνδεση χρήστη
    return render(request, 'logout.html')  # Εμφάνιση σελίδας αποσύνδεσης

@login_required  # Προσθήκη νέου ασθενούς
def add_patient(request):
    if request.user.role != 'secretary':  # Ελέγχει αν ο χρήστης είναι γραμματέας
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    if request.method == "POST":  # Αν είναι POST αίτηση
        form = PatientForm(request.POST)
        if form.is_valid():  # Έγκυρη φόρμα
            form.save()  # Αποθήκευση νέου ασθενούς
            return redirect('list_patients')  # Ανακατεύθυνση στη λίστα ασθενών
    else:
        form = PatientForm()  # Δημιουργία φόρμας για νέο ασθενή
    return render(request, 'add_patient.html', {'form': form})  # Εμφάνιση φόρμας προσθήκης ασθενούς

@login_required  # Επεξεργασία υπαρχόντων ασθενών
def edit_patient(request, amka):
    patient = get_object_or_404(Patient, amka=amka)  # Λήψη ασθενούς από τη βάση δεδομένων
    if request.user.role != 'secretary':  # Ελέγχει αν ο χρήστης είναι γραμματέας
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    if request.method == "POST":  # Αν είναι POST αίτηση
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():  # Έγκυρη φόρμα
            form.save()  # Αποθήκευση επεξεργασμένων στοιχείων ασθενούς
            return redirect('list_patients')  # Ανακατεύθυνση στη λίστα ασθενών
    else:
        form = PatientForm(instance=patient)  # Δημιουργία φόρμας με τα υπάρχοντα δεδομένα του ασθενούς
    return render(request, 'edit_patient.html', {'form': form})  # Εμφάνιση φόρμας επεξεργασίας ασθενούς


@login_required
def book_appointment(request):
    if request.user.role != 'patient':  # Ελέγχει αν ο χρήστης είναι ασθενής
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == "POST":  # Αν είναι POST αίτηση
        form = AppointmentForm(request.POST, user=request.user)
        if form.is_valid():  # Έγκυρη φόρμα
            appointment = form.save(commit=False)  # Αποθήκευση χωρίς δέσμευση
            try:
                patient = Patient.objects.get(user=request.user)  # Βρίσκουμε τον ασθενή που σχετίζεται με τον χρήστη
            except Patient.DoesNotExist:
                return JsonResponse({'error': 'Patient not found for the current user'}, status=404)

            appointment.patient = patient  # Αναθέτουμε τον τρέχοντα χρήστη ως ασθενή
            selected_slot = form.cleaned_data['available_slots']  # Παίρνουμε το επιλεγμένο slot
            
            if selected_slot.is_available:  # Ελέγχουμε αν το slot είναι διαθέσιμο
                selected_slot.is_available = False  # Μαρκάρουμε το slot ως μη διαθέσιμο
                selected_slot.save()  # Αποθηκεύουμε την αλλαγή στο slot
                
                return redirect('view_user_appointment')  # Ανακατεύθυνση στη λίστα ραντεβού
            else:
                form.add_error('available_slots', 'Το επιλεγμένο ραντεβού δεν είναι πλέον διαθέσιμο.')

    else:
        form = AppointmentForm(user=request.user)  # Δημιουργία φόρμας για ραντεβού

    return render(request, 'book_appointment.html', {'form': form})  # Εμφάνιση φόρμας δημιουργίας ραντεβού

@login_required
def view_medical_history(request, amka):
    patient = get_object_or_404(Patient, amka=amka)  # Λήψη ασθενούς από τη βάση δεδομένων
    if request.user != patient.user and not request.user.groups.filter(name="Doctor").exists(): 
        return HttpResponseForbidden()  # Απαγόρευση πρόσβασης αν ο χρήστης δεν είναι γιατρός ή ασθενής
    medical_records = MedicalRecord.objects.filter(patient=patient)  # Λήψη ιατρικού ιστορικού ασθενούς
    return render(request, "view_medical_history.html", {"patient": patient, "records": medical_records})   # Εμφάνιση ιατρικού ιστορικού

@login_required
def medical_record_detail(request, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id)
    return render(request, 'medical_record_detail.html', {'record': record})


@login_required
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)  # Λήψη ραντεβού από τη βάση δεδομένων

    if request.user != appointment.patient.user and request.user != appointment.doctor.user:
        return HttpResponseForbidden('You are not authorized to view this appointment.')  # Απαγόρευση πρόσβασης αν ο χρήστης δεν έχει δικαίωμα

    medical_records = MedicalRecord.objects.filter(appointment=appointment)  # Λήψη ιατρικών εγγράφων για το ραντεβού

    context = {
        'appointment': appointment,
        'medical_records': medical_records,  
    }

    return render(request, 'appointment_detail.html', context)  # Εμφάνιση λεπτομερειών ραντεβού

@login_required
def view_medicaloffice_appointments(request, medicaloffice_id):
    medicaloffice = get_object_or_404(MedicalOffice, id=medicaloffice_id)  # Λήψη ιατρικού γραφείου από τη βάση δεδομένων

    # Ελέγχουμε αν ο χρήστης είναι είτε γιατρός είτε γραμματέας στο συγκεκριμένο ιατρείο
    is_doctor = Doctor.objects.filter(user=request.user, medical_office=medicaloffice).exists()
    is_secretary = Secretary.objects.filter(user=request.user, medical_office=medicaloffice).exists()

    if not (is_doctor or is_secretary):  # Αν δεν είναι ούτε γιατρός ούτε γραμματέας
        return HttpResponseForbidden("Access Denied.")  # Απαγόρευση πρόσβασης
    
     # Αν είναι γιατρός, φέρνουμε τα ραντεβού του, αλλιώς αν είναι γραμματέας, φέρνουμε όλα τα ραντεβού του ιατρείου
    if is_doctor:
        appointments = Appointment.objects.filter(doctor__user=request.user, doctor__in=medicaloffice.doctor_set.all())
    else:  # Αν είναι γραμματέας
        appointments = Appointment.objects.filter(doctor__in=medicaloffice.doctor_set.all())

    context = {
        'medicaloffice': medicaloffice,
        'appointments': appointments,
    }
    return render(request, 'view_med_appointment.html', context)  # Εμφάνιση ραντεβού του ιατρικού γραφείου


@login_required
def view_user_appointment(request):
    user = request.user
    appointments = Appointment.objects.filter(patient__user=user)  # Λήψη ραντεβού του χρήστη

    return render(request, 'view_user_appointment.html', {'appointments': appointments})  # Εμφάνιση ραντεβού του χρήστη


@login_required
def download_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)  # Λήψη ραντεβού από τη βάση δεδομένων
    if not request.user.is_superuser and not request.user.is_secretary and request.user != appointment.doctor.user and request.user != appointment.patient.user:
        return HttpResponseForbidden("You do not have permission to download this file.")  # Απαγόρευση πρόσβασης

    if not hasattr(appointment, 'file') or not appointment.file:  # Αν δεν υπάρχει αρχείο ραντεβού
        return HttpResponse("No file available for this appointment.", status=404)

    file_path = appointment.file.path  # Λήψη διαδρομής αρχείου
    response = FileResponse(open(file_path, 'rb'))  # Δημιουργία απόκρισης με το αρχείο
    response['Content-Disposition'] = f'attachment; filename="{appointment.file.name}"'  # Λήψη αρχείου
    return response

@login_required
def add_medical_record(request, amka):
    patient = get_object_or_404(Patient, amka=amka)

    # Μόνο γιατροί και γραμματείς μπορούν να προσθέσουν ιστορικό
    if not (request.user.is_staff or request.user.role in ["doctor", "secretary"]):
        return HttpResponseForbidden("Δεν έχετε άδεια να προσθέσετε ιατρικό ιστορικό.")

    if request.method == "POST":
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient

            # Ελέγχουμε αν το πεδίο appointment υπάρχει στο αίτημα
            if 'appointment' in form.cleaned_data and form.cleaned_data['appointment']:
                record.appointment = form.cleaned_data['appointment']
            else:
                record.appointment = None  # προεπιλεγμένη τιμή

            record.save()
            messages.success(request, "Το ιατρικό ιστορικό προστέθηκε με επιτυχία.")
            return redirect('medicalofficesystem:view_medical_history', amka=amka)
    else:
        form = MedicalRecordForm()

    return render(request, 'add_medical_record.html', {'form': form, 'patient': patient})

@login_required
def delete_medical_record(request, amka, record_id):
    record = get_object_or_404(MedicalRecord, id=record_id, patient__amka=amka)

    # Μόνο γιατροί και γραμματείς μπορούν να διαγράψουν
    if not (request.user.is_staff or request.user.role in ["doctor", "secretary"]):
        return HttpResponseForbidden("Δεν έχετε άδεια να διαγράψετε ιατρικό ιστορικό.")
    
    record.delete()
    messages.success(request, "Το ιατρικό ιστορικό διαγράφηκε με επιτυχία.")
    return redirect('medicalofficesystem:view_medical_history', amka=amka)


def medicaloffice_details(request, medicaloffice_id):
    medicaloffice = get_object_or_404(MedicalOffice, id=medicaloffice_id)  # Λήψη ιατρικού γραφείου

    user_is_doctor = False
    if request.user.is_authenticated:  # Ελέγχει αν ο χρήστης είναι γιατρός στο ιατρικό γραφείο
        user_is_doctor = medicaloffice.doctor_set.filter(user=request.user).exists()  

    context = {
        'medicaloffice': medicaloffice,
        'user_is_doctor': user_is_doctor,
    }

    return render(request, 'medicaloffice_details.html', context)  # Εμφάνιση λεπτομερειών ιατρικού γραφείου

@login_required
def list_appointments(request):
    if request.user.role == 'doctor':  # Αν ο χρήστης είναι γιατρός
        appointments = Appointment.objects.filter(doctor__user=request.user)
    elif request.user.role == 'patient':  # Αν ο χρήστης είναι ασθενής
        appointments = Appointment.objects.filter(patient__user=request.user)
    else:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    return render(request, 'list_appointments.html', {'appointments': appointments})  # Εμφάνιση λίστας ραντεβού
