from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from website import models
from django.db.models import Sum
from django.db import connection

# Create your views here.
def a_login(request):
    if request.user.is_authenticated:
        return redirect('administrator:logout')
    
    if request.method == 'POST':
        username = request.POST['SRN']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect("administrator:dashboard")
            else:
                messages.error(request, "There was an error logging in")
                return redirect("administrator:login")
        else:
            messages.error(request, "User does not exist")
            return redirect("administrator:login")
        
    return render(request, "alogin.html", {})

def a_logout(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("administrator:login")

def dashboard(request):
    if request.method == "POST":
        print(request.POST)
        e1 = request.POST["E1"]
        e2 = request.POST["E2"]
        context = {}
        if e1 != "%":
            e1_m = models.ElectiveTeachingFaculty.objects.filter(E_id=e1)
            e1_c = models.ElectiveTeachingFaculty.objects.filter(E_id=e1).aggregate(Sum("student_no"))
            print(e1_c)
            context["e1m"] = e1_m
            context["e1c"] = e1_c
        if e2 != "%":
            e2_m = models.ElectiveTeachingFaculty.objects.filter(E_id=e2)
            e2_c = models.ElectiveTeachingFaculty.objects.filter(E_id=e2).aggregate(Sum("student_no"))
            print(e2_c)
            context["e2m"] = e2_m
            context["e2c"] = e2_c

        with connection.cursor() as cursor:
            cursor.callproc('EmptyClassrooms')
            empty_classrooms = cursor.fetchall()
            empty_classrooms = [room[0] for room in empty_classrooms]
            print(empty_classrooms)

        context["empty"] = empty_classrooms
        context["e1s"] = models.Elective.objects.filter(E_type=1)
        context["e2s"] = models.Elective.objects.filter(E_type=2)
        context["naughty"] = models.Student.objects.filter(EF1=None,EF2=None)
        return render(request, "adashboard.html", context)

    with connection.cursor() as cursor:
        cursor.callproc('EmptyClassrooms')
        empty_classrooms = cursor.fetchall()
        empty_classrooms = [room[0] for room in empty_classrooms]
        print(empty_classrooms)
        #context["empty"] = empty_classrooms

    e1s = models.Elective.objects.filter(E_type=1)
    e2s = models.Elective.objects.filter(E_type=2)
    naughty = models.Student.objects.filter(EF1=None,EF2=None)
    return render(request, "adashboard.html", {"e1s":e1s, "e2s":e2s, "naughty": naughty, "empty": empty_classrooms})

def allocate(request):
    efs = models.ElectiveTeachingFaculty.objects.all().order_by("-student_no")
    rooms = models.Room.objects.all().order_by("floor", "-capacity")

    for ef in efs:
        r = None
        for room in rooms:
            if room.capacity > ef.student_no:
                ef.room_no = room
                ef.save()
                r = room
                break
        if r:
            rooms = rooms.exclude(room_no=r.room_no)

    return redirect("administrator:dashboard")

def naughty(request):
    students = models.Student.objects.all()
    naughty_students = []

    for student in students:
        if not student.EF1:
            naughty_students.append(student)

    request.session["naughty"] = naughty_students

    return redirect("administrator:dashboard")
