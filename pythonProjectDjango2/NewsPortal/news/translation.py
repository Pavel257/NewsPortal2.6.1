from modeltranslation.translator import register, TranslationOptions

from .models import *


# импортируем декоратор register для перевода и класс настроек TranslationOptions, от которого будем наследоваться
# регистрируем наши модели для перевода
# указывам fields (во мноественном числе) даже если поле одно

@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'text',)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('authorUser',)