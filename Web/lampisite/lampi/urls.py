from django.urls import path, re_path

from . import views

urlpatterns = [
   # path('', views.IndexView.as_view(), name='index'),
   re_path(r'device/(?P<device_id>[0-9a-fA-F]+)', views.DetailView.as_view(), name='detail'),
]
