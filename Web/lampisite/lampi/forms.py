from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.conf import settings
from .models import Lampi, LampiPref


def device_association_topic(device_id):
    return 'devices/{}/lamp/associated'.format(device_id)


class AddLampiForm(forms.Form):
    association_code = forms.CharField(label="Association Code", min_length=6,
                                       max_length=6)

    def clean(self):
        cleaned_data = super(AddLampiForm, self).clean()
        print("received form with code {}".format(
              cleaned_data['association_code']))
        # look up device with start of association_code
        uname = settings.DEFAULT_USER
        parked_user = get_user_model().objects.get(username=uname)
        devices = Lampi.objects.filter(
            user=parked_user,
            association_code__startswith=cleaned_data['association_code'])
        if not devices:
            self.add_error('association_code',
                           ValidationError("Invalid Association Code",
                                           code='invalid'))
        else:
            cleaned_data['device'] = devices[0]
        return cleaned_data

class AddUserForm(forms.Form):
    username = forms.CharField(label="Username")
    def clean(self):
        cleaned_data = super(AddUserForm, self).clean()
        print("received form with username {}".format(
              cleaned_data['username']))
        existing_users = LampiPref.objects.order_by('username').distinct()
        if cleaned_data['username'] in existing_users:
            self.add_eror('username', ValidationError("Username already exists", code='invalid'))
        else:
            print()
        return cleaned_data

class AddUserSettingForm(forms.Form):

    def __init__(self, device_id, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = LampiPref.objects.filter(device_id=device_id)
        print(type(users))
        print(users)
        usernames = []
        for i in range(len(users)):
            user = users[i]
            usernames.append((user.username, user.username))
        print(type(usernames))
        print(usernames)
        self.fields['username'] = forms.CharField(label='User Name', widget=forms.Select(choices=usernames))

    def clean(self):
        cleaned_data = super(AddUserSettingForm, self).clean()
        print("received form for user name {}".format(
              cleaned_data['username']))
        return cleaned_data
