from modeltranslation.translator import register, TranslationOptions

from .models import *


# ����������� ��������� register ��� �������� � ����� �������� TranslationOptions, �� �������� ����� �������������
# ������������ ���� ������ ��� ��������
# �������� fields (�� ������������ �����) ���� ���� ���� ����

@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'text',)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('authorUser',)