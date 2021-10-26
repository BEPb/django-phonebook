from django.contrib import admin
# настройка админки
# Register your models here.

from .models import Phonenumber, Division, MilitaryUnit


class PhonenumberAdmin(admin.ModelAdmin):  # описываем раздел админки "Справочник"
    # указываем отображаемые поля
    list_display = (
        'id',
        'military_unit',  # указываем воинскую часть из таблицы MilitaryUnit
        'division',  # указываем подразделение из таблицы Division
        'subdivision',
        'position',
        'surname',
        'name',
        'second_name',
        'oficial_telephone',
        'landline_telephone',
        'service_fax',
        'mobile_telephone',
        'create_at', 'update_at',
        'photo',
        'is_published',
        'note',
        'service_email'
    )

    list_display_links = ('id',  # перечесляем те позиции которые при нажатие открывают окно редактирование объекта
        'military_unit',  # указываем воинскую часть из таблицы MilitaryUnit
        'division',  # указываем подразделение из таблицы Division
        'subdivision',
        'position',
        'surname',
        'name',
        'second_name',
        'oficial_telephone',
        'landline_telephone',
        'service_fax',
        'mobile_telephone',
        'service_email')
    search_fields = ('surname',  # перечесляем все позиции по которым доступен поиск
                     'position',
                     'oficial_telephone',
                     'landline_telephone',
                     'service_fax',
                     'mobile_telephone'
                     )
    # list_editable = ('is_published',)
    # list_filter = ('is_published',)

    # 'subdivision', 'position', 'surname', 'name', 'second_name', 'oficial_telephone', 'landline_telephone', 'service_fax', 'mobile_telephone', 'create_at', 'update_at', 'photo', 'is_published', 'note'


class DivisionAdmin(admin.ModelAdmin):  # описываем раздел админки "Подразделение"
    list_display = ('id', 'title')  # указываем отображаемые поля
    list_display_links = ('id', 'title')  # перечесляем те позиции которые при нажатие открывают окно редактирование объекта
    search_fields = ('title',)  # перечесляем все позиции по которым доступен поиск



class MilitaryUnitAdmin(admin.ModelAdmin):  # описываем раздел админки "Подразделение"
    list_display = ('id', 'title', 'name_unity')  # указываем отображаемые поля
    list_display_links = ('id', 'title', 'name_unity')  # перечесляем те позиции которые при нажатие открывают окно редактирование объекта
    search_fields = ('title', 'name_unity')  # перечесляем все позиции по которым доступен поиск


admin.site.register(Phonenumber, PhonenumberAdmin)  # регистрируем в нашей админке наше приложение
admin.site.register(Division, DivisionAdmin)  # регистрируем в нашей админке подразделения
admin.site.register(MilitaryUnit, MilitaryUnitAdmin)  # регистрируем в нашей админке воинские части
