from random import choice, shuffle
import string
from django.conf import settings
from django.template.loader import render_to_string
from io import BytesIO
from weasyprint import HTML
import os


def generate_random_password(length):

    special_characters = string.punctuation
    letters = string.ascii_letters
    numbers_list = string.digits

    remainder = 0
    count = length // 3
    if not length % 3 == 0:
        remainder = length - (count * 3)

    letter_part = ''
    for i in range(0, count + remainder):
        letter_part += choice(letters)

    number_part = ''
    for i in range(0, count):
        number_part += choice(numbers_list)

    special_part = ''
    for i in range(0, count):
        special_part += choice(special_characters)

    password = list(letter_part + number_part + special_part)
    shuffle(password)

    return ''.join(password)


def generate_exam_pdf(exam, patient, password):

    template_path = os.path.join(settings.BASE_DIR,
                                 'templates/partials/exam_password.html')
    rendered_template = render_to_string(
        template_path, {'exam': exam,
                        'patient': patient,
                        'password': password})

    output_path = BytesIO()

    HTML(string=rendered_template).write_pdf(output_path)
    output_path.seek(0)

    return output_path
