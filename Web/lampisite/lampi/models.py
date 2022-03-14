from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import uuid
import paho.mqtt.publish as publish
import json

# Create your models here.
DEFAULT_USER = 'parked_device_user'


def get_parked_user():
    return get_user_model().objects.get_or_create(username=DEFAULT_USER)[0]

def generate_association_code():
    return uuid.uuid4().hex

class Lampi(models.Model):
    name = models.CharField(max_length=50, default="My LAMPI")
    device_id = models.CharField(max_length=12, primary_key=True)
    user = models.ForeignKey(User,
                             on_delete=models.SET(get_parked_user))
    created_at = models.DateTimeField(auto_now_add=True)
    association_code = models.CharField(max_length=32, default=generate_association_code)

    def __str__(self):
        return "{}: {}".format(self.device_id, self.name)

    def _generate_device_association_topic(self):
        return 'devices/{}/lamp/associated'.format(self.device_id)

    def publish_unassociated_msg(self):
       # send association MQTT message
        assoc_msg = {
            'code': self.association_code,
            'associated': False,
        }
        publish.single(self._generate_device_association_topic(), 
        payload=json.dumps(assoc_msg), hostname="localhost", port=50001,
        retain=True, qos=2)
    
    def associate_and_publish_associated_msg(self,  user):
        # update Lampi instance with new user
        # publish associated message
        assoc_msg = {
            'associated': True
        }
        self.user = user
        self.save()
        publish.single(self._generate_device_association_topic(), 
        payload=json.dumps(assoc_msg), hostname="localhost", port=50001,
        retain=True, qos=2)
