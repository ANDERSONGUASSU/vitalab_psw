# Generated by Django 4.2.5 on 2023-10-07 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TypesExams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type_exam', models.CharField(choices=[('I', 'Exame de imagem'), ('S', 'Exame de sangue')], max_length=1)),
                ('price', models.FloatField()),
                ('available', models.BooleanField(default=True)),
                ('start_time', models.IntegerField()),
                ('end_time', models.IntegerField()),
            ],
        ),
    ]