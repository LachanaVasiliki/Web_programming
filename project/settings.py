import os
from pathlib import Path

# Ορισμός του ρυθμιστικού αρχείου του Django για το project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Ρυθμίσεις βασικού φακέλου του έργου
BASE_DIR = Path(__file__).resolve().parent.parent

# Ορισμός μυστικού κλειδιού για την εφαρμογή (πρέπει να παραμείνει απόρρητο)
SECRET_KEY = 'django-insecure-v-zes40knfo^q5zh890!pl-u)8$dcopk(qky+qb#tt!o+u#vqt'

# Ενεργοποίηση λειτουργίας αποσφαλμάτωσης (Debug) για την ανάπτυξη
DEBUG = False

# Ρύθμιση επιτρεπόμενων hosts για την εφαρμογή
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Εγκατεστημένες εφαρμογές
INSTALLED_APPS = [
    'medicalofficesystem.apps.MedicalOfficesystemConfig',  # Η εφαρμογή για το ιατρικό σύστημα
    'phonenumber_field',  # Εφαρμογή για την υποστήριξη αριθμών τηλεφώνου
    'django.contrib.admin',  # Διαχειριστικό πάνελ του Django
    'django.contrib.auth',  # Διαχείριση χρηστών και πιστοποίησης
    'django.contrib.contenttypes',  # Διαχείριση τύπων περιεχομένων
    'django.contrib.sessions',  # Διαχείριση συνεδριών
    'django.contrib.messages',  # Υποστήριξη μηνυμάτων
    'django.contrib.staticfiles',  # Διαχείριση στατικών αρχείων
]

# Ρυθμίσεις Middleware για επεξεργασία αιτήσεων/απαντήσεων
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Ασφάλεια της εφαρμογής
    'django.contrib.sessions.middleware.SessionMiddleware',  # Υποστήριξη συνεδριών
    'django.middleware.common.CommonMiddleware',  # Κοινές ρυθμίσεις για αιτήσεις
    'django.middleware.csrf.CsrfViewMiddleware',  # Προστασία από επιθέσεις CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Διαχείριση πιστοποίησης χρηστών
    'django.contrib.messages.middleware.MessageMiddleware',  # Υποστήριξη μηνυμάτων
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Προστασία από Clickjacking επιθέσεις
]

# Ορισμός του βασικού αρχείου για τη διαχείριση των URLs
ROOT_URLCONF = 'project.urls'

# Ρυθμίσεις για τα templates της εφαρμογής
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Χρήση του Django template engine
        'DIRS': [BASE_DIR / 'templates'],  # Καθορισμός φακέλου για τα templates
        'APP_DIRS': True,  # Επιτρέπει την εύρεση templates από τις εφαρμογές
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Ενεργοποίηση αποσφαλμάτωσης
                'django.template.context_processors.request',  # Επεξεργασία αιτήσεων
                'django.contrib.auth.context_processors.auth',  # Διαχείριση δεδομένων χρηστών
                'django.contrib.messages.context_processors.messages',  # Υποστήριξη μηνυμάτων
            ],
        },
    },
]

# Ορισμός για την εφαρμογή WSGI
WSGI_APPLICATION = 'project.wsgi.application'

# Ρυθμίσεις για τη βάση δεδομένων (PostgreSQL)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # Χρήση PostgreSQL ως βάση δεδομένων
        "NAME": "medical_db",  # Όνομα της βάσης δεδομένων
        "USER": "medical_user",  # Χρήστης της βάσης δεδομένων
        "PASSWORD": "securepassword",  # Κωδικός πρόσβασης για τη βάση
        "HOST": "localhost",  # Διακομιστής της βάσης δεδομένων (τοπικός)
        "PORT": "5432",  # Θύρα για τη σύνδεση με την PostgreSQL
    }
}

# Ρυθμίσεις επικύρωσης κωδικών πρόσβασης για τους χρήστες
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Ρυθμίσεις για τη διεθνοποίηση (γλώσσα και ζώνη ώρας)
LANGUAGE_CODE = 'el-gr'  # Ρυθμίσεις για την ελληνική γλώσσα
TIME_ZONE = 'Europe/Athens'  # Ρυθμίσεις ώρας για Ελλάδα (Αθήνα)
USE_I18N = True  # Ενεργοποίηση διεθνοποίησης
USE_TZ = True  # Χρήση ζώνης ώρας

# Ρυθμίσεις για τα στατικά αρχεία
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'medicalofficesystem/static'),  # This points to your static folder
]

# Ρυθμίσεις για τα αρχεία media (όπως εικόνες και αρχεία από χρήστες)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'uploads/'  # Ο φάκελος για την αποθήκευση των media αρχείων

# Ρύθμιση για το πεδίο των μοντέλων
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Ορισμός προσαρμοσμένου μοντέλου χρήστη
AUTH_USER_MODEL = "medicalofficesystem.User"

# Ρυθμίσεις για τις σελίδες σύνδεσης/αποσύνδεσης
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"

# Ρυθμίσεις για την περιοχή αριθμών τηλεφώνου (Ελλάδα)
PHONENUMBER_DEFAULT_REGION = 'GR'  # Η Ελλάδα ως προεπιλεγμένη περιοχή για τους αριθμούς τηλεφώνου

