# Ορισμός των μοντέλων της εφαρμογής

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

# Διαχείριση χρηστών με την κλάση UserManager
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, phone, password, **extra_fields):
        # Ελέγχει αν τα απαιτούμενα πεδία (email και phone) υπάρχουν
        if not email:
            raise ValueError('Το πεδίο email είναι υποχρεωτικό')
        if not phone:
            raise ValueError('Το πεδίο phone είναι υποχρεωτικό')
        email = self.normalize_email(email)  # Κανονικοποιεί το email
        user = self.model(email=email, phone=phone, **extra_fields)  # Δημιουργεί τον χρήστη
        user.set_password(password)  # Ρυθμίζει τον κωδικό πρόσβασης
        user.save(using=self._db)  # Αποθηκεύει τον χρήστη στη βάση
        return user

    def create_user(self, email, phone, password=None, **extra_fields):
        # Δημιουργεί έναν κανονικό χρήστη
        extra_fields.setdefault('is_staff', False)  # Ο χρήστης δεν είναι μέλος του προσωπικού από προεπιλογή
        return self._create_user(email, phone, password, **extra_fields)

    def create_superuser(self, email, phone, password, **extra_fields):
        # Δημιουργεί έναν υπερχρήστη (superuser)
        extra_fields.setdefault('is_superuser', True)  # Ο υπερχρήστης είναι διαχειριστής
        extra_fields.setdefault('is_staff', True)  # Ο υπερχρήστης είναι μέλος του προσωπικού

        # Ελέγχει αν πληρούνται τα απαραίτητα κριτήρια
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, phone, password, **extra_fields)


# Ορισμός του μοντέλου User
class User(AbstractUser):
    username = None  # Δεν χρησιμοποιούμε το πεδίο username
    email = models.EmailField(_('Email Address'), unique=True)  # Πεδίο email
    phone = PhoneNumberField(blank=True, null=True, unique=True)  # Πεδίο τηλεφώνου
    ROLE_CHOICES = [('doctor', 'Doctor'), ('secretary', 'Secretary'), ('patient', 'Patient')]  # Επιλογές ρόλου
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')  # Ρόλος χρήστη

    USERNAME_FIELD = 'email'  # Χρησιμοποιούμε το email ως όνομα χρήστη
    REQUIRED_FIELDS = ['phone']  # Τα απαιτούμενα πεδία είναι το τηλέφωνο

    objects = UserManager()  # Χρήση του custom manager για τους χρήστες

    # Σχέση με τα groups και permissions για αποφυγή συγκρούσεων
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='medicalofficesystem_user_set',  # Σχέση με τα groups
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='medicalofficesystem_user_permissions_set',  # Σχέση με τα permissions
        blank=True
    )

    def __str__(self):
        return self.email  # Επιστρέφει το email του χρήστη


# Ορισμός του μοντέλου MedicalOffice
class MedicalOffice(models.Model):
    name = models.CharField(max_length=255)  # Όνομα του ιατρείου
    address = models.CharField(max_length=255)  # Διεύθυνση του ιατρείου
    contact_email = models.EmailField()  # Email επικοινωνίας
    contact_phone = models.CharField(max_length=15)  # Τηλέφωνο επικοινωνίας

    def __str__(self):
        return self.name  # Επιστρέφει το όνομα του ιατρείου


# Ορισμός του μοντέλου Doctor
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Σχέση με τον χρήστη
    specialty = models.CharField(max_length=100)  # Ειδικότητα του γιατρού
    available_slots = models.JSONField(default=list)  # Διάθεση θέσεων (σε μορφή JSON)
    medical_office=models.ForeignKey(MedicalOffice, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Dr. {self.user.email} ({self.specialty})"  # Επιστρέφει το όνομα και την ειδικότητα του γιατρού

class Secretary(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    medical_office = models.ForeignKey(MedicalOffice, on_delete=models.CASCADE)
    def __str__(self):
        return f"Secretary {self.user.email}"

class AppointmentSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    is_available = models.BooleanField(default=True)
    def __str__(self):
        return f"Ιατρός: {self.doctor.user.email} στις {self.date} και ώρα {self.time}"

# Ορισμός του μοντέλου Patient
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Σχέση με τον χρήστη
    amka = models.CharField(max_length=11, unique=True, blank=False, null=False)  # Αριθμός μητρώου ασφάλισης (ΑΜΚΑ)
    date_of_birth = models.DateField(blank=True, null=True)  # Ημερομηνία γέννησης
    contact_info = models.TextField()  # Στοιχεία επικοινωνίας
    registration_date = models.DateTimeField(auto_now_add=True)  # Ημερομηνία εγγραφής

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"  # Επιστρέφει το όνομα και το επώνυμο του ασθενούς


# Ορισμός του μοντέλου Appointment
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  # Σχέση με τον ασθενή
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # Σχέση με τον γιατρό
    date_time = models.DateTimeField()  # Ημερομηνία και ώρα ραντεβού
    duration = models.PositiveIntegerField(default=30)  # Διάρκεια ραντεβού σε λεπτά
    reason = models.TextField(blank=True, null=True)  # Λόγος ραντεβού
    status = models.CharField(
        choices=[("Scheduled", "Scheduled"), ("Completed", "Completed"), ("Cancelled", "Cancelled")],
        default="Scheduled"  # Κατάσταση ραντεβού
    )

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user.email} on {self.date_time}"  # Επιστρέφει την περιγραφή του ραντεβού


# Ορισμός του μοντέλου MedicalRecord
class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)  # Σχέση με τον ασθενή
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # Σχέση με τον γιατρό
    appointment = models.ForeignKey(Appointment, null=True, blank=True, on_delete=models.SET_NULL)  # Σχέση με το ραντεβού
    diagnosis = models.TextField()  # Διάγνωση
    treatment = models.TextField()  # Θεραπεία
    notes = models.TextField(blank=True, null=True)  # Πρόσθετες σημειώσεις
    date = models.DateTimeField(auto_now_add=True)  # Ημερομηνία καταγραφής

    def __str__(self):
        return f"Medical Record for {self.patient.user.email} ({self.date})"  # Επιστρέφει το email του ασθενούς και την ημερομηνία
