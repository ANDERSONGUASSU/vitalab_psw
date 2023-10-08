from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.functions import Concat
from django.contrib.admin.views.decorators import staff_member_required
from exams.models import MedicalTestInquiries
from django.http import FileResponse


@staff_member_required
def manage_clients(request):
    clients = User.objects.filter(is_staff=False)

    full_name = request.GET.get('full_name')
    email = request.GET.get('email')

    if email:
        clients = clients.filter(email__contains=email)
    if full_name:
        clients = clients.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name')
        ).filter(full_name__contains=full_name)

    return render(request, 'manage_clients.html',
                  {'clients': clients, 'full_name': full_name, 'email': email})


@staff_member_required
def client(request, client_id):
    client = User.objects.get(id=client_id)
    exams = MedicalTestInquiries.objects.filter(user=client)
    return render(request, 'client.html', {'client': client, 'exams': exams})


@staff_member_required
def exam_client(request, exam_id):
    exam = MedicalTestInquiries.objects.get(id=exam_id)
    return render(request, 'exam_client.html', {'exam': exam})


@staff_member_required
def proxy_pdf(request, exam_id):
    exam = MedicalTestInquiries.objects.get(id=exam_id)

    response = exam.result.open()
    return FileResponse(response)
