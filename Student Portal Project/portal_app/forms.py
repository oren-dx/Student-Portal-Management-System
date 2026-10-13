from django import forms
from portal_app.models import *
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2','role']

class StudentListForm(forms.ModelForm):
    class Meta:
        model = StudentModel
        fields = '__all__'
        exclude = ['user']
        
        
class StudentResultForm(forms.ModelForm):
    class Meta:
        model = ResultModel
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-select',
            }),
            'semester': forms.Select(attrs={
                'class': 'form-select',
            }),
            'subject_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter subject name',
            }),
            'marks_obtained': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Enter obtained marks',
            }),
            'total_marks': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Enter total marks',
            }),
            'grade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter grade',
            }),
            'gpa': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Enter GPA',
            }),
            'exam_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter exam year',
            }),
        }
        


class StudentFeeForm(forms.ModelForm):
    class Meta:
        model = FeeModel
        fields = '__all__'
        exclude = ['user','created_at']
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-select',
            }),
            'fee_type': forms.Select(attrs={
                'class': 'form-select',
            }),
            'semester': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Example: 1st',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter fee description',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': 'Enter fee amount',
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }

        
    def clean_amount(self):
        amount = self.cleaned_data['amount']

        if amount <= 0:
            raise forms.ValidationError(
                'Fee amount must be greater than zero.'
            )
        return amount
    
    
class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeePaymentModel
        fields = '__all__'
        exclude = ['user','student','transaction_id']
        widgets = {
            'fee': forms.Select(attrs={
                'class': 'form-select',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': 'Enter payment amount',
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-select',
            }),
            'transaction_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter transaction ID (optional)',
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['fee'].queryset = (
            FeeModel.objects.select_related('student').all()
        )
        
    def clean_amount(self):
        amount = self.cleaned_data['amount']

        if amount <= 0:
            raise forms.ValidationError(
                'Payment amount must be greater than zero.'
            )
        return amount


