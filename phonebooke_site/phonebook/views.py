# python 3.9 (name dev: 3BEPb)
# views.py - контроллер приложения

from django.shortcuts import render
# Create your views here.

from django.http import HttpResponse  # работа с ответами
from .models import Phonenumber  # из текущей дирректории, файла models импортируем класс Phonenumber

def index(request):  # создаем функцию обрабатывающую запрос index
    # phonebook = Phonenumber.objects.order_by('-create_at')   # отображение в обратном порядке по дате создания записи
    phonebook = Phonenumber.objects.all()  # отображение всего списка (порядок отображения указан в админке)
    context = {
        'phonebook': phonebook,
        'title': 'Список телефонных номеров'
    }
    return render(request, template_name='phonebook/index.html', context=context)  # ответ - заполненный шаблон
    # request - работа с запросами
    # template_name='phonebook/index.html' - папка нахождения шаблона
    # context = context  - заполнение шаблона данными из переменной context

def test_list(request):  # создаем функцию обрабатывающую запрос index
    phonebook = Phonenumber.objects.all()  # отображение всего списка (порядок отображения указан в админке)
    context = {
        'phonebook': phonebook,
        'title': 'Список телефонных номеров'
    }
    return render(request, template_name='phonebook/test_list.html', context=context)  # ответ - заполненный шаблон
    # request - работа с запросами
    # template_name='phonebook/index.html' - папка нахождения шаблона
    # context = context  - заполнение шаблона данными из переменной context

def test(request):  # создаем функцию обрабатывающую запрос test
    print(request)
    numbers = Phonenumber.objects.all()  # создадим переменную в которую поместим все данные класса Phonenumber
    res = '<h1>СПРАВОЧНИК</h1>'
    for item in numbers:
        res += f'<div><p>{item.subdivision}</p><p>{item.position}{item.oficial_telephone}</p></div>\n<hr>\n'
        # f -  форматированная строка
        # <div> -  блок
        # <p> - параграф
        # <hr> - горизонтальная линия
        # \n - перенос на новую строку
    return HttpResponse(res)
