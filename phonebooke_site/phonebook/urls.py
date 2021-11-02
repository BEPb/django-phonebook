# python 3.9 (name dev: 3BEPb)
# urls.py - файл работы с адресами приложения

from django.urls import path  # импортируем модуль определения пути размещения файла
from .views import *  # импортируем все модули из файла views
from django.views.decorators.cache import cache_page  # модуль кеширования классов (страниц)

# словарь адресов страниц
urlpatterns = [
    # path('', index, name='home'),  # при запросе в браузере пустрой строки отображается страница index
    # path('index/', index, name='home'),  # страница index (работа через функцию index)
    # path('', HomePhones.as_view(), name='home'),  # страница index работа через класс HomePhones (не кешированный)
    path('', cache_page(60)(HomePhones.as_view()), name='home'),  # страница 127.0.0.1/ работа через класс HomePhones (кешированный)
    path('index/', HomePhones.as_view(), name='home'),  # страница index работа через класс HomePhones (не кешированный)
    # path('index/', cache_page(60)(HomePhones.as_view()), name='home'),  # страница index работа через класс HomePhones (кешированный)
    # 60 секунд время на которое осуществляется обновление кеша
    path('list_mil/', HomeMilytary.as_view(), name='mils'),  # страница mil работа через класс HomeMilytary

    path('test_list/', test_list, name='test_list'),  # при запросе в браузере test_list отображается страница test_list
    # path('test/', test, name='test'),  # при запросе в браузере test отображается страница test

    # path('div/<int:div_id>/', division, name='division'),  # страница division, через функцию divisiion (views)
    # path('div/<int:div_id>/', PhonesByDivision.as_view(), name='division'),  # страница division, через класс  PhonesByDivision (views)
    path('div/<int:div_id>/', PhonesByDivision.as_view(), name='division'),  # страница division, через класс  PhonesByDivision (views)

    # path('mil/<int:mil_id>/', mil_unit, name='mil_unit'),  # страница mil_unit, через функцию mil_unit (views)
    path('mil/<int:mil_id>/', PhonesByMilitary.as_view(), name='mil_unit'),  # страница mil_unit, через класс  PhonesByMilitary (views)

    # path('user/<int:user_id>/', user_data, name='user_data'),  # страница user_data через функцию user_data (views)
    # path('user/<int:user_id>/', ViewPhones.as_view(), name='user_data'),  # страница user_data через класс ViewPhones (views)
    path('user/<int:pk>/', ViewPhones.as_view(), name='user_data'),  # страница user_data через класс ViewPhones (views)
    # 'user/<int:user_id>/' - указываем ссылку, где <int:user_id> - переменная, зависит от номера данных
    # user_data - функция в обработчике (views) каторая отрабатывает данную страницу
    # name='user_data' - имя данной страницы(без привязки к путю размещения)

    # path('add_phone/', add_phone, name='add_phone'),  # работа через функцию
    path('add_phone/', CreatePhones.as_view(), name='add_phone'),  # работа через класс

    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('mail/', mail_go, name='mail'),
]
