from django.contrib import admin

# Register your models here.

from .models import Phonenumber, Category


class PhonenumberAdmin(admin.ModelAdmin):  # описываем раздел админки "Справочник"
    # указываем отображаемые поля
    list_display = (
        'id',
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
        'note'
    )

    list_display_links = ('id',  # перечесляем те позиции которые при нажатие открывают окно редактирование объекта
        'subdivision',
        'position',
        'surname',
        'name',
        'second_name',
        'oficial_telephone',
        'landline_telephone',
        'service_fax',
        'mobile_telephone')
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


# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'subdivision')
#     list_display_links = ('id', 'surname')
#     search_fields = ('surname',
#                      'position',)


admin.site.register(Phonenumber, PhonenumberAdmin)  # регистрируем в нашей админке наше приложение
# admin.site.register(Category, CategoryAdmin)
