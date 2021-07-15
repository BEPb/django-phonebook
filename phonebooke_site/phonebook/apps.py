# python 3.9 (name dev: 3BEPb)
# apps.py - модуль настройки нашего приложения

from django.apps import AppConfig


class PhonebookConfig(AppConfig):  # класс конфигурации приложения
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'phonebook'
    verbose_name = 'Справочник'  # изменяем имя модели в админке (в шапке таблицы)
