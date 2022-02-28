from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from .models import Lampi

# Create your views here.
class DetailView(LoginRequiredMixin, TemplateView):
    template_name = 'lampi/detail.html'

class IndexView(LoginRequiredMixin, ListView):
    template_name = 'lampi/index.html'
    def get_queryset(self):
        return Lampi.objects.all().filter(user=self.request.user)

'''
def index(request):
    return render(request, 'lampi/index.html')
'''