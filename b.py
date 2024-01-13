import cv2

background_path = r"D:\work\cctv python\background2.png"
background = cv2.imread(background_path)

# Check if the background image is loaded successfully
if background is None:
    print(f"Error: Unable to load background image from {background_path}")
    exit()

# Resize the background image to match the dimensions of the video frames
video_path = r"D:\work\cctv python\video.mp4"
video = cv2.VideoCapture(video_path)

# Check if the video file is opened successfully
if not video.isOpened():
    print(f"Error: Unable to open video file at {video_path}")
    exit()

# Get the dimensions of the video frames
frame_width = int(video.get(3))
frame_height = int(video.get(4))

# Resize the background image
background = cv2.resize(background, (frame_width, frame_height))

# Preprocess the background
background_gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
background_blur = cv2.GaussianBlur(background_gray, (21, 21), 0)

while True:
    status, frame = video.read()

    # Check if the video frame is read successfully
    if not status:
        print("Error: Unable to read video frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    diff = cv2.absdiff(background_blur, gray)

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
