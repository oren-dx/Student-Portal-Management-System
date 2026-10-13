from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class UserModel(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Student', 'Student'),
    ]
    role = models.CharField(max_length=10,choices=ROLE_CHOICES,default='Student')

    pass

    def __str__(self):
        return f'{self.username}'
    

class StudentModel(models.Model):
    DEPT_TYPES = [
        ('BBA', 'BBA'),
        ('CSE', 'CSE'),
        ('EEE', 'EEE'),
    ]
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='media/student_images',null=True,blank=True)
    department = models.CharField(choices=DEPT_TYPES,max_length=20,null=True,blank=True)

    def __str__(self):
        return self.name or self.user.username


class ResultModel(models.Model):
    SEMESTER_CHOICES = [
        ('1st', '1st Semester'),
        ('2nd', '2nd Semester'),
        ('3rd', '3rd Semester'),
        ('4th', '4th Semester'),
        ('5th', '5th Semester'),
        ('6th', '6th Semester'),
        ('7th', '7th Semester'),
        ('8th', '8th Semester'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='results'
    )
    student = models.ForeignKey(
        StudentModel,
        on_delete=models.CASCADE,
        related_name='results',
        null=True
    )
    semester = models.CharField(
        max_length=10,
        choices=SEMESTER_CHOICES,
        null=True
    )
    subject_name = models.CharField(max_length=100,null=True)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, default=100,null=True)
    grade = models.CharField(max_length=5, null=True, blank=True)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    exam_year = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f'{self.student.name} - {self.subject_name}'


class FeeModel(models.Model):
    FEE_TYPES = [
        ('Tuition', 'Tuition Fee'),
        ('Semester', 'Semester Fee'),
        ('Other', 'Other Fee'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_fees'
    )
    student = models.ForeignKey(
        StudentModel,
        on_delete=models.CASCADE,
        related_name='fees'
    )
    fee_type = models.CharField(
        max_length=20,
        choices=FEE_TYPES,
        null=True
    )
    semester = models.CharField(max_length=10,null=True)
    description = models.CharField(max_length=200,null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.name} - {self.fee_type}'

    @property
    def paid_amount(self):
        return self.payments.aggregate(
            total=models.Sum('amount')
        )['total'] or 0

    @property
    def due_amount(self):
        return self.amount - self.paid_amount


class FeePaymentModel(models.Model):
    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('Bank', 'Bank Transfer'),
        ('Mobile Banking', 'Mobile Banking'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='fee_payments'
    )
    student = models.ForeignKey(
        StudentModel,
        on_delete=models.CASCADE,
        related_name='fee_payments'
    )
    fee = models.ForeignKey(
        FeeModel,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    payment_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(choices=PAYMENT_METHODS,max_length=20,null=True)
    transaction_id = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return f'{self.student.name} - {self.amount}'
