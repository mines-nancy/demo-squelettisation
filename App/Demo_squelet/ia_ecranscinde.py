import cv2
from ultralytics import YOLO
import numpy as np

model_nano1=YOLO('yolov8n-pose.pt')
model_drone=YOLO('yolov8n.pt')

# Définir la pipeline GStreamer
gstreamer_nano1= 'udpsrc port=12002 ! application/x-rtp, payload=96 ! rtpjitterbuffer ! rtph264depay ! avdec_h264 ! videoconvert ! videoscale ! video/x-raw, width=1280,height=720 ! appsink'
gstreamer_drone = 'udpsrc port=12001 ! application/x-rtp, payload=96 ! rtpjitterbuffer ! rtph264depay ! avdec_h264 ! videoconvert ! videoscale ! video/x-raw, width=1280,height=720 ! appsink'

## TEST AVEC WEBCAM
#gstreamer_nano1 = 'v4l2src device=/dev/video0 ! videoscale ! video/x-raw, format=YUY2, width=1280, height=720, pixel-aspect-ratio=1/1, framerate=30/1 ! videoconvert ! appsink'
#gstreamer_drone = 'v4l2src device=/dev/video0 ! video/x-raw, format=YUY2, width=640, height=480, pixel-aspect-ratio=1/1, framerate=30/1 ! videoconvert ! appsink'

## TEST AVEC TELEPHONE
#gstreamer_nano1 = 'rtspsrc location=rtsp://137.194.154.130:8080/h264_ulaw.sdp latency=100 ! queue ! rtph264depay ! avdec_h264 ! videoconvert ! videoscale ! video/x-raw,width=1280,height=720,format=BGR ! appsink drop=1'
#gstreamer_drone = 'rtspsrc location=rtsp://192.168.60.168:8080/h264_ulaw.sdp latency=100 ! queue ! rtph264depay ! avdec_h264 ! videoconvert ! videoscale ! video/x-raw,width=1280,height=720,format=BGR ! appsink drop=1'


# Créer l'objet VideoCapture avec la pipeline GStreamer
cap_nano1 = cv2.VideoCapture(gstreamer_nano1)
cap_drone = cv2.VideoCapture(gstreamer_drone)

# Vérifier si la capture vidéo est ouverte
if not cap_nano1.isOpened() or not cap_drone.isOpened():
    print("Erreur lors de l'ouverture de la capture vidéo.")
    exit()

# Lire et afficher les images de la vidéo
while True :
	# Lecture des flux video
    success_nano1, frame_nano1 = cap_nano1.read()
    success_drone, frame_drone = cap_drone.read()

    # run prediction on img
    results_nano1 = model_nano1(frame_nano1, conf=0.6)
    results_drone = model_drone(frame_drone, conf=0.5) 

    # Visualize the results on the frame
    annotedframe_nano1 = results_nano1[0].plot()
    annotedframe_drone= results_drone[0].plot()

    imgbunker = cv2.imread('Demo14Juillet/bunker.jpg')
    imgdrone = cv2.imread('Demo14Juillet/drone.jpg')
    
    if success_nano1 and success_drone:
        ## Composition des frames
        frame_h1 = np.hstack((annotedframe_nano1,annotedframe_drone))
        frame_h2 = np.hstack((imgbunker, imgdrone))

        fullscreen = np.vstack((frame_h1,frame_h2))


        cv2.namedWindow('Demonstration aux Invalides', cv2.WINDOW_NORMAL)
        cv2.imshow('Demonstration aux Invalides', fullscreen)
        if cv2.waitKey(1) == ord('q'):
            break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
