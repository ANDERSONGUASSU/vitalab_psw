from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TypesExams, MedicalTestInquiries, ExaminationOrders
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants


@login_required
def medical_test_inquiries(request):
    types_exams = TypesExams.objects.all()

    if request.method == "GET":
        return render(request, 'medical_test_inquiries.html',
                      {'types_exams': types_exams})
    elif request.method == "POST":
        exams_id = request.POST.getlist('exams')
        exams_inquiries = TypesExams.objects.filter(id__in=exams_id)

        total_price = 0
        for i in exams_inquiries:
            if i.available:
                total_price += i.price
        date = datetime.now()

        return render(request, 'medical_test_inquiries.html',
                      {'types_exams': types_exams,
                       'exams_inquiries': exams_inquiries,
                       'total_price': total_price,
                       'date': date,
                       })


@login_required
def close_order(request):
    exams_id = request.POST.getlist('exams')
    exams_inquiries = TypesExams.objects.filter(id__in=exams_id)

    exam_order = ExaminationOrders(
        user=request.user,
        date=datetime.now()
    )

    exam_order.save()

    for exam in exams_inquiries:
        exams_inquiries_temp = MedicalTestInquiries(
            user=request.user,
            exam=exam,
            status="E"
        )
        exams_inquiries_temp.save()
        exam_order.exams.add(exams_inquiries_temp)

    exam_order.save()

    messages.add_message(request, constants.SUCCESS,
                         'Pedido de exame concluído com sucesso!')
    return redirect('/exams/manage_orders/')


@login_required
def manage_orders(request):
    exams_orders = ExaminationOrders.objects.filter(user=request.user)
    return render(request, 'manage_orders.html',
                  {'exams_orders': exams_orders})


@login_required
def cancel_orders(request, order_id):
    order = ExaminationOrders.objects.get(id=order_id)
    if order.user == request.user:
        messages.add_message(request, constants.ERROR,
                             'Esse pedido não é seu!')
        return redirect('/exams/manage_orders/')

    order.scheduled = False
    order.save()
    messages.add_message(request, constants.SUCCESS,
                         'Pedido de exame cancelado com sucesso!')
    return redirect('/exams/manage_orders/')


@login_required
def manage_exams(request):
    exams = MedicalTestInquiries.objects.filter(user=request.user)
    return render(request, 'manage_exams.html', {'exams': exams})


@login_required
def allow_opening_exam(request, exam_id):
    exam = MedicalTestInquiries.objects.get(id=exam_id)
    if not exam.requires_password:
        # todo: verificar se tem o PDF do resultado
        return redirect(exam.result.url)
    return redirect(f'/exams/request_exam_passoword/{exam_id}')


@login_required
def request_exam_passoword(request, exam_id):
    exam = MedicalTestInquiries.objects.get(id=exam_id)
    if request.method == "GET":
        return render(request, 'request_exam_passoword.html', {'exam': exam})
    elif request.method == "POST":
        password = request.POST.get("password")
        # TODo: validar se o exame é do usuário
        if password == exam.password:
            return redirect(exam.result.url)
        else:
            messages.add_message(request, constants.ERROR, 'Senha inválida')
            return redirect(f'/exams/request_exam_passoword/{exam.id}')
