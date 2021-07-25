from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),  # при запросе в браузере пустрой строки отображается страница index
    path('index/', index, name='home'),  # при запросе в браузере index отображается страница index
    path('test_list/', test_list, name='test_list'),  # при запросе в браузере test_list отображается страница test_list
    path('test/', test, name='test'),  # при запросе в браузере test отображается страница test
    path('div/<int:div_id>/', division, name='division'),  # при запросе в браузере div, идет обращение к функции divisiion (views)
    path('mil/<int:mil_id>/', mil_unit, name='mil_unit'),  # при запросе в браузере mil, идет обращение к функции mil_unit (views)
    path('user/<int:user_id>/', user_data, name='user_data'),  # при запросе в браузере user, идет обращение к функции user_data (views)
]
