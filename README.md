Medical Office Management System

Overview

This project is a Medical Office Management System built as part of a university assignment. The goal was not to create a large or complex application, but to model a realistic medical office scenario correctly, following clear rules and constraints.
The focus of the project is on correct domain modeling, role-based logic, and server-side validation, rather than UI features.
________________________________________
Academic Requirements

The system was designed according to specific requirements set by the course instructor:
•	The Medical Office is identified by its name, not by a numeric ID.
•	A Medical Office can only be associated with a user who is a Doctor.
•	Patients are not allowed to own or manage a Medical Office.
•	These rules are enforced both at the model level and in application logic.
The purpose of these constraints is to reflect real-world semantics and prevent invalid data relationships.
________________________________________
What the System Does

User Roles

•	Doctor
o	Can be linked to a Medical Office
o	Can manage office-related data

•	Patient
o	Has restricted access
o	Cannot be associated with a Medical Office

Medical Office Management
•	Creation of medical offices using a unique name
•	Validation to prevent duplicate or invalid entries
•	Explicit checks to ensure only doctors can be assigned
________________________________________
Data Model Notes

•	MedicalOffice

o	Uses name as the primary identifier
o	Linked to a user only if the user has the Doctor role

•	User

o	Includes a role field (Doctor / Patient)
o	Role is validated before relationships are created
All constraints are enforced server-side to avoid bypassing the rules.
________________________________________
Security & Validation

•	Role-based access control for sensitive actions
•	Server-side validation of all business rules
•	No credentials or sensitive data included in the repository
The system is designed to fail safely when invalid input is provided.
________________________________________
Tech Stack

•	Python
•	Django
•	Relational database (SQLite / PostgreSQL)
________________________________________
Setup:

git clone <repository-url>

cd medical-office-system

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
________________________________________
Why This Project Matters

This project demonstrates:

•	Careful modeling of real-world constraints
•	Proper use of Django relationships and validation
•	A security-aware mindset in backend development
The emphasis is on doing the basics correctly, which is essential in real systems.

