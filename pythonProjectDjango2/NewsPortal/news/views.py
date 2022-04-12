import pytz #  импортируем стандартный модуль для работы с часовыми поясами
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .tasks import send_mail_for_sub_once
from .models import *
from .forms import NewsForm
from .filters import NewsFilter, CategoryFilter
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.utils.translation import gettext as _  # импортируем функцию для перевода
# from django.utils.translation import activate, get_supported_language_variant, LANGUAGE_SESSION_KEY


class Index(View):
    def get(self, request):

        curent_time = timezone.now()
        models = Category.objects.all()

        context = {
            'models': models,
            'current_time': timezone.now(),
            'timezones': pytz.common_timezones #  добавляем в контекст все доступные часовые пояса
        }
        return HttpResponse(render(request, 'index.html', context))

    #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/news/')



        # string = _('Hello my world')
        #
        # return HttpResponse(string)


class CategoryList(ListView):
    model = Category
    template_name = 'category.html'
    queryset = Category.objects.all()
    context_object_name = 'Category'


class AuthorList(ListView):
    model = Author
    template_name = 'authors.html'
    queryset = Author.objects.all()
    context_object_name = 'Authors'
    ordering = ['-ratingAuthor']

    # paginate_by = 5
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Author.objects.all()

        return context


class NewsList(ListView):
    model = Post
    template_name = 'news1.html'
    context_object_name = 'Posts'
    ordering = ['-dateCreation']
    paginate_by = 5

    def get_filter(self):
        return NewsFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['is_authors'] = self.request.user.groups.filter(name='authors').exists()
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        # context['date_filter'] = DateFilter(self.request.GET, queryset=self.get_queryset())

        # context['posts'] = Post.objects.all()
        # context['form'] = NewsForm()

        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)
    #     return {
    #         **super().get_context_data(*args, **kwargs),
    #         'filter': self.get_filter(),
    #     }
    #
    # def __str__(self):
    #     return f'{self.title[1:] + self.title[:1]}'




class NewsSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'Posts'
    ordering = ['-dateCreation']
    paginate_by = 5

    def get_filter(self):
        return NewsFilter(self.request.GET, queryset=super().get_queryset())
        # and DateFilter(self.request.GET, queryset=self.get_queryset())

        # def news_list(request):
        #     f = NewsFilter(request.GET, queryset=Post.objects.all())
        #     return render(request, 'news/news_search.html', {'filter': f})

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        # context['date_filter'] = DateFilter(self.request.GET, queryset=self.get_queryset())
        return context
        # context['posts'] = Post.objects.all()
        # context['form'] = NewsForm()


class NewsDetailView(DetailView):
    template_name = 'news_detail.html'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        aaa = Category.objects.filter(pk=Post.objects.get(pk=id).postCategory.name).values("subscribers__username")
        context['is_not_subscribe'] = not aaa.filter(subscribers__username=self.request.user).exists()
        context['is_subscribe'] = aaa.filter(subscribers__username=self.request.user).exists()
        return context

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'product-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует также. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(*args, **kwargs)
            cache.set(f'product-{self.kwargs["pk"]}', obj)

        return obj


"""подписка и отписка"""
@login_required
def subscribe_me(request, news_category_id):
    user = request.user
    my_category = Category.objects.get(id=news_category_id)
    sub_user = User.objects.get(id=user.pk)
    if my_category.subscribers.filter(id=user.pk):
        my_category.subscribers.remove(sub_user)
        return redirect(f'/news')
    else:
        my_category.subscribers.add(sub_user)
        return redirect(f'/news')





class NewsCreateView(CreateView):
    template_name = 'news_create.html'
    form_class = NewsForm
    success_url = '/news/'



class NewsUpdateView(UpdateView):
    template_name = 'news_create.html'
    form_class = NewsForm
    success_url = '/news/'

    def get_object(self, **kwargs):  # (4)
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать

    # def get_object(self, **kwargs):
    #     id = self.kwargs.get('pk')
    #     return Post.objects.get(pk=id)


class NewsDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class AddNews(PermissionRequiredMixin, NewsCreateView):
    permission_required = ('news.add_post',)


class ChangeNews(PermissionRequiredMixin, NewsUpdateView):
    permission_required = ('news.change_post',)


class DeleteNews(PermissionRequiredMixin, NewsDeleteView):
    permission_required = ('news.delete_post',)


def send_mail_for_sub(instance, created, ):
    print()
    print()
    print('====================ПРОВЕРКА СИГНАЛОВ===========================')
    print()
    print('задача - отправка письма подписчикам при добавлении новой статьи')


    sub_text = instance.text
    category = Category.objects.get(pk=Post.objects.get(pk=instance.pk).postCategory.pk)
    print()
    print('category:', category)
    print()
    subscribers = category.subscribers.all()

    post = instance

    # для удобства вывода инфы в консоль, никакой важной функции не несет
    print('Адреса рассылки:')
    for zzz in subscribers:
        print(zzz.email)

    print()
    print()
    print()
    for subscriber in subscribers:
        # для удобства вывода инфы в консоль, никакой важной функции не несет
        print('**********************', subscriber.email, '**********************')
        print()
        print('Адресат:', subscriber.email)

        html_content = render_to_string(
            'mail.html', {'user': subscriber, 'text': sub_text[:50], 'post': post})

        sub_username = subscriber.username
        sub_useremail = subscriber.email

        send_mail_for_sub_once.delay(sub_username, sub_useremail, html_content)

        msg = EmailMultiAlternatives(
            subject=f'Здравствуй, {subscriber.username}. Новая статья в вашем разделе!',
            from_email='st3p.pavel@yandex.ru',
            to=[subscriber.email]
        )
        #
        msg.attach_alternative(html_content, 'text/html')

        # для удобства вывода инфы в консоль
        print()
        print(html_content)
        print()

        # Чтобы запустить реальную рассылку нужно раскоментить нижнюю строчку
        # msg.send()


    print('Представления - конец')
    return redirect('/news/')


def pageNotFound(request, exception):
    return render(request, 'NotFound.html')




# def pageNotFound(request, exception):
#     return HttpResponseNotFound('<h1> СТРАНИЦА НЕ НАЙДЕНА!!!</h1>'
#                                 )
#




