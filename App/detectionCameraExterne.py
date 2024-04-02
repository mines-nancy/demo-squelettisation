import cv2
from ultralytics import YOLO

modelDetectionObjet = YOLO('yolov8n.pt')

#cap = cv2.VideoCapture('v4l2src device=/dev/video0 ! video/x-raw, width=640, height=480 ! videoconvert ! appsink')

#cap = cv2.VideoCapture('udpsrc port=12000 ! application/x-rtp, payload=96 ! rtpjitterbuffer ! rtph264depay ! avdec_h264 ! videoconvert ! appsink ')

cap = cv2.VideoCapture('rtspsrc location=rtsp://100.75.153.159:8080/h264_ulaw.sdp latency=100 ! queue ! rtph264depay ! avdec_h264 ! videoconvert ! videoscale ! video/x-raw,width=640,height=480,format=BGR ! appsink drop=1')
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
