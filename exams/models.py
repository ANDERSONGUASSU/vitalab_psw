from django.db import models
from django.contrib.auth.models import User


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
    paasword = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return f'{self.user} | {self.exam.name}'


class ExaminationOrders(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exams = models.ManyToManyField(MedicalTestInquiries)
    scheduled = models.BooleanField(default=True)
    date = models.DateField()

    def __str__(self):
        return f'{self.user} | {self.date}'
