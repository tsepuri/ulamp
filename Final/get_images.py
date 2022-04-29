#! /usr/bin/python

# import the necessary packages
import requests # to get image from the web
import shutil # to save it locally
from paho.mqtt.client import Client
from lamp_common import *
import json
import os
from train_model import train

MQTT_CLIENT_ID = "get_images"
class GetImages:
    def __init__(self):
        self.mqtt = Client(client_id=MQTT_CLIENT_ID)

    def runner(self):
        self.mqtt.enable_logger()
        self.mqtt.on_connect = self.on_connect
        self.mqtt.connect(MQTT_BROKER_HOST, port=MQTT_BROKER_PORT,
                          keepalive=MQTT_BROKER_KEEP_ALIVE_SECS)
        self.mqtt.loop_forever()
        
    def on_connect(self, client, userdata, flags, rc):
        self.mqtt.message_callback_add(TOPIC_USER_ADDED,
                                       self.receive_new_user)
        self.mqtt.subscribe(TOPIC_USER_ADDED, qos=1)

    def receive_new_user(self, client, userdata, message):
        if message.topic == 'user/added' and message.payload != 0:
            new_user_added = json.loads(message.payload.decode('utf-8'))
            username = new_user_added['username']
            directory = os.path.join(os.getcwd(), 'dataset', username)
            os.makedirs(directory)
            image_url_base = "http://ec2-3-90-19-244.compute-1.amazonaws.com/static/users/"
            for i in range(10):
                image_url = image_url_base + username + f'/{i+1}.png'
                # filename = image_url.split("/")[-1]
                
                filename = os.path.join(directory, f'{i+1}.png')
                # Open the url image, set stream to True, this will return the stream content.
                r = requests.get(image_url, stream = True)
                
                # Check if the image was retrieved successfully
                if r.status_code == 200:
                    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                    r.raw.decode_content = True
                    
                    # Open a local file with wb ( write binary ) permission.
                    with open(filename,'wb') as f:
                        shutil.copyfileobj(r.raw, f)
                        
                    print('Image sucessfully Downloaded: ',filename)
                else:
                    print('Image Couldn\'t be retreived')
            train()
            

GetImages().runner()