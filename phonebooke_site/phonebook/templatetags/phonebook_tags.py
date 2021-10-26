# python 3.9 (name dev: 3BEPb)
# задаем пользовательские теги

from django import template  # импорт модуля работы с библиотекой template
from django.db.models import Count, F  # импорт модуля подсчета значений и фильтрации
from phonebook.models import *  # импорт всех классов из файла .models

register = template.Library()

@register.simple_tag()  # указываем простой декоратор взятия списка всех воинских частей (simple_tag) и присваеваем ему имя
def get_units():   # задаем пользовательский тег
    # return MilitaryUnit.objects.all()  # отображает список всех воинских частей
    return MilitaryUnit.objects.annotate(cnt=Count('phonenumber')).filter(cnt__gt=0)  # отображает только в\ч в которых есть записи

@register.simple_tag()  # указываем простой декоратор (simple_tag) и присваеваем ему имя
def get_division():   # задаем пользовательский тег
    return Division.objects.all()


@register.inclusion_tag('phonebook/list_divisions.html')  # указываем встроенный декоратор
def show_divisions():  # задаем пользовательский тег отобразить подразделения
    # divisions = Division.objects.all()  # загружает полный список таблицы divisions
    # divisions = Division.objects.annotate(cnt=Count('phonenumber')).filter(cnt__gt=0) #загружаем не пустые списки
    #divisions = Division.objects.annotate(cnt=Count('phonenumber', filter=F('phonenumber__is_published'))).filter(cnt__gt=0).filter(phonenumber__military_unit_id=1)
    # divisions = Division.objects.filter('phonenumber__military_unit_id')
    divisions = Division.objects.annotate(cnt=Count('phonenumber', filter=F('phonenumber__is_published'))).filter(
        cnt__gt=0)
    return {"divisions": divisions, }

@register.inclusion_tag('phonebook/list_content.html')  # указываем встроенный декоратор
def show_all():  # задаем пользовательский тег
    phonebooks = Phonenumber.objects.all()
    divisions = Division.objects.all()
    units = MilitaryUnit.objects.all()
    line = Phonenumber.objects.filter(id=8)
    return {"phonebooks": phonebooks, "divisions": divisions, "units": units, "line": line}

