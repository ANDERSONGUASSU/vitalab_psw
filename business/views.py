from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.functions import Concat
from django.contrib.admin.views.decorators import staff_member_required
from exams.models import MedicalTestInquiries
from django.http import FileResponse
from .utils import generate_exam_pdf, generate_random_password
from django.contrib import messages
from django.contrib.messages import constants


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


@staff_member_required
def generate_password(request, exam_id):
    exam = MedicalTestInquiries.objects.get(id=exam_id)

    if exam.password:
        # Download the document of the existing password
        return FileResponse(generate_exam_pdf(
            exam.exam.name, exam.user, exam.password), filename="token.pdf")

    password = generate_random_password(9)
    exam.password = password
    exam.save()
    return FileResponse(generate_exam_pdf(
        exam.exam.name, exam.user, exam.password), filename="token.pdf")


@staff_member_required
def update_exam_data(request, exam_id):
    exam = MedicalTestInquiries.objects.get(id=exam_id)

    pdf = request.FILES.get('result')
    status = request.POST.get('status')
    requires_password = request.POST.get('requires_password')

    if requires_password and (not exam.password):
        messages.add_message(
            request, constants.ERROR,
            'Para exigir uma senha, primeiro crie uma.')
        return redirect(f'/business/exam_client/{exam_id}')

    exam.requires_password = True if requires_password else False

    if pdf:
        exam.result = pdf

    exam.status = status
    exam.save()
    messages.add_message(
        request, constants.SUCCESS, 'Change made successfully')
    return redirect(f'/business/exam_client/{exam_id}')
