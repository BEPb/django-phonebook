# python 3.9 (name dev: 3BEPb)
# utils.py - файл в котором храняться наши миксины (можно использовать только для классов)
# для функций используются декораторы

class MyMixin(object):
    mixin_prop = ''  # свойство которое можно в дальнейшем переопределять

    def get_prop(self):
        return self.mixin_prop.upper()  # переопределяет значение переменной mixin_prop в верхний регистр

    def get_upper(self, s):  # переопределяет значение строки в верхний регистр
        if isinstance(s, str):  # если это строка
            return s.upper()  # то преобразуем в верхний регистр
        else:
            return s.title.upper()  # обратимся к значению и преобразуем в строку
