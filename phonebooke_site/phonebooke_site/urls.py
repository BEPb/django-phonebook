"""phonebooke_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings  # подгружаем настройки в режиме отладки
from django.conf.urls.static import static  # для работы с статическими адресами
# from phonebook.views import index  # прописываем отдельно маршрут к функции модуля phonebook прописан в views.py
from phonebook.views import *  # прописываем маршрут ко всем функциям модуля phonebook прописан в views.py
from django.urls import path, include

urlpatterns = [  # в левой части - запрос, в правой место расположения страницы
    path('admin/', admin.site.urls),
    # path('phonebook/', index),  # прописываем маршрут к приложению phonebook
    # path('phonebook/', test),  # прописываем маршрут к приложению phonebook
    path('', include('phonebook.urls')),  # прописываем все маршруты к приложению phonebook
    path('phonebook/', include('phonebook.urls')),  # прописываем все маршруты к приложению phonebook
]

# отладчик по умолчанию
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# в качестве отладчика используем модуль debug_toolbar
# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#                       path('__debug__/', include(debug_toolbar.urls)),
#                   ] + urlpatterns
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
