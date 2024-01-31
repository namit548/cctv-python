import cv2 
import numpy as np

# web cam
cap = cv2.VideoCapture('D:\\work\\cctv python\\cctv 1.0\\video.mp4') #here // mistake happens

while True:
    ret, frame1 = cap.read()

    # Check if the video capture was successful
    if not ret:
        print("Error: Unable to read frame.")
        break

    # Check the frame dimensions
    print("Frame dimensions:", frame1.shape)

    cv2.imshow('video original', frame1)

    if cv2.waitKey(1) == 13:
        break

cv2.destroyAllWindows()
cap.release()
