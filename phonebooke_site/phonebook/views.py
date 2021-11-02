# python 3.9 (name dev: 3BEPb)
# views.py - контроллер приложения (контроллеры-классы и контроллеры-функции)

from django.shortcuts import render, get_object_or_404, redirect  # импорт модуля рендеринга (обработчика), модуля
# обработки отсутсвующих объектов, модуль перенаправления
from django.http import HttpResponse  # работа с ответами
from .models import Phonenumber, Division, MilitaryUnit  # из текущей дирректории, файла models импортируем класс Phonenumber, Division, MilitaryUnit
from .forms import PhoneForm, UserRegisterForm, UserLoginForm, ContactForm  # импортируем модуль заполнения наших форм из .forms
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Count, F  # импорт модуля подсчета значений и фильтрации
# импортируем модуль ListView - просмотра общих данных страницы,
# DetailView - просмотра детальных данных одной записи
# CreateView - создание записи
from django.urls import reverse_lazy  # импортируем модуль построения ленивой ссылки
from .utils import MyMixin  # импортируем созданный миксин из файла utils.py
from django.contrib.auth.mixins import LoginRequiredMixin  # импортируем штатный миксин проверки аутентификации
from django.core.paginator import Paginator  # пагинация страниц
from django.contrib.auth.forms import UserCreationForm  # модуль создания формы регистрации пользователя
from django.contrib import messages  # модуль сообщений
from django.contrib.auth import login, logout  # модуль логирования и выхода
from django.core.mail import send_mail  # модуль отправки сообщений


### Контроллеры-классы

# класс-обработчик главной страницы (переопределяем атрибуты класса ListView)
class HomePhones(MyMixin, ListView):  # наследуем атрибуты от класса ListView и собственный миксин MyMixin
    model = Phonenumber  # привязываем к модели
    template_name = 'phonebook/home_phone_list.html'  # указываем путь размещения нашего шаблона
    context_object_name = 'phonebooks'  # указываем имя передаваемого листа объектов
    allow_empty = False  # пустые списки - ошибка 404 (также защищает от 500 ошибки сервера)
    # extra_context = {'title': 'Главная'}
    # units = MilitaryUnit
    paginate_by = 5  # указываем по сколько записей на странице должно быть

    # функция для создания контекста, передаваемого в загружаемую страницу
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # получаем значения указанные в ключе ссылки  сохраняем в переменную context
        context['title'] = self.get_upper('Главная страница')  # дополняем данными переменную context
        # self.get_upper - миксин каторый преобразует тайтл в верхний регистр
        return context  # передаем результирующую переменную

    def get_queryset(self):  # функция (метод) - фильтр по опубликованным данным
        return Phonenumber.objects.filter(is_published=True).select_related('division', 'military_unit')
    # select_related('division', 'military_unit') - уменьшаем колличество запросов SQL за счет "жадных" запросов

# класс-обработчик страницы данных за в\ч (переопределяем атрибуты класса ListView)
class PhonesByMilitary(ListView):  # наследуем атрибуты от класса ListView
    model = MilitaryUnit  # привязываем к модели
    template_name = 'phonebook/mil_unit.html'  # указываем путь размещения нашего шаблона
    context_object_name = 'military_units'  # указываем имя передаваемого листа объектов
    allow_empty = False  # пустые списки - ошибка 404 (также защищает от 500 ошибки сервера)
    paginate_by = 5  # указываем по сколько записей на странице должно быть

    # функция для создания контекста, передаваемого в загружаемую страницу
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # получаем значения указанные в ключе ссылки
        context['title'] = MilitaryUnit.objects.get(pk=self.kwargs['mil_id'])  # подписываем тайтл именем части, по mil_id - параметра запроса в urls
        context['devi_nub'] = Phonenumber.objects.filter(military_unit_id=self.kwargs['mil_id'], is_published=True).values('division').annotate(the_division=Count('division'))  # выводит сколько и каких подразделений имеется в этой воинской части
        context['number_dev'] = Phonenumber.objects.filter(military_unit_id=self.kwargs['mil_id'], is_published=True).values('division').annotate(the_division=Count('division')).count  # сколько всего отделов в этой воинской части
        context['number_ab'] = Phonenumber.objects.filter(military_unit_id=self.kwargs['mil_id'], is_published=True).count
        return context  # непосредственно передает словарь на страницу

    def get_queryset(self):  # функция (метод) - фильтр по опубликованным данным
        return Phonenumber.objects.filter(military_unit_id=self.kwargs['mil_id'], is_published=True).select_related('division', 'military_unit')
        # return - передает отфильтрованные значения модели Phonenumber
        # military_unit_id -  по ключу заложенного в адресе (URLS) = 'mil_id'
        # is_published=True -  по опубликованным записям
        # mil_id - параметра запроса в urls
        # select_related('division', 'military_unit') - уменьшаем колличество запросов SQL за счет "жадных" запросов

