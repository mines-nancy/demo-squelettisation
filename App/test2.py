import cv2
from ultralytics import YOLO

modelDetectionObjet = YOLO('yolov8m-pose.pt')

#cap = cv2.VideoCapture('v4l2src device=/dev/video0 ! video/x-raw, width=640, height=480 ! videoconvert ! appsink')

#cap = cv2.VideoCapture('udpsrc port=12000 ! application/x-rtp, payload=96 ! rtpjitterbuffer ! rtph264depay ! avdec_h264 ! videoconvert ! appsink ')

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()

    # run prediction on img
    results = modelDetectionObjet(frame) 

    if not ret:
        break
    # Visualize the results on the frame
    annotated_frame = results[0].plot()
    cv2.namedWindow('Demonstration IA', cv2.WINDOW_NORMAL)
    cv2.imshow('Demonstration IA', annotated_frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
