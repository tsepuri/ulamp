import cv2
import time
'''
apiPreference    preferred Capture API backends to use. 
Can be used to enforce a specific reader implementation 
if multiple are available: 
e.g. cv2.CAP_MSMF or cv2.CAP_DSHOW.
'''
# open video0
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,1024)
#cap.set(cv2.CAP_PROP_FPS, 10)
#cap.set(10,52)
#cap.set(11,16)  
#cap.set(12,29)
#for i in range(3):
time.sleep(2.0)
cap.set(15, -8.0)

# set width and height
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# set fps
# cap.set(cv2.CAP_PROP_FPS, 30)
# while(True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     # Display the resulting frame
#     # cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
for img_counter in range(10):
    # Capture frame-by-frame
    
    ret, frame = cap.read()
    print(ret)
    # Display the resulting frame
    # cv2.imshow('frame', frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    if ret:
        name = "test"
        print("Worked")
        img_name = "dataset/"+ name +"/image_{}.jpg".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()