# класс список воинских частей
class HomeMilytary(MyMixin, ListView):  # наследуем атрибуты от класса ListView
    model = MilitaryUnit  # привязываем к модели класс список воинских частей
    template_name = 'phonebook/list_military.html'  # указываем путь размещения нашего шаблона
    context_object_name = 'mill_unts'  # указываем имя передаваемого листа объектов
    allow_empty = False  # пустые списки - ошибка 404 (также защищает от 500 ошибки сервера)
    paginate_by = 7  # указываем по сколько записей на странице должно быть

    # функция для создания контекста, передаваемого в загружаемую страницу
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # получаем значения указанные в ключе ссылки  сохраняем в переменную context
        context['title'] = self.get_upper('Все в\ч')  # дополняем данными переменную context, применяем к ней миксин get_upper
        # self.get_upper - миксин каторый преобразует тайтл в верхний регистр
        return context  # передаем результирующую переменную

    def get_queryset(self):  # функция (метод) - фильтр по опубликованным данным
        return MilitaryUnit.objects.annotate(cnt=Count('phonenumber')).filter(cnt__gt=0)
        # return MilitaryUnit.objects.all()
    # select_related('division', 'military_unit') - уменьшаем колличество запросов SQL за счет "жадных" запросов

# класс-обработчик страницы данных за подразделение (переопределяем атрибуты класса ListView)
class PhonesByDivision(ListView):  # наследуем атрибуты от класса ListView
    model = Division  # привязываем к модели
    template_name = 'phonebook/home_phone_list.html'  # указываем путь размещения нашего шаблона
    context_object_name = 'phonebooks'  # указываем имя передаваемого листа объектов
    allow_empty = False  # пустые списки - ошибка 404 (также защищает от 500 ошибки сервера)
    extra_context = {'mil_id': 1}  # дополнительный контент
    paginate_by = 5  # указываем по сколько записей на странице должно быть

    # функция для создания контекста, передаваемого в загружаемую страницу (для заполнения словаря для использования в качестве контекста шаблона)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # переопределяем контекст, получаем значения указанные в ключе ссылки
        # context['mil_id'] = Division.objects.get(pk=self.kwargs['2'])  # дополняем контекст тайтлом, div_id - параметра запроса в urls
        context['title'] = Division.objects.get(pk=self.kwargs['div_id'])  # подписываем тайтл именем части, по div_id - параметра запроса в urls
        return context  # непосредственно передает словарь на страницу

    def get_queryset(self):  # функция (метод) - фильтр по опубликованным данным, определяет список объектов, которые вы хотите отобразить
        # return Phonenumber.objects.filter(division_id=self.kwargs['div_id'], is_published=True).select_related('division', 'military_unit')
        return Phonenumber.objects.filter(division_id=self.kwargs['div_id'], is_published=True).select_related('division', 'military_unit')
        # return - передает отфильтрованные значения модели Phonenumber
        # division_id -  по ключу заложенного в адресе (URLS) = 'div_id'
        # is_published=True -  по опубликованным записям
        # div_id - параметра запроса в urls
        # select_related('division', 'military_unit') - уменьшаем колличество запросов SQL за счет "жадных" запросов


# класс просмотра детальной онформации о записи
class ViewPhones(DetailView):
    model = Phonenumber
    context_object_name = 'phone_item'
    template_name = 'phonebook/user_data.html'
    # pk_url_kwarg = 'user_id'  # если использовать собственную переменную, а не pk

