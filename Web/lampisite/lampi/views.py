from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Lampi, LampiPref
from django.conf import settings
from lampi.forms import AddLampiForm, AddUserSettingForm
from mixpanel import Mixpanel

class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['MIXPANEL_TOKEN'] = settings.MIXPANEL_TOKEN
        return context

class UsersIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'users/index.html'

    def get_queryset(self):
        results = LampiPref.objects.order_by('user_name').distinct()
        return results

    def get_context_data(self, **kwargs):
        context = super(UsersIndexView, self).get_context_data(**kwargs)
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
    template_name = 'lampi/addlampi.html'
    form_class = AddLampiForm
    success_url = '/lampi'

    def get_context_data(self, **kwargs):
        context = super(AddUserView, self).get_context_data(**kwargs)
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
        context['h'] = self.request.GET['h']
        context['s'] = self.request.GET['s']
        context['b'] = self.request.GET['b']
        context['MIXPANEL_TOKEN'] = settings.MIXPANEL_TOKEN
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_name = form.cleaned_data['user_name']
        lampis = Lampi.objects.filter(user=self.request.user)
        user = LampiPref.objects.get(device_id=context['device_id'], user_name=user_name)
        print(user)
        self.success_url = "device/" + context['device_id']
        return super(UpdateSettingsView, self).form_valid(form)