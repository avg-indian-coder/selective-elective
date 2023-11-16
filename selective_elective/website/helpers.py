from . import models
import re

def dashboard_context(elective):
    EF = models.ElectiveTeachingFaculty.objects.all()
    #print(EF)
    context = []

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
    students = models.Student.objects.all()
    for student in students:
        if student.EF1:
            student.EF1.student_no += 1
            student.EF1.save()
        if student.EF2:
            student.EF2.student_no += 1
            student.EF2.save()

    
