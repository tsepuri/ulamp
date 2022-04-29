#! /usr/bin/python

# import the necessary packages
from imutils import paths
import face_recognition
# import argparse
import pickle
import cv2
import os
from paho.mqtt.client import Client
from lamp_common import *

MQTT_BROKER_PORT = 1883
MQTT_CLIENT_ID = 'camera'
def train():
	print("here")
	# our images are located in the dataset folder
	print("[INFO] start processing faces...")
	imagePaths = list(paths.list_images("dataset"))

	# initialize the list of known encodings and known names
	knownEncodings = []
	knownNames = []

	# loop over the image paths
	for (i, imagePath) in enumerate(imagePaths):
		# extract the person name from the image path
		print("[INFO] processing image {}/{}".format(i + 1,
														len(imagePaths)))
		name = imagePath.split(os.path.sep)[-2]

		# load the input image and convert it from RGB (OpenCV ordering)
		# to dlib ordering (RGB)
		image = cv2.imread(imagePath)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		# detect the (x, y)-coordinates of the bounding boxes
		# corresponding to each face in the input image
		boxes = face_recognition.face_locations(rgb,
												model="hog")

		# compute the facial embedding for the face
		encodings = face_recognition.face_encodings(rgb, boxes)

		# loop over the encodings
		for encoding in encodings:
			# add each encoding + name to our set of known names and
			# encodings
			knownEncodings.append(encoding)
			knownNames.append(name)

	# dump the facial encodings + names to disk
	print("[INFO] serializing encodings...")
	data = {"encodings": knownEncodings, "names": knownNames}
	f = open("encodings.pickle", "wb")
	f.write(pickle.dumps(data))
	f.close()
'''
class Train:
    def __init__(self):
        self._updated = False
        self.hue = 1
        self.saturation = 1
        self.brightness = 1
        self.lamp_is_on = True

        self.mqtt = Client(client_id=MQTT_CLIENT_ID)
        self.mqtt.enable_logger()
        self.mqtt.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc):
        self.mqtt.message_callback_add("devices/cameraid/" + TOPIC_USER_ADDED,
                                       self.train)
        self.mqtt.subscribe("devices/cameraid/" + TOPIC_USER_ADDED, qos=1)

    def serve(self):
        self.mqtt.connect('localhost', port=MQTT_BROKER_PORT)
        self.mqtt.loop_forever()

    def train(self):
        print("here")
        # our images are located in the dataset folder
        print("[INFO] start processing faces...")
        imagePaths = list(paths.list_images("dataset"))

        # initialize the list of known encodings and known names
        knownEncodings = []
        knownNames = []

        # loop over the image paths
        for (i, imagePath) in enumerate(imagePaths):
            # extract the person name from the image path
            print("[INFO] processing image {}/{}".format(i + 1,
                                                         len(imagePaths)))
            name = imagePath.split(os.path.sep)[-2]

            # load the input image and convert it from RGB (OpenCV ordering)
            # to dlib ordering (RGB)
            image = cv2.imread(imagePath)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            boxes = face_recognition.face_locations(rgb,
                                                    model="hog")

            # compute the facial embedding for the face
            encodings = face_recognition.face_encodings(rgb, boxes)

            # loop over the encodings
            for encoding in encodings:
                # add each encoding + name to our set of known names and
                # encodings
                knownEncodings.append(encoding)
                knownNames.append(name)

        # dump the facial encodings + names to disk
        print("[INFO] serializing encodings...")
        data = {"encodings": knownEncodings, "names": knownNames}
        f = open("encodings.pickle", "wb")
        f.write(pickle.dumps(data))
        f.close()
'''
