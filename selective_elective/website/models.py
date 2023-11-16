from django.db import models

# Create your models here.
class Elective(models.Model):
    E_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    types = models.IntegerChoices("types", "E1 E2")
    E_type = models.IntegerField(choices=types.choices)

class Faculty(models.Model):
    F_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)

class Room(models.Model):
    room_no = models.CharField(primary_key=True, max_length=10)
    floor = models.IntegerField()
    capacity = models.IntegerField()
    
class ElectiveTeachingFaculty(models.Model):
    F_id = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    E_id = models.ForeignKey(Elective, on_delete=models.CASCADE)
    room_no = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True)
    student_no = models.IntegerField(default=0)

class Student(models.Model):
    SRN = models.CharField(max_length=30, primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True)
    GPA = models.DecimalField(max_digits=4, decimal_places=2)
    EF1 = models.ForeignKey(ElectiveTeachingFaculty, on_delete=models.CASCADE, blank=True, null=True, related_name='E1')
    EF2 = models.ForeignKey(ElectiveTeachingFaculty, on_delete=models.CASCADE, blank=True, null=True, related_name='E2')
