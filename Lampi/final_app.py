import platform
from math import fabs
import json
import os
from paho.mqtt.client import Client
from lamp_common import *

MQTT_BROKER_PORT = 50001
MQTT_CLIENT_ID = "user_persets"

class UserPresets:
    def __init__(self):
        self._updated = False
        self.hue = 1
        self.saturation = 1
        self.brightness = 1
        self.lamp_is_on = False

        self.mqtt = Client(client_id=MQTT_CLIENT_ID)
        self.mqtt.enable_logger()
        self.mqtt.on_connect = self.on_connect
        

    def on_connect(self, client, userdata, flags, rc):
        self.mqtt.message_callback_add(TOPIC_USER_DETECTED,
                                       self.receive_new_lamp_state)
        self.mqtt.subscribe("devices/b827eba09ec0/" + TOPIC_USER_DETECTED, qos=1)

    def serve(self):
        self.mqtt.connect('localhost', port=50001)
        self.mqtt.loop_forever()

    def receive_new_lamp_state(self, client, userdata, message):
        new_person = json.loads(message.payload.decode('utf-8'))
        if new_person['name'] == 'Oleksii':
            new_state = {'color': {'h': 0.5, 's':1},
               'brightness': 1,
               'on': self.lamp_is_on,
               'client': 'ec2'}
        if new_person['name'] == 'Tarun':
            new_state = {'color': {'h': 0.2, 's': 1},
               'brightness': 1,
               'on': self.lamp_is_on,
               'client': 'ec2'}

        Clock.schedule_once(lambda dt: self._update_ui(new_state), 0.01)

    def _update_ui(self, new_state):
        if self._updated and new_state['client'] == MQTT_CLIENT_ID:
            # ignore updates generated by this client, except the first to
            #   make sure the UI is syncrhonized with the lamp_service
            return
        try:
            if 'color' in new_state:
                self.hue = new_state['color']['h']
                self.saturation = new_state['color']['s']
            if 'brightness' in new_state:
                self.brightness = new_state['brightness']
            if 'on' in new_state:
                self.lamp_is_on = new_state['on']
            self._update_leds()
        finally:
            self._updatingUI = False

        self._updated = True

    def _update_leds(self):
        msg = {'color': {'h': self.hue, 's': self.saturation},
               'brightness': self.brightness,
               'on': self.lamp_is_on,
               'client': MQTT_CLIENT_ID}
        self.mqtt.publish("devices/b827eba09ec0/" + TOPIC_SET_LAMP_CONFIG,
                          json.dumps(msg).encode('utf-8'),
                          qos=1)

user_presets = UserPresets()
user_presets.serve()