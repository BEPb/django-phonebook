from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),  # при запросе в браузере пустрой строки отображается страница index
    path('index/', index, name='home'),  # при запросе в браузере index отображается страница index
    path('test_list/', test_list, name='test_list'),  # при запросе в браузере test_list отображается страница test_list
    path('test/', test, name='test'),  # при запросе в браузере test отображается страница test
]