# класс создания записи
class CreatePhones(LoginRequiredMixin, CreateView):
    # LoginRequiredMixin - миксин джанго для проверки аутентификации
    # raise_exception = True  # жестко отключает возможность аутентификации, перенаправляет на 403 ошибку (доступ запрещен)
    login_url = '/admin/'  # в случае ручного обращения к ссылке перенаправляет на страницу авторизации
    form_class = PhoneForm  # привязываем класс создания с формой
    template_name = 'phonebook/add_phone.html'  # страница заполнения формы
    # success_url = reverse_lazy('home')  # перенаправление по заполнению формы


### Контроллеры-функции
# функция регистрации
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # сохраняет введенные данные
            login(request, user)  # сразу вводит данные после регистрация для логирования
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')  # перенаправляет на главную страницу
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'phonebook/register.html', {"form": form})

# функции логирования
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'phonebook/login.html', {"form": form})

# функции выхода
def user_logout(request):
    logout(request)
    return redirect('login')

# функции отправки сообщения
def mail_go(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'Marinchenko_av@vch2034.gpk.by',
                             ['Marinchenko_av@vch2034.gpk.by'], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено!')
                return redirect('mail')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = ContactForm()
    return render(request, 'phonebook/mail.html', {"form": form})

# функция обработки запроса на тестовую страницу
def test_list(request):  # создаем функцию обрабатывающую запрос test_list
    phonebook = Phonenumber.objects.all()  # отображение всего списка (порядок отображения указан в админке)
    context = {
        'phonebook': phonebook,
        'title': 'Список телефонных номеров'
    }
    return render(request, template_name='phonebook/test_list.html', context=context)  # ответ - заполненный шаблон
    # request - работа с запросами
    # template_name='phonebook/online_indx.html' - папка нахождения шаблона
    # context = context  - заполнение шаблона данными из переменной context



# Черновик

# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#     return render(request, template_name='news/index.html', context=context)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     return render(request, 'news/category.html', {'news': news, 'category': category})


# # функция обработчик главной страницы
# def index(request):  # создаем функцию обрабатывающую запрос index
#     # phonebook = Phonenumber.objects.order_by('-create_at')   # отображение в обратном порядке по дате создания записи
#     phonebooks = Phonenumber.objects.all()  # отображение всего списка (порядок отображения указан в админке)
#     line = Phonenumber.objects.filter(id=8)
#     # divisions = Division.objects.all() - унифицируем вместо него используем пользовательский тег
#     units = MilitaryUnit.objects.all()
#     context = {
#         'title': 'Телефонная книга',  # задаем переменную (подпись страницы)
#         'phonebooks': phonebooks,
#         #'divisions': divisions, - унифицируем вместо него используем пользовательский тег
#         'units': units,
#         'line': line
#     }
#     return render(request, template_name='phonebook/index.html', context=context)  # ответ - заполненный шаблон
#     # request - работа с запросами
#     # template_name='phonebook/online_indx.html' - папка нахождения шаблона
#     # context = context  - заполнение шаблона данными из переменной context
#
# # функция обработчик страницы mil_unit
# def mil_unit(request, mil_id):  # создаем функцию обрабатывающую запрос index
#     # phonebooks = Phonenumber.objects.all()  # отображение всего списка (порядок отображения указан в админке)
#     phonebooks = Phonenumber.objects.filter(military_unit_id=mil_id)  # отображение отфильтрованного списка (порядок отображения указан в админке)
#
#     # divisions = Division.objects.all() - унифицируем вместо него используем пользовательский тег
#     units = MilitaryUnit.objects.all()
#     # unit = MilitaryUnit.objects.get(pk=mil_id)
#     unit = get_object_or_404(MilitaryUnit, pk=mil_id)  # отображение отфильтрованного списка (с учетом обработки ошибки 404)
#
#     line = Phonenumber.objects.filter(id=8)  # отображение отфильтрованного списка
#
#     # формируем передоваемые данные на страницу
#     context = {
#         'title': 'Телефонная книга в\ч',  # задаем переменную (подпись страницы)
#         'phonebooks': phonebooks,  # отфильтрованный список
#         # 'divisions': divisions, - унифицируем вместо него используем пользовательский тег
#         'units': units,
#         'unit': unit,
#         'line': line
#     }
#     return render(request, template_name='phonebook/mil_unit.html', context=context)  # ответ - заполненный шаблон
#     # request - работа с запросами
#     # template_name='phonebook/mil_unit.html' - папка нахождения шаблона
#     # context = context  - заполнение шаблона данными из переменной context
#
# # функция обработчик страницы division
# def division(request, div_id):  # создаем функцию обрабатывающую запрос index
#     # phonebooks = Phonenumber.objects.all()  # отображение всего списка (порядок отображения указан в админке)
#     phonebooks = Phonenumber.objects.filter(division_id=div_id)  # отображение отфильтрованного списка (порядок отображения указан в админке)
#     division = Division.objects.filter(pk=div_id)
#     # divisions = Division.objects.all() - унифицируем вместо него используем пользовательский тег
#     units = MilitaryUnit.objects.all()
#     line = Phonenumber.objects.filter(id=8)
#
#     context = {
#         'title': 'Подразделение',  # задаем переменную (подпись страницы)
#         'phonebooks': phonebooks,  # отфильтрованный список
#         # 'divisions': divisions, - унифицируем вместо него используем пользовательский тег
#         'units': units,
#         'line': line
#     }
#     return render(request, template_name='phonebook/division.html', context=context)  # ответ - заполненный шаблон
#     # request - работа с запросами
#     # template_name='phonebook/division.html' - папка нахождения шаблона
#     # context = context  - заполнение шаблона данными из переменной context
#
# # функция обработчик страницы user_data
# def user_data(request, user_id):  # создаем функцию обрабатывающую запрос user_data
#     # phonebook = Phonenumber.objects.filter()  # отображение всего списка (порядок отображения указан в админке)
#     phonebooks = Phonenumber.objects.filter(id=user_id)  # отображение отфильтрованного списка
#     # divisions = Division.objects.all() - унифицируем вместо него используем пользовательский тег
#     units = MilitaryUnit.objects.all()
#     line = Phonenumber.objects.filter(id=8)
#
#     context = {
#         'title': 'Данные пользователя',  # задаем переменную (подпись страницы)
#         'phonebooks': phonebooks,
#         # 'divisions': divisions, - унифицируем вместо него используем пользовательский тег
#         'units': units,
#         'line': line
#     }
#     return render(request, template_name='phonebook/user_data.html', context=context)  # ответ - заполненный шаблон
#     # request - работа с запросами
#     # template_name='phonebook/online_indx.html' - папка нахождения шаблона
#     # context = context  - заполнение шаблона данными из переменной context
#
# # функция обработчик страницы заполнения формы записи данных
# def add_phone(request):
#     if request.method == 'POST':  # если данные пришли из формы (метод = POST)
#         # принимаем данные заполненые ранее
#         form = PhoneForm(request.POST)
#         if form.is_valid():  # проверяем прошла ли форма валидацию (все ли данные соответствуют базе данных)
#             # print(form.cleaned_data)  # если форма прошла валидацию то появляется словарь c данными cleaned_data
#             # phone = Phonenumber.objects.create(**form.cleaned_data)  # сохраняем запись с несвязанной формой
#             phone = form.save()  # сохраняем запись со связанной формой
#             return redirect(phone)  # осуществляем перенаправление на созданную запись
#     else:  # в противном случае мы заполняем новую форму
#         form = PhoneForm()
#     return render(request, 'phonebook/add_phone.html', {'form': form})

# # тестовая страница для пагинации
# def test(request):
#     objects = ['john1', 'paul2', 'george3', 'ringo4', 'john5', 'paul6', 'george7']
#     paginator = Paginator(objects, 2)  # указывает список и по сколько записей выводить на странице
#     page_num = request.GET.get('page', 1)  # берет номер текущей страницы из массива GET методом get, по умолчанию 1
#     page_objects = paginator.get_page(page_num)  # берет объекты для текущей страницы
#     return render(request, 'phonebook/test_list.html', {'page_obj': page_objects})  # рендерит тестовую страницу для пагинации


# функция обработчик страницы test_list


# функция обработчик страницы test
# def test(request):  # создаем функцию обрабатывающую запрос test
#     print(request)
#     numbers = Phonenumber.objects.all()  # создадим переменную в которую поместим все данные класса Phonenumber
#     res = '<h1>СПРАВОЧНИК</h1>'
#     for item in numbers:
#         res += f'<div><p>{item.subdivision}</p><p>{item.position}{item.oficial_telephone}</p></div>\n<hr>\n'
#         # f -  форматированная строка
#         # <div> -  блок
#         # <p> - параграф
#         # <hr> - горизонтальная линия
#         # \n - перенос на новую строку
#     return HttpResponse(res)
