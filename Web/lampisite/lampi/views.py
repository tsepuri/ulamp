from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Lampi, LampiPref
from django.conf import settings
from lampi.forms import AddLampiForm, AddUserSettingForm, AddUserForm
from mixpanel import Mixpanel
import json

class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['MIXPANEL_TOKEN'] = settings.MIXPANEL_TOKEN
        return context

class UsersIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'users/index.html'

    def get_queryset(self):
        results = LampiPref.objects.order_by('username').distinct()
        return results

    def get_context_data(self, **kwargs):
        context = super(UsersIndexView, self).get_context_data(**kwargs)
        devices = Lampi.objects.filter(user=self.request.user)     
        context['can_add_user'] = devices is not None
        context['MIXPANEL_TOKEN'] = settings.MIXPANEL_TOKEN
        return context

class LampiIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'lampi/index.html'

    def get_queryset(self):
        results = Lampi.objects.filter(user=self.request.user)
        return results

    def get_context_data(self, **kwargs):
        context = super(LampiIndexView, self).get_context_data(**kwargs)
        context['MIXPANEL_TOKEN'] = settings.MIXPANEL_TOKEN
        return context


class DetailView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'lampi/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['device'] = get_object_or_404(
            Lampi, pk=kwargs['device_id'], user=self.request.user)
        context['MIXPANEL_TOKEN'] = settings.MIXPANEL_TOKEN
        return context

class UserDetailView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'lampi/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['device'] = get_object_or_404(
            Lampi, pk=kwargs['device_id'], user=self.request.user)
        context['MIXPANEL_TOKEN'] = settings.MIXPANEL_TOKEN
        return context


class AddLampiView(LoginRequiredMixin, generic.FormView):
    template_name = 'lampi/addlampi.html'
    form_class = AddLampiForm
    success_url = '/lampi'

    def get_context_data(self, **kwargs):
        context = super(AddLampiView, self).get_context_data(**kwargs)
        context['MIXPANEL_TOKEN'] = settings.MIXPANEL_TOKEN
        return context

    def form_valid(self, form):
        device = form.cleaned_data['device']
        device.associate_and_publish_associated_msg(self.request.user)

        mp = Mixpanel(settings.MIXPANEL_TOKEN)
        mp.track(device.user.username, "LAMPI Activation",
                 {'event_type': 'activations', 'interface': 'web',
                  'device_id': device.device_id})

        return super(AddLampiView, self).form_valid(form)

class AddUserView(LoginRequiredMixin, generic.FormView):
    template_name = 'users/adduser.html'
    form_class = AddUserForm
    success_url = '/users'

    def get_context_data(self, **kwargs):
        context = super(AddUserView, self).get_context_data(**kwargs)
        context['MIXPANEL_TOKEN'] = settings.MIXPANEL_TOKEN
        return context

    def form_valid(self, form):
        username = form.cleaned_data['username']
        print(username)
        
        # Finding Associated Lampis
        lampis = Lampi.objects.filter(user=self.request.user)
        for lampi in lampis:
            print(f"Device id: {lampi.device_id}")
            try:
                preference = LampiPref.objects.get(device_id=lampi, username=username)
            except LampiPref.DoesNotExist:
                preference = None

            if preference == None:
                preference = LampiPref.objects.create(device_id=lampi, username=username)

        return super(AddUserView, self).form_valid(form)

def upload_photos(request):
    print(request)
    photos = request.POST.get('photos', None)
    print(photos)

class UpdateSettingsView(LoginRequiredMixin, generic.FormView):
    template_name = 'lampi/updateSettings.html'
    form_class = AddUserSettingForm
    success_url = ""

    def get_form(self, form_class=None):
        # context = super(UpdateSettingsView, self).get_context_data()
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(device_id=self.request.GET['device_id'], user=self.request.user, **self.get_form_kwargs())
        
    def get_context_data(self, **kwargs):
        context = super(UpdateSettingsView, self).get_context_data(**kwargs)
        print(kwargs) 
        print(self.request.GET)
        context['device_id'] = self.request.GET['device_id']
        context['device'] = get_object_or_404(
            Lampi, pk=self.request.GET['device_id'], user=self.request.user)
        print(context['device_id'])
        context['h'] = int(self.request.GET['h'])/100
        context['s'] = int(self.request.GET['s'])/100
        context['b'] = int(self.request.GET['b'])/100
        context['MIXPANEL_TOKEN'] = settings.MIXPANEL_TOKEN
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        username = form.cleaned_data['username']
        lampis = Lampi.objects.filter(user=self.request.user)
        user = LampiPref.objects.get(device_id=context['device_id'], username=username)
        print(user)
        if user is not None:
            new_state = {"color": {"h": context['h'], "s":context['s']},
            "brightness": context['b']}
            user.settings = json.dumps(new_state)
            user.save()
        self.success_url = "device/" + context['device_id']
        return super(UpdateSettingsView, self).form_valid(form)