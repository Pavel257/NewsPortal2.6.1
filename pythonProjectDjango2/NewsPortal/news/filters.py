from django.template.backends import django
from django_filters import FilterSet, DateFilter, DateTimeFromToRangeFilter, CharFilter, ModelChoiceFilter, \
    ModelMultipleChoiceFilter
from .models import *
from datetime import datetime
from django.forms import DateInput
from django.utils.translation import gettext as _


class NewsFilter(FilterSet):
    dateCreation = DateFilter(
        lookup_expr='gt',
        label=_('Позже даты'),
        widget=DateInput(
            attrs={
                'type': 'date'
            }
        )
    )
    title = ModelChoiceFilter('title', label=_('Поиск по заголовкам статьи:'), lookup_expr='icontains',
                              queryset=Post.objects.all(), empty_label=_('Заголовки не выбраны')
                              )

    postCategory = ModelChoiceFilter(queryset=Category.objects.all(), empty_label=_('Категории не выбраны'))


    author = ModelChoiceFilter(
        field_name='author_id',
        label=_('Авторы'),
        queryset=Author.objects.all(),
        empty_label=_('Авторы не выбраны')
    )

    class Meta:
        model = Post
        fields = ('author', 'postCategory', 'dateCreation')
        # fields = {
        #     'title': ['icontains'],
        #     'author': ['in'],
        #     'postCategory': ['exact'],
        #     'dateCreation': ['gt']
        #
        # }

# class PostFilter(FilterSet):
#     author = ModelMultipleChoiceFilter(
#         field_name='author',
#         lookup_expr='in',
#         label='Автор',
#         queryset=Post.objects.all()
#     )
#
#     title = CharFilter(
#         field_name='heading',
#         lookup_expr='icontains',
#         label='Заголовок'
#     )
#     datetime = DateFilter(
#         field_name='data_create',
#         widget=DateInput(attrs={'type': 'date'}),
#         lookup_expr='gt',
#         label='Позже даты'
#     )
#
#     class Meta:
#         model = Post
#         fields = []

# title = CharFilter('title', label='Заголовок содержит:', lookup_expr='icontains')
# author = ModelMultipleChoiceFilter('author',
# label ='Автор:',
# lookup_expr ='exact',
# queryset =Post.objects.all())


# time_in = DateFilter(
#     lookup_expr='icontains',
#     widget=django.forms.DateInput(
#         attrs={
#             'type': 'date'
#         }
#     )
# )
class CategoryFilter(FilterSet):
    name = ModelChoiceFilter(queryset=Category.objects.all())

    class Meta:
        model = Category
        fields = ('name',)