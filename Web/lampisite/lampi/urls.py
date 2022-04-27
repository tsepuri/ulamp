from django.urls import path, re_path, include, reverse

from . import views

app_name = 'lampi'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('lampi/', include([
    path('', views.LampiIndexView.as_view(), name='lampiindex'),
    path('add/', views.AddLampiView.as_view(), name='add'),
    re_path(r'^device/(?P<device_id>[0-9a-fA-F]+)$',
            views.DetailView.as_view(), name='detail'),
    re_path(r'^settings$',
            views.UpdateSettingsView.as_view(), name='user_settings'),
    ])),
    path('users/', include([
    path('', views.UsersIndexView.as_view(), name='usersindex'),
    path('add/', views.AddUserView.as_view(), name='adduser'),
    re_path(r'^user/(?P<user_name>[0-9a-fA-F]+)$',
            views.UserDetailView.as_view(), name='userdetail'),
    ]))
]
