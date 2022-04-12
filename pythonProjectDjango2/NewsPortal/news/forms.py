from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField  # Импортируем true-false поле
from django_filters import ModelChoiceFilter
from django.utils.translation import gettext as _
from .models import *


class NewsForm(ModelForm):
    check_box = BooleanField(label=_('Поставьте галочку'))  # добавляем галочку, или же true-false поле

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].empty_label = _("Авторы не выбраны")
        self.fields['postCategory'].empty_label = _("Категории не выбраны")

    class Meta:
        model = Post
        fields = ['author', 'categoryType', 'postCategory', 'title', 'text', 'check_box']

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 120:
            raise ValidationError('Длина превышает 120 символов')

        return title
