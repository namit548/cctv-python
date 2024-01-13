import cv2

background_path = r"D:\work\cctv python\background2.png"
background = cv2.imread(background_path)

# Check if the background image is loaded successfully
if background is None:
    print(f"Error: Unable to load background image from {background_path}")
    exit()

background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
background = cv2.GaussianBlur(background, (21, 21), 0)

video_path = r"D:\work\cctv python\testing.mp4"
video = cv2.VideoCapture(video_path)

# Check if the video file is opened successfully
if not video.isOpened():
    print(f"Error: Unable to open video file at {video_path}")
    exit()

while True:
    status, frame = video.read()

    # Check if the video frame is read successfully
    if not status:
        print("Error: Unable to read video frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    diff = cv2.absdiff(background, gray)

    thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    cnts, res = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2.imshow("All Contours", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
