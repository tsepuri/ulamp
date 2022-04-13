#! /usr/bin/python

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2


MQTT_CLIENT_ID = "facial_req"

# initialize the video stream and allow the camera sensor to warm up
# Set the ser to the followng
# src = 0 : for the build in single web cam, could be your laptop webcam
# src = 2 : I had to set it to 2 inorder to use the USB webcam attached to my laptop
# vs = VideoStream(src=0,framerate=5).start()
class FacialRecognition:
	def __init__(self):
		#Initialize 'currentname' to trigger only when a new person is identified.
		currentname = "unknown"
		#Determine faces from encodings.pickle file model created from train_model.py
		encodingsP = "encodings.pickle"

		# load the known faces and embeddings along with OpenCV's Haar
		# cascade for face detection
		print("[INFO] loading encodings + face detector...")
		data = pickle.loads(open(encodingsP, "rb").read())
		print("Read pickle")

        self.mqtt = Client(client_id=MQTT_CLIENT_ID)
        self.mqtt.enable_logger()
        self.mqtt.on_connect = self.on_connect
        self.mqtt.connect(MQTT_BROKER_HOST, port=MQTT_BROKER_PORT,
                          keepalive=MQTT_BROKER_KEEP_ALIVE_SECS)
		self.mqtt.loop_start()
        
    def on_connect(self, client, userdata, flags, rc):
        # self.mqtt.message_callback_add(TOPIC_USER_DETECTED,
        #                                self.receive_new_lamp_state)
        # self.mqtt.subscribe(TOPIC_USER_DETECTED, qos=1)
		pass

	def runner(self):
		cap = cv2.VideoCapture(0)
		cv2.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
		cv2.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
		# set fps
		cv2.set(cv2.CAP_PROP_FPS, 5)

		#vs = VideoStream(usePiCamera=True).start()
		time.sleep(2.0)

		# start the FPS counter
		fps = FPS().start()

		img_counter = 0
		# loop over frames from the video file stream
		while True:
			# grab the frame from the threaded video stream and resize it
			# to 500px (to speedup processing)
			# frame = vs.read()
			ret, frame = cap.read()
			cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)
			print(ret)
			print("Read Image")
			# frame = imutils.resize(frame, width=500)
			if ret:
				name = "test"
				print("Worked")
				img_name = "dataset/"+ name +"/image_{}.jpg".format(img_counter)
				cv2.imwrite(img_name, frame)
				print("{} written!".format(img_name))
				img_counter += 1
			print("Resized")
			# Detect the fce boxes
			boxes = face_recognition.face_locations(frame)
			print("Boxes")
			# compute the facial embeddings for each face bounding box
			encodings = face_recognition.face_encodings(frame, boxes)
			names = []
			print("Got encodings")

			# loop over the facial embeddings
			for encoding in encodings:
				# attempt to match each face in the input image to our known
				# encodings
				print("Encoding")
				matches = face_recognition.compare_faces(data["encodings"],
					encoding)
				name = "Unknown" #if face is not recognized, then print Unknown
				print(f"Matches: {matches}")

				# check to see if we have found a match
				if True in matches:
					# find the indexes of all matched faces then initialize a
					# dictionary to count the total number of times each face
					# was matched
					print("Matched")
					matchedIdxs = [i for (i, b) in enumerate(matches) if b]
					counts = {}
					# loop over the matched indexes and maintain a count for
					# each recognized face face
					for i in matchedIdxs:
						name = data["names"][i]
						print(f"Matched: {name}")
						msg = {"name":name, "client":MQTT_CLIENT_ID}
						self.mqtt.publish(TOPIC_USER_DELETED,
							json.dumps(msg).encode('utf-8'),
							qos=1)
						counts[name] = counts.get(name, 0) + 1

					# determine the recognized face with the largest number
					# of votes (note: in the event of an unlikely tie Python
					# will select first entry in the dictionary)
					name = max(counts, key=counts.get)

					#If someone in your dataset is identified, print their name on the screen
					if currentname != name:
						currentname = name
						print(currentname)

				# update the list of names
				names.append(name)

			# loop over the recognized faces
			# for ((top, right, bottom, left), name) in zip(boxes, names):
			# 	# draw the predicted face name on the image - color is in BGR
			# 	cv2.rectangle(frame, (left, top), (right, bottom),
			# 		(0, 255, 225), 2)
			# 	y = top - 15 if top - 15 > 15 else top + 15
			# 	cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			# 		.8, (0, 255, 255), 2)

			# display the image to our screen
			# cv2.imshow("Facial Recognition is Running", frame)
			key = cv2.waitKey(1) & 0xFF

			# quit when 'q' key is pressed
			if key == ord("q"):
				break

			# update the FPS counter
			fps.update()

		# stop the timer and display FPS information
		fps.stop()
		print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
		print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

		# do a bit of cleanup
		cv2.destroyAllWindows()
		vs.stop()
