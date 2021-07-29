from django import forms  # импортируем модуль работы с формами
from .models import Division, MilitaryUnit, Phonenumber  # импортируем данные из файла .models
import re  # импортируем модуль регулярных выражений, для работы с данными в форме (для применения собственных проверок введенных данных в форму)
from django.core.exceptions import ValidationError  # модуль обработок собственных ошибок
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # модуль регистрации пользователя и логирования
from django.contrib.auth.models import User  # модуль работы с пользователями
from django.core.mail import send_mail  # модуль отправки сообщений

# создаем класс формы не связанного с моделью по которому будем заполнять наши данные
# class PhoneForm(forms.Form):
#     military_unit = forms.ModelChoiceField(empty_label='Выберете в/ч', queryset=MilitaryUnit.objects.all(),
#                                            label='в\ч, организация', widget=forms.Select(attrs={"class": "form-control"}))
#     division = forms.ModelChoiceField(empty_label='Выберете подразделение', queryset=Division.objects.all(),
#                                       label='подразделение', widget=forms.Select(attrs={"class": "form-control"}))
#     # empty_label='Выберете подразделение' - значение в выпадающем меню в начале списка
#     subdivision = forms.CharField(max_length=150, label='подотдел', required=False,
#                                   widget=forms.TextInput(attrs={"class": "form-control"}))  # поле "подотдел",
#     # max_length = 150, - максимальная длинна 150 символов
#     # label = 'подотдел', - отображаемое имя
#     # required = False - не обязательное к заполнению поле
#     # widget=forms.TextInput - уточняем используемый виджет
#     position = forms.CharField(max_length=150, label='должность', widget=forms.TextInput(attrs={"class": "form-control"}))  # поле "должность", максимальная длинна 150 символов
#     surname = forms.CharField(max_length=50, label='фамилия', widget=forms.TextInput(attrs={"class": "form-control"}))  # поле "фамилия", максимальная длинна 50 символов
#     name = forms.CharField(max_length=20, label='имя', widget=forms.TextInput(attrs={"class": "form-control"}))  # поле "имя", максимальная длинна 20 символов
#     second_name = forms.CharField(max_length=20, label='отчество', widget=forms.TextInput(attrs={"class": "form-control"}))  # поле "отчество", максимальная длинна 20 символов
#     oficial_telephone = forms.CharField(max_length=20, label='служебный телефон', required=False, widget=forms.TextInput(attrs={"class": "form-control"}))  # поле "служебный телефон"
#     landline_telephone = forms.CharField(max_length=20, label='городской телефон', required=False, widget=forms.TextInput(attrs={"class": "form-control"}))  # поле "городской телефон"
#     service_fax = forms.CharField(max_length=20, label='служебный факс', required=False, widget=forms.TextInput(attrs={"class": "form-control"}))  # поле "служебный факс"
#     mobile_telephone = forms.CharField(max_length=20, label='мобильный телефон', required=False, widget=forms.TextInput(attrs={"class": "form-control"}))  # поле "мобильный телефон"
#     # photo = forms.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='фото',
#     #                           blank=True)  # upload_to='photos/' - место хранения фото
#     is_published = forms.BooleanField(label='опубликовано', initial=True)  # публикация, по умолчанию - истина
#     note = forms.CharField(max_length=50, label='примечание', required=False, widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}))  # поле "примечание"
#     service_email = forms.CharField(max_length=150, label='почта', required=False, widget=forms.TextInput(attrs={"class": "form-control"}))  # поле с указание служебной почты

# создаем класс формы не связанного с моделью по которому будем заполнять наши данные

# форма ввода данных телефонный справочник
class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phonenumber
        #fields = '__all__'  # отображает связанную форму всех полей по умолчанию django
        fields = ['military_unit', 'division', 'subdivision', 'position', 'surname', 'name', 'second_name', 'oficial_telephone', 'landline_telephone', 'service_fax', 'mobile_telephone', 'is_published', 'note', 'service_email']
        widgets = {
            'military_unit': forms.Select(attrs={"class": "form-control"}),
            'division': forms.Select(attrs={"class": "form-control"}),
            'subdivision': forms.TextInput(attrs={"class": "form-control"}),
            'position': forms.TextInput(attrs={"class": "form-control"}),  # поле "должность", максимальная длинна 150 символов
            'surname': forms.TextInput(attrs={"class": "form-control"}),  # поле "фамилия", максимальная длинна 50 символов
            'name': forms.TextInput(attrs={"class": "form-control"}),  # поле "имя", максимальная длинна 20 символов
            'second_name': forms.TextInput(attrs={"class": "form-control"}),  # поле "отчество", максимальная длинна 20 символов
            'oficial_telephone': forms.TextInput(attrs={"class": "form-control"}),  # поле "служебный телефон"
            'landline_telephone': forms.TextInput(attrs={"class": "form-control"}),  # поле "городской телефон"
            'service_fax': forms.TextInput(attrs={"class": "form-control"}),  # поле "служебный факс"
            'mobile_telephone': forms.TextInput(attrs={"class": "form-control"}),  # поле "мобильный телефон"
            # 'is_published': forms.BooleanField(label='опубликовано', initial=True),  # публикация, по умолчанию - истина
            'note': forms.Textarea(attrs={"class": "form-control", "rows": 5}),  # поле "примечание"
            'service_email': forms.TextInput(attrs={"class": "form-control"}), # поле с указание служебной почты
            }
    # валидатор - метод для автоматической проверки правильно ли введены данные в поле
    def clean_surname(self):  # создаем метод для обработки собственных ошибок, в данном случае фамилия не должна начинаться на цифру
        surname = self.cleaned_data['surname']  # получаем введенные данные по ключу 'surname'
        if re.match(r'\d', surname):  # проверяем не начинается ли строка с цифры
            raise ValidationError('Фамилия не должна начинаться с цифры')  #текст ошибки
        return surname  # возвращает значение


# форма регистрации
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', help_text='Максимум 150 символов', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# форма логирования
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# форма отправки почты
class ContactForm(forms.Form):
    subject = forms.CharField(label='Тема', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'class': 'form-control', "rows": 5, 'placeholder': "Введите сообщение для менеджера раздела. Содержание карточки будет добавлено к сообщению автоматически.", 'maxlength': "1000", 'autocomplete': "off"}))
