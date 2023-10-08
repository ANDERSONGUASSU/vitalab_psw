from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from secrets import token_urlsafe
from django.utils import timezone
from datetime import timedelta


class TypesExams(models.Model):
    name = models.CharField(max_length=50)
    type_exam_choices = (
        ('I', 'Exame de imagem'),
        ('S', 'Exame de sangue'),
    )
    type_exam = models.CharField(max_length=1, choices=type_exam_choices)
    price = models.FloatField()
    available = models.BooleanField(default=True)
    start_time = models.IntegerField()
    end_time = models.IntegerField()

    def __str__(self):
        return self.name


class MedicalTestInquiries(models.Model):
    choice_status = (
        ('E', 'Em análise'),
        ('F', 'Finalizado')
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exam = models.ForeignKey(TypesExams, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=2, choices=choice_status)
    result = models.FileField(upload_to="results", null=True, blank=True)
    requires_password = models.BooleanField(default=False)
    password = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return f'{self.user} | {self.exam.name}'

    def badge_template(self):
        if self.status == "E":
            classes = 'bg-warning text-dark'
            text = "Em análise"
        elif self.status == "F":
            classes = 'bg-success'
            text = "Finalizado"

        return mark_safe(f'<span class= "badge {classes}">{text}</span>')


class ExaminationOrders(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exams = models.ManyToManyField(MedicalTestInquiries)
    scheduled = models.BooleanField(default=True)
    date = models.DateField()

    def __str__(self):
        return f'{self.user} | {self.date}'


class MedicalAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    identification = models.CharField(max_length=50)
    access_time = models.IntegerField()
    created_at = models.DateTimeField()
    initial_exam_date = models.DateField()
    final_exam_date = models.DateField()
    token = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.token

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = token_urlsafe(6)

        super(MedicalAccess, self).save(*args, **kwargs)

    @property
    def status(self):
        return 'Expirado' if timezone.now() > (self.created_at + timedelta(
            hours=self.access_time)) else 'Ativo'

    @property
    def link(self):
        # TODo: reverse
        return f'http://127.0.0.1:8000/exams/medical_access/{self.token}'
