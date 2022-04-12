import pytz
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protect/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['is_authors'] = self.request.user.groups.filter(name='authors').exists()
        return context


    # def get(self, request):
    #
    #     curent_time = timezone.now()
    #
    #     context = {
    #         'current_time': timezone.now(),
    #         'timezones': pytz.common_timezones
    #     }
    #     return HttpResponse(render(request, 'protect/index.html', context))
    #
    # def post(self, request):
    #     request.session['django_timezone'] = request.POST['timezone']
    #     return redirect('/')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['is_not_premium'] = not self.request.user.groups.filter(name='premium').exists()
    #     return context




