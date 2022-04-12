from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import *


def like_plus_five(modeladmin, request, queryset):
    # функция накрутки лайков статье
    for posts in queryset:
        posts.rating = posts.rating + 5
        posts.save()


like_plus_five.short_description = 'Накрутить пять лайков к рейтингу поста'


def like_minus_five(modeladmin, request, queryset):
    # функция  скрутки лайков статье
    for posts in queryset:
        posts.rating = posts.rating - 5
        posts.save()


like_minus_five.short_description = 'Скрутить пять лайков к рейтингу поста'


class PostCategoryInLine(admin.TabularInline):
    model = Post.postCategory.through


# class PostAdmin(admin.ModelAdmin):
#     list_display = ('author',  'title', 'categoryType', 'dateCreation', 'rating',)
#     # list_display = [field.name for field in Post._meta.get_fields()]
#     list_filter = ('author', 'dateCreation', 'postCategory', 'rating',)
#     list_display_links = ('author',)
#     inlines = [PostCategoryInLine, ]
#     actions = [like_plus_five, like_minus_five]  # добавляем действия в список
#     search_fields = ('title',)  # тут всё очень похоже на фильтры из запросов в базу
#     # list_editable = ('title', 'categoryType')  #список имен полей в модели, который позволит редактировать на странице списка изменений.

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name',)
#     list_display_links = ("name",)
#     inlines = [PostCategoryInLine, ]


class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.get_fields()]
    list_display_links = ('commentUser', 'text')
    list_filter = ('rating', 'dateCreation')


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('postThrough', 'categoryThrough',)


# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('authorUser', 'ratingAuthor')


class AuthorAdmin(TranslationAdmin):
    model = Author
    # list_editable = ('authorUser', )

class PostAdmin(TranslationAdmin):
    model = Post



class CategoryAdmin(TranslationAdmin):
    model = Category


admin.site.register(Author, AuthorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin, )
admin.site.register(PostCategory, PostCategoryAdmin)

admin.site.site_title = 'Админ-панель портала новостей'
admin.site.site_header = 'Админ-панель портала новостей'