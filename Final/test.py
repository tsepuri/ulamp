import cv2
'''
apiPreference    preferred Capture API backends to use. 
Can be used to enforce a specific reader implementation 
if multiple are available: 
e.g. cv2.CAP_MSMF or cv2.CAP_DSHOW.
'''
# open video0
cap = cv2.VideoCapture(0)
# set width and height
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# set fps
# cap.set(cv2.CAP_PROP_FPS, 30)
# while(True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()
#     # Display the resulting frame
#     # cv2.imshow('frame', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
for img_counter in range(2):
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