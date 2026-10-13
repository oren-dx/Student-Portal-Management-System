from django.shortcuts import render ,redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from portal_app.models import*
from portal_app.forms import*


def register_view(request):
    form_data = RegisterForm()
    if request.method == 'POST':
        form_data = RegisterForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            messages.success(request, 'User created successfully')
            return redirect('login_view')
        else:
            messages.warning(request,'User Already Exists')
            form_data = RegisterForm()

    context = {
        'form_data' : form_data
    }
    return render(request, 'auth/register.html', context)


def login_view(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        password = request.POST.get('password')

        try:
            user_data = UserModel.objects.get(username = text)
        except UserModel.DoesNotExist:
            user_data = UserModel.objects.get(email = text)

        print(user_data)

        if user_data:
            user = authenticate(request, username = user_data.username, password = password)

            if user:
                login(request, user)
                messages.success(request, 'User login successfully')
                return redirect('dashboard')
    return render(request, 'auth/login.html')


def logout_view(request):
    messages.success(request,'User logout successfully')
    logout(request)
    return redirect('login_view')


@login_required
def dashboard(request):
    students = StudentModel.objects.all()

    context = {
        'students': students,
        'total_students': students.count(),
        'bba_students': students.filter(department='BBA').count(),
        'cse_students': students.filter(department='CSE').count(),
        'eee_students': students.filter(department='EEE').count(),
    }

    return render(request, 'pages/dashboard.html', context)

@login_required
def student_list(request):
    # Admin can see all student profiles
    if request.user.role == 'Admin':
        students = StudentModel.objects.select_related(
            'user'
        ).all()

    # Student can view the list but cannot manage other profiles
    else:
        students = StudentModel.objects.select_related(
            'user'
        ).all()

    context = {
        'students': students
    }
    return render(request, 'pages/student_list.html', context)


@login_required
def student_detail(request, s_id):
    student = get_object_or_404(StudentModel, id=s_id)

    # Student can view only their own profile
    if request.user.role != 'Admin' and student.user_id != request.user.id:
        messages.error(request, 'You cannot view another student profile.')
        return redirect('student_list')

    context = {
        'student': student
    }
    return render(request, 'pages/student_detail.html', context)


@login_required
def student_create(request):
    # A student can create only one profile
    if request.user.role == 'Student':
        if StudentModel.objects.filter(user=request.user).exists():
            messages.info(request, 'You have already created your profile.')
            return redirect('student_detail', s_id=request.user.student_profile.id)

    form = StudentListForm(request.POST or None, request.FILES or None)

    # Students must not choose another user's account
    if request.user.role != 'Admin':
        form.fields.pop('user', None)

    if request.method == 'POST' and form.is_valid():
        student = form.save(commit=False)

        if request.user.role == 'Student':
            student.user = request.user
        else:
            if not hasattr(student, 'user') or student.user_id is None:
                form.add_error('user', 'Please select a student account.')
                return render(
                    request,
                    'pages/student_create.html',
                    {'form': form}
                )

            if student.user.role != 'Student':
                form.add_error('user', 'Select a Student account.')
                return render(
                    request,
                    'pages/student_create.html',
                    {'form': form}
                )

        student.save()

        messages.success(request, 'Student profile created successfully!')
        return redirect('student_list')

    context = {
        'form': form
    }

    return render(request, 'pages/student_create.html', context)



@login_required
def student_update(request, s_id):
    student = get_object_or_404(StudentModel, id=s_id)

    # Students can update only their own profile
    if request.user.role != 'Admin' and student.user_id != request.user.id:
        messages.error(request, 'You cannot update another student profile.')
        return redirect('student_list')

    form = StudentListForm(
        request.POST or None,
        request.FILES or None,
        instance=student
    )

    # Prevent students from changing the profile owner
    if request.user.role != 'Admin':
        form.fields.pop('user', None)

    if request.method == 'POST' and form.is_valid():
        updated_student = form.save(commit=False)

        if request.user.role != 'Admin':
            updated_student.user = request.user
        elif updated_student.user.role != 'Student':
            form.add_error('user', 'Select a Student account.')
            return render(
                request,
                'pages/student_update.html',
                {'form': form, 'student': student}
            )

        updated_student.save()

        messages.success(request, 'Student profile updated successfully!')
        return redirect('student_list')

    context = {
        'form': form,
        'student': student
    }

    return render(request, 'pages/student_update.html', context)


@login_required
def student_delete(request, s_id):
    # Only Admin can delete student profiles
    if request.user.role != 'Admin':
        messages.error(request, 'Only Admin can delete student profiles.')
        return redirect('student_list')

    student = get_object_or_404(StudentModel, id=s_id)
    student.delete()

    messages.success(request, 'Student profile deleted successfully!')
    return redirect('student_list')


@login_required
def result_list(request):
    if request.user.role == 'Admin':
        results = ResultModel.objects.select_related(
            'student', 'user'
        ).all()
    else:
        results = ResultModel.objects.filter(
            user=request.user,
            student__user=request.user
        )
        
    context ={
        'results': results
    }

    return render(request,'pages/result_list.html',context)


@login_required
def result_create(request):
    if request.user.role != 'Admin':
        return redirect('result_list')

    form = StudentResultForm(request.POST or None)

    if form.is_valid():
        result = form.save(commit=False)
        result.user = result.student.user
        result.save()

        messages.success(request, 'Result added successfully.')
        return redirect('result_list')
    
    context ={
        'form': form 
    }

    return render(request,'pages/result_create.html',context)

@login_required
def result_update(request, r_id):
    if request.user.role != 'Admin':
        messages.error(request, 'You are not authorized to update results.')
        return redirect('result_list')

    result = get_object_or_404(ResultModel, id=r_id)

    if request.method == 'POST':
        form = StudentResultForm(request.POST, instance=result)

        if form.is_valid():
            form.save()
            messages.success(request, 'Student result updated successfully.')
            return redirect('result_list')
    else:
        form = StudentResultForm(instance=result)

    context = {
        'form': form,
        'result': result,
    }

    return render(request, 'pages/result_update.html', context)

def result_delete(request,r_id):
    result = ResultModel.objects.get(id =r_id).delete()
    return redirect('result_list')




@login_required
def fee_list(request):
    if request.user.role == 'Admin':
        fees = FeeModel.objects.select_related(
            'student', 'user'
        ).order_by('-id')
    else:
        student = FeeModel.objects.none()

        fees = FeeModel.objects.filter(
            user=request.user,
            student__user=request.user
        ).select_related('student').order_by('-id')

    context = {
        'fees': fees,
    }
    return render(request, 'pages/fee_list.html', context)


@login_required
def fee_create(request):
    if request.user.role != 'Admin':
        return redirect('fee_list')

    form = StudentFeeForm(request.POST or None)

    if form.is_valid():
        fee = form.save(commit=False)
        fee.user = fee.student.user
        fee.save()

        messages.success(request, 'Fee added successfully.')
        return redirect('fee_list')
    
    context ={
        'form': form
    }
    return render(request,'pages/fee_create.html',context)

@login_required
def fee_update(request, f_id):
    if request.user.role != 'Admin':
        messages.error(request, 'You are not authorized to update fees.')
        return redirect('fee_list')

    fee = get_object_or_404(FeeModel, id=f_id)

    if request.method == 'POST':
        form = StudentFeeForm(request.POST, instance=fee)

        if form.is_valid():
            form.save()
            messages.success(request, 'Fee updated successfully.')
            return redirect('fee_list')
    else:
        form = StudentFeeForm(instance=fee)

    context = {
        'form': form,
        'fee': fee,
    }

    return render(request, 'pages/fee_update.html', context)

    
@login_required
def payment_list(request):
    if request.user.role == 'Admin':
        payments = FeePaymentModel.objects.select_related(
            'student', 'fee', 'user'
        ).order_by('-payment_date', '-id')

    else:
        payments = FeePaymentModel.objects.filter(
            student__user=request.user
        ).select_related(
            'student', 'fee', 'user'
        ).order_by('-payment_date', '-id')

    context = {
        'payments': payments,
    }
    return render(request, 'pages/payment_list.html', context)


@login_required
def payment_create(request):
    if request.user.role != 'Student':
        messages.error(
            request,
            'Admin cannot make payments.'
        )
        return redirect('payment_list')

    form = FeePaymentForm(request.POST or None)

    # Students can only pay their own fees
    form.fields['fee'].queryset = FeeModel.objects.filter(
        student__user=request.user
    )

    if form.is_valid():
        payment = form.save(commit=False)

        payment.student = payment.fee.student
        payment.user = request.user

        if payment.amount <= 0:
            form.add_error(
                'amount',
                'Payment amount must be greater than zero.'
            )

        elif payment.amount > payment.fee.due_amount:
            form.add_error(
                'amount',
                'Payment cannot exceed the outstanding fee.'
            )

        else:
            payment.save()
            messages.success(request,'Payment recorded successfully.')
            return redirect('payment_list')

    context = {
        'form': form
    }

    return render(request,'pages/payment_create.html',context)


