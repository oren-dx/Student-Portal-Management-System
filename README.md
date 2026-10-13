# 🎓 Student Portal Management System

A web-based **Student Portal Management System** built with Python and Django. This application helps educational institutions manage student profiles, academic results, semester information, tuition fees, and fee payments through a centralized platform.

The system includes role-based user management for Admins and Students, making student information and academic records easier to organize and access.

## 🚀 Features

### 👤 User Management
- Custom user model using Django's `AbstractUser`.
- Role-based access for Admin and Student.
- User authentication and account management.
- Separate roles for administrators and students.

### 🧑‍🎓 Student Profile Management
- Create and manage student profiles.
- Store student name, email, phone number, and address.
- Upload and manage student profile images.
- Manage academic departments:
  - BBA
  - CSE
  - EEE
- Connect each student profile to a user account.

### 📚 Academic Result Management
- Store student examination results.
- Manage semester-wise academic records.
- Record subject names and marks obtained.
- Store total marks, grades, and GPA.
- Track examination years.
- Support all eight semesters.

### 💰 Student Fee Management
- Manage different types of student fees:
  - Tuition Fee
  - Semester Fee
  - Other Fees
- Record fee amounts, descriptions, and due dates.
- Track the amount paid and the remaining balance.
- Maintain fee records for individual students.

### 💳 Fee Payment Management
- Record student fee payments.
- Support multiple payment methods:
  - Cash
  - Bank Transfer
  - Mobile Banking
- Store transaction IDs for payment tracking.
- Record payment dates.
- Automatically calculate total paid amounts and outstanding dues.

## 🛠️ Technologies Used

- **Backend:** Python, Django
- **Database:** SQLite (default development database)
- **Frontend:** HTML, CSS, Bootstrap (if implemented)
- **Authentication:** Django Authentication System
- **ORM:** Django Models and QuerySets
- **Version Control:** Git and GitHub

## 📂 Project Structure

```text
Student-Portal/
│
├── manage.py
├── requirements.txt
├── db.sqlite3
│
├── StudentPortal/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── studentapp/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   └── templates/
│
├── static/
├── media/
└── README.md
```

*Note: Update the folder and app names to match your actual project structure.*

## ⚙️ Installation and Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repository.git
```

Navigate to the project directory:

```bash
cd Student-Portal
```

### 2. Create a Virtual Environment

```bash
python -m venv env
```

Activate the environment on Windows:

```bash
env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install django pillow
```

If you have a `requirements.txt` file, install all dependencies using:

```bash
pip install -r requirements.txt
```

### 4. Configure the Custom User Model

In `settings.py`, make sure the custom user model is configured before creating the database tables:

```python
AUTH_USER_MODEL = 'studentapp.UserModel'
```

Replace `studentapp` with the actual Django app name.

### 5. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an administrator account.

### 7. Run the Development Server

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

Django Admin is available at:

```text
http://127.0.0.1:8000/admin/
```

## 🗄️ Database Models

The application uses five primary Django models.

| Model | Description |
|---|---|
| `UserModel` | Manages user accounts and roles |
| `StudentModel` | Stores student profile information |
| `ResultModel` | Stores semester-wise academic results |
| `FeeModel` | Maintains student fee records and outstanding balances |
| `FeePaymentModel` | Records fee payments and transaction details |

### Model Relationships

- `UserModel` → `StudentModel`: One-to-one relationship.
- `UserModel` → `ResultModel`: One-to-many relationship.
- `StudentModel` → `ResultModel`: One-to-many relationship.
- `StudentModel` → `FeeModel`: One-to-many relationship.
- `StudentModel` → `FeePaymentModel`: One-to-many relationship.
- `FeeModel` → `FeePaymentModel`: One-to-many relationship.

These relationships help organize student information, academic results, and financial records.

## 🧮 Fee Calculation

The system provides properties to calculate paid amounts and outstanding balances.

```python
@property
def paid_amount(self):
    return self.payments.aggregate(
        total=models.Sum('amount')
    )['total'] or 0

@property
def due_amount(self):
    return self.amount - self.paid_amount
```

- **Paid Amount:** Total payments recorded against a fee.
- **Due Amount:** Original fee amount minus the total paid amount.

For reliable financial calculations, fee amounts and payment amounts should be validated to prevent negative payments or payments exceeding the outstanding balance.

## 🔐 Security and Access Control

The custom user model defines two user roles:

- **Admin:** Intended for managing student records, results, fees, and payments.
- **Student:** Intended for accessing personal academic and financial information.

Actual permissions depend on the implementation in the project's views, URL configurations, and templates. Role checks should also be enforced on the server side.

## 🎯 Project Objectives

- Simplify student information management.
- Organize academic results and semester records.
- Improve fee collection and payment tracking.
- Calculate outstanding student balances.
- Maintain structured academic and financial records.
- Practice Django model relationships and custom authentication.

## 🔮 Future Improvements

- Student dashboard with academic summaries.
- Admin dashboard with statistics and reports.
- Search and filter students by name, department, and semester.
- Result sheets and downloadable transcripts.
- Fee receipts and downloadable payment reports.
- Email notifications for upcoming fee deadlines.
- REST API integration using Django REST Framework.
- Online payment gateway integration.
- Deployment using Render or another cloud hosting platform.

## 👨‍💻 Developer

**Oren Michael Dessai**

Aspiring Python Backend Developer focused on Django, database-driven applications, and web development.

- GitHub: [oren-dx](https://github.com/oren-dx)

## 📄 License

This project is intended for educational and portfolio purposes. Add a specific open-source license, such as the MIT License, if you want to permit reuse under its terms.
