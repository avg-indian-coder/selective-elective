from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from . import models
from . import helpers
from django.db import connection

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST['SRN']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "There was an error logging in")
            return redirect('home') 
    else:
        return render(request, 'login.html', {})

def dashboard(request):
    try:
        if request.user.is_authenticated:
            electives_data_1 = helpers.dashboard_context(elective=1)
            electives_data_2 = helpers.dashboard_context(elective=2)
            #print(request.user.username)
            with connection.cursor() as cursor:
                cursor.execute(f'''
                    select * from website_Student
                    where SRN='{request.user.username}'
                ''')
                student_data = cursor.fetchone()
            student_data = models.Student.objects.get(SRN=request.user)
            context = {
                'student': student_data,
                'elective1': electives_data_1,
                'elective2': electives_data_2
            }
            return render(request, 'home.html', context)
        else:
            return redirect('home')
    except Exception as e:
        print(e)
        return redirect('logout')

def store(request):
    if request.method == "POST":
        E1 = request.POST['E1']
        E2 = request.POST['E2']
        e1_e, e1_f = E1.split('_')
        e2_e, e2_f = E2.split('_')
        if (e1_e == '%'):
            messages.error(request, "Choose a subject for elective 1")
            return redirect("dashboard")
        elif (e2_e == '%'):
            messages.error(request, "Choose a subject for elective 2")
            return redirect("dashboard")
        e1_e, e1_f, e2_e, e2_f = int(e1_e), int(e1_f), int(e2_e), int(e2_f)
        with connection.cursor() as cursor:
            cursor.execute(f"select * from website_ElectiveTeachingFaculty as ef where ef.E_id_id={e1_e} and ef.F_id_id={e1_f}")
            ef1 = cursor.fetchall()
            cursor.execute(f"select * from website_ElectiveTeachingFaculty as ef where ef.E_id_id={e2_e} and ef.F_id_id={e2_f}")
            ef2 = cursor.fetchall()
            cursor.execute(f"select * from website_Student where website_Student.SRN='{request.user}'")
            student = cursor.fetchall()
        print(ef1, ef2, student)
        ef1 = models.ElectiveTeachingFaculty.objects.get(E_id=e1_e, F_id=e1_f)
        ef2 = models.ElectiveTeachingFaculty.objects.get(E_id=e2_e, F_id=e2_f)
        student = models.Student.objects.get(SRN=request.user)
        helpers.update_EF_db(student)
        ef1.student_no += 1
        ef2.student_no += 1
        student.EF1 = ef1
        student.EF2 = ef2
        messages.success(request, "Saved electives!")
        ef1.save()
        ef2.save()
        student.save()
    
    return redirect('dashboard')

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("home")

def register_user(request):
    if request.method == 'POST':
        SRN = request.POST['SRN']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        GPA = request.POST['GPA']
        password = request.POST['password']
        c_password = request.POST['confirmPassword']

        if not helpers.check_SRN(SRN):
            messages.error(request, "Incorrect SRN format")
            return redirect('register')
        
        try:
            GPA = float(GPA)
        except:
            messages.error(request, "Enter valid GPA")
            return redirect('register')
        
        count_spec = 0
        for i in password:
            if not i.isalpha():
                count_spec += 1
        with connection.cursor() as cursor:
            cursor.execute(f"select * from auth_user as u where u.username='{SRN}'")
            user = cursor.fetchall()
        if User.objects.filter(username=SRN).exists() or len(user) > 0:
            messages.error(request, "User already exists")
            return redirect('register')
        elif password != c_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')
        elif len(password) < 8:
            messages.error(request, "Password is too short")
            return redirect('register')
        elif count_spec < 2:
            messages.error(request, "Add more special characters")
            return redirect('register')
        elif GPA > 10 or GPA < 0:
            messages.error(request, "Enter valid GPA")
            return redirect('register')
        else:
            messages.success(request, "Successfully signed up! Log in now")
            user = User.objects.create_user(SRN, password=password)
            student = models.Student(SRN=SRN, first_name=first_name, last_name=last_name, GPA=GPA)
            user.save()
            student.save()
            print("Details saved!!!")
            return redirect('home')
        
    return render(request, 'signup.html', {})

def clear(request):
    if request.method == 'POST':
        student = models.Student.objects.get(SRN=request.user)
        student.EF1 = None
        student.EF2 = None
        student.save()
        return redirect('dashboard')

def reset_db(request):
    helpers.init_db()
    return redirect('home')