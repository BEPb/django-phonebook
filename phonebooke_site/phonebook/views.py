# python 3.9 (name dev: 3BEPb)
# views.py - контроллер приложения

from django.shortcuts import render
# Create your views here.

from django.http import HttpResponse  # работа с ответами
from .models import Phonenumber, Division, MilitaryUnit  # из текущей дирректории, файла models импортируем класс Phonenumber

def index(request):  # создаем функцию обрабатывающую запрос index
    # phonebook = Phonenumber.objects.order_by('-create_at')   # отображение в обратном порядке по дате создания записи
    phonebooks = Phonenumber.objects.all()  # отображение всего списка (порядок отображения указан в админке)
    line = Phonenumber.objects.filter(id=8)
    # divisions = Division.objects.all() - унифицируем вместо него используем пользовательский тег
    units = MilitaryUnit.objects.all()
    context = {
        'title': 'Телефонная книга',  # задаем переменную (подпись страницы)
        'phonebooks': phonebooks,
        #'divisions': divisions, - унифицируем вместо него используем пользовательский тег
        'units': units,
        'line': line
    }
    return render(request, template_name='phonebook/index.html', context=context)  # ответ - заполненный шаблон
    # request - работа с запросами
    # template_name='phonebook/online_indx.html' - папка нахождения шаблона
    # context = context  - заполнение шаблона данными из переменной context

def mil_unit(request, mil_id):  # создаем функцию обрабатывающую запрос index
    # phonebooks = Phonenumber.objects.all()  # отображение всего списка (порядок отображения указан в админке)
    phonebooks = Phonenumber.objects.filter(military_unit_id=mil_id)  # отображение отфильтрованного списка (порядок отображения указан в админке)
    # divisions = Division.objects.all() - унифицируем вместо него используем пользовательский тег
    units = MilitaryUnit.objects.all()
    unit = MilitaryUnit.objects.get(pk=mil_id)
    line = Phonenumber.objects.filter(id=8)

    # формируем передоваемые данные на страницу
    context = {
        'title': 'Телефонная книга в\ч',  # задаем переменную (подпись страницы)
        'phonebooks': phonebooks,  # отфильтрованный список
        # 'divisions': divisions, - унифицируем вместо него используем пользовательский тег
        'units': units,
        'unit': unit,
        'line': line
    }
    return render(request, template_name='phonebook/mil_unit.html', context=context)  # ответ - заполненный шаблон
    # request - работа с запросами
    # template_name='phonebook/mil_unit.html' - папка нахождения шаблона
    # context = context  - заполнение шаблона данными из переменной context

def division(request, div_id):  # создаем функцию обрабатывающую запрос index
    # phonebooks = Phonenumber.objects.all()  # отображение всего списка (порядок отображения указан в админке)
    phonebooks = Phonenumber.objects.filter(division_id=div_id)  # отображение отфильтрованного списка (порядок отображения указан в админке)
    # division = Division.objects.filter(pk=division_id)
    # divisions = Division.objects.all() - унифицируем вместо него используем пользовательский тег
    units = MilitaryUnit.objects.all()
    line = Phonenumber.objects.filter(id=8)

    context = {
        'title': 'Подразделение',  # задаем переменную (подпись страницы)
        'phonebooks': phonebooks,  # отфильтрованный список
        # 'divisions': divisions, - унифицируем вместо него используем пользовательский тег
        'units': units,
        'line': line
    }
    return render(request, template_name='phonebook/division.html', context=context)  # ответ - заполненный шаблон
    # request - работа с запросами
    # template_name='phonebook/division.html' - папка нахождения шаблона
    # context = context  - заполнение шаблона данными из переменной context

def user_data(request, user_id):  # создаем функцию обрабатывающую запрос index
    # phonebook = Phonenumber.objects.filter()  # отображение всего списка (порядок отображения указан в админке)
    phonebooks = Phonenumber.objects.filter(id=user_id)  # отображение отфильтрованного списка
    # divisions = Division.objects.all() - унифицируем вместо него используем пользовательский тег
    units = MilitaryUnit.objects.all()
    line = Phonenumber.objects.filter(id=8)

    context = {
        'title': 'Данные пользователя',  # задаем переменную (подпись страницы)
        'phonebooks': phonebooks,
        # 'divisions': divisions, - унифицируем вместо него используем пользовательский тег
        'units': units,
        'line': line
    }
    return render(request, template_name='phonebook/user_data.html', context=context)  # ответ - заполненный шаблон
    # request - работа с запросами
    # template_name='phonebook/online_indx.html' - папка нахождения шаблона
    # context = context  - заполнение шаблона данными из переменной context

def test_list(request):  # создаем функцию обрабатывающую запрос index
    phonebook = Phonenumber.objects.all()  # отображение всего списка (порядок отображения указан в админке)
    context = {
        'phonebook': phonebook,
        'title': 'Список телефонных номеров'
    }
    return render(request, template_name='phonebook/test_list.html', context=context)  # ответ - заполненный шаблон
    # request - работа с запросами
    # template_name='phonebook/online_indx.html' - папка нахождения шаблона
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
