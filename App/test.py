import cv2
from ultralytics import YOLO
import numpy as np

modelDetectionObjet = YOLO('yolov8n.pt')

# Définir la pipeline GStreamer
#gstreamer_str = "v4l2src device=/dev/video0 ! video/x-raw, format=YUY2, width=640, height=480, pixel-aspect-ratio=1/1, framerate=30/1 ! videoconvert ! appsink"

# Créer l'objet VideoCapture avec la pipeline GStreamer
#cap1 = cv2.VideoCapture('udpsrc port=12000 ! application/x-rtp, payload=96 ! rtpjitterbuffer ! rtph264depay ! avdec_h264 ! videoconvert ! videoscale ! video/x-raw,width=640,height=480!  appsink')
cap2 = cv2.VideoCapture('udpsrc port=12000 ! application/x-rtp, payload=96 ! rtpjitterbuffer ! rtph264depay ! avdec_h264 ! videoconvert ! videoscale ! video/x-raw, width=680,height=480 ! appsink')
# Vérifier si la capture vidéo est ouverte
if not cap2.isOpened():
    print("Erreur lors de l'ouverture de la capture vidéo.")
    exit()

# Lire et afficher les images de la vidéo
while True :
    #success1, frame1 = cap1.read()
    success2, frame2 = cap2.read()

    # run prediction on img
    results = modelDetectionObjet(frame2)                
    # Visualize the results on the frame
    annotated_frame1 = results[0].plot()
    
    if success2:
        frameh1 = frame2
        cv2.namedWindow('Demonstration aux Invalides', cv2.WINDOW_NORMAL)
        cv2.imshow('Demonstration aux Invalides', frameh1)
        if cv2.waitKey(1) == ord('q'):
            break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
