from . import models
import re
from django.db import connection

def dashboard_context(elective):
    with connection.cursor() as cursor:
        cursor.execute("select * from website_ElectiveTeachingFaculty")
        EF = cursor.fetchall()
    #print(EF)
    EF = models.ElectiveTeachingFaculty.objects.all()
    context = []

    # you want EFs where elective is that only
    for ef in EF:
        if ef.E_id.E_type == elective:
            c = {
                'E_id': ef.E_id.E_id,
                'F_id': ef.F_id.F_id,
                'E_name': ef.E_id.name,
                'F_fname': ef.F_id.first_name,
                'F_lname': ef.F_id.last_name
            }
            context.append(c)
   
    with connection.cursor() as cursor:
        cursor.execute(f"select * from (select * from website_electiveteachingfaculty as ef where ef.e_id_id={elective}) as efs join website_faculty as f on efs.F_id_id=f.F_id;")
        out = cursor.fetchall()
        #cprint(out)

    context.sort(key=lambda x: x['E_name'])

    return context

def update_EF_db(student):
    if student.EF1:
        student.EF1.student_no -= 1
        student.EF1.save()
    if student.EF2:
        student.EF2.student_no -= 1
        student.EF2.save()

def check_SRN(SRN):
    pattern = re.compile(r'^PES[12]{1}UG\d{2}[A-Z]{2}\d{3}')
    return bool(pattern.match(SRN))

def init_db():
    models.ElectiveTeachingFaculty.objects.update(student_no=0)
    with connection.cursor() as cursor:
        cursor.execute("select * from Student")
        students = cursor.fetchall()
    students = models.Student.objects.all()
    for student in students:
        if student.EF1:
            student.EF1.student_no += 1
            student.EF1.save()
        if student.EF2:
            student.EF2.student_no += 1
            student.EF2.save()

    
