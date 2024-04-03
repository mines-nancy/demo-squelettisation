import cv2
import os
from ultralytics import YOLO
import numpy as np
import argparse

#from utils.plots import colors

class Colors:
    # Ultralytics color palette https://ultralytics.com/
    def __init__(self):
        #Initialize colors as hex = matplotlib.colors.TABLEAU_COLORS.values().
        hexs = ('FF3838', 'FF9D97', 'FF701F', 'FFB21D', 'CFD231', '48F90A', '92CC17', '3DDB86', '1A9334', '00D4BB',
                '2C99A8', '00C2FF', '344593', '6473FF', '0018EC', '8438FF', '520085', 'CB38FF', 'FF95C8', 'FF37C7')
        self.palette = [self.hex2rgb(f'#{c}') for c in hexs]
        self.n = len(self.palette)
        self.pose_palette = np.array([[255, 128, 0], [255, 153, 51], [255, 178, 102], [230, 230, 0], [255, 153, 255],
                                      [153, 204, 255], [255, 102, 255], [255, 51, 255], [102, 178, 255], [51, 153, 255],
                                      [255, 153, 153], [255, 102, 102], [255, 51, 51], [153, 255, 153], [102, 255, 102],
                                      [51, 255, 51], [0, 255, 0], [0, 0, 255], [255, 0, 0], [255, 255, 255]],
                                     dtype=np.uint8)

    def __call__(self, i, bgr=False):
        #Converts hex color codes to rgb values.
        c = self.palette[int(i) % self.n]
        return (c[2], c[1], c[0]) if bgr else c

    @staticmethod
    def hex2rgb(h):  # rgb order (PIL)
        return tuple(int(h[1 + i:1 + i + 2], 16) for i in (0, 2, 4))


colors = Colors()  # create instance for 'from utils.plots import colors'

limb_color = colors.pose_palette[[9, 9, 9, 9, 7, 7, 7, 0, 0, 0, 0, 0, 16, 16, 16, 16, 16, 16, 16]]
kpt_color = colors.pose_palette[[16, 16, 16, 16, 16, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9]]



skeleton_lines = [[16, 14], [14, 12], [17, 15], [15, 13], [12, 13], [6, 12], [7, 13], 
[6, 7], [6, 8], [7, 9], [8, 10], [9, 11], [2, 3], [1, 2], [1, 3], [2, 4], [3, 5], 
[4, 6], [5, 7]]

# Définir la pipeline GStreamer
def cameraSelection(vecteurVideo):
    return switch_case(vecteurVideo) 

def switch_case(argument):
	match argument:
		case 'nano2':
			return 'rtspsrc location=rtsp://100.75.153.134:8554/camera latency=100 ! queue ! rtph265depay ! avdec_h265 ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1'
		case 'o11':
			return 'rtspsrc location=rtsp://192.168.50.205:8080/h264_ulaw.sdp latency=100 ! queue ! rtph264depay ! avdec_h264 ! videoconvert ! videoscale ! video/x-raw,width=1280,height=720,format=BGR ! appsink drop=1'
		case 'prompt_ip_webcam':
			print("Please enter the device's IP address")
			return 'rtspsrc location=rtsp://'+input()+':8080/h264_ulaw.sdp latency=100 ! queue ! rtph264depay ! avdec_h264 ! videoconvert ! videoscale ! video/x-raw,width=1280,height=720,format=BGR ! appsink drop=1'
		case 'prompt_rtsp':
			print("Please enter the full link")
			return  'rtspsrc location='+input()+' latency=100 ! queue ! rtph264depay ! avdec_h264 ! videoconvert ! videoscale ! video/x-raw,width=1280,height=720,format=BGR ! appsink drop=1'
		case _:
			return 'Option invalide'


def detection(args):
    # Load the YOLOv8 model
    model = YOLO(args.yolo_weights)
    names = model.names

    model_pose = YOLO(args.pose_weights)
    names_pose = model_pose.names 
    #print(names_pose)


    # Open the video file
    video_path = cameraSelection(args.source) if args.source!= '/dev/video0' else args.source
    cap = cv2.VideoCapture(video_path)
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH,args.width)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT,args.height)
    #cap.set(3,args.width)
    #cap.set(4,args.height)
    #save_path = "."
    # Loop through the video frames
    file_num = 0
    uniques_id=set()
    cv2.namedWindow("Démonstration IA", cv2.WINDOW_NORMAL)
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()
        #print(model_pose)
        if success:
            # Run YOLOv8 inference on the frame
            if args.tracking == 'y' or args.tracking == 'Y':
                results = model.track(frame, persist=True, conf=0.75, device=0)
            else:
                results = model(frame,conf=0.75, device=0)
            results_pose = model_pose(frame, conf=0.25, device=0)

            if  results[0].boxes.id !=  None:
                boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
                classes = results[0].boxes.cls.cpu().numpy().astype(str)
                skeletons = results_pose[0].keypoints.xy.cpu().numpy()

                if results_pose[0].keypoints.conf is not None:
                    confidence_skeleton = results_pose[0].keypoints.conf.cpu().numpy().astype(float)

                ids = results[0].boxes.id.cpu().numpy().astype(int)
                #print(results_pose[0].keypoints)
                for box, id, classe in zip(boxes, ids, classes):
                    # Check if the id is unique
                    #print(skeleton[0][0])
                    int_id =int(id)
                    if  int_id  not  in  uniques_id:
                        uniques_id.add(int_id)
        
                        # Crop the image using the bounding box coordinates
                        cropped_img = frame[box[1]:box[3], box[0]:box[2]]
        
                        # Save the cropped image with a unique filename
                        #filename = f"cropped_img_{int_id}.jpg"
                        #filepath = os.path.join(save_path, filename)
                        #cv2.imwrite(filepath, cropped_img)
        
                    # Draw the bounding box and id on the frame (85, 45, 255)
                    color_box = (int(colors.pose_palette[int(float(classe))%len(colors.pose_palette)][0]), int(colors.pose_palette[int(float(classe))%len(colors.pose_palette)][1]), int(colors.pose_palette[int(float(classe))%len(colors.pose_palette)][2]))
                    cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), color_box, 2, lineType=cv2.LINE_AA)
                    """
                    cv2.putText(
                        frame,
                        f"Id {id}, {names[int(float(classe))]}",
                        (box[0], box[1]),
                        0,
                        0.9,
                        [85, 45, 255],
                        2,
                        lineType=cv2.LINE_AA
                    """
                    cv2.putText(
                        frame,
                        f"{names[int(float(classe))]}",
                        (box[0]+5, box[1]+20),
                        0,
                        0.9,
                        [85, 45, 255],
                        2,
                        lineType=cv2.LINE_AA
                    )
                 
                for skeleton in skeletons:
                    if len(skeleton)==17:
                        for i in range(len(skeleton_lines)):
                            #print(confidence_skeleton[0])
                            if confidence_skeleton[0][int(skeleton_lines[i][0]-1)]>0.25 and confidence_skeleton[0][int(skeleton_lines[i][1]-1)]>0.25:
                                #print(limb_color)
                                color_limb_to_display = ( int( limb_color[i][0]), int( limb_color[i][1]), int( limb_color[i][2]))
                                cv2.line(frame, (round(skeleton[int(skeleton_lines[i][0]-1)][0]), round(skeleton[int(skeleton_lines[i][0]-1)][1])), ( round(skeleton[int(skeleton_lines[i][1]-1)][0]),
                                round(skeleton[int(skeleton_lines[i][1]-1)][1])), color_limb_to_display, thickness=2, lineType=cv2.LINE_AA)
                        for j in range(len(skeleton)):
                            if confidence_skeleton[0][j]>0.25 :
                                color_pts_to_display = ( int( kpt_color[j][0]), int( kpt_color[j][1]), int( kpt_color[j][2]))
                                cv2.circle(frame, (round(skeleton[j][0]), round(skeleton[j][1])), 5, color_pts_to_display, -1, lineType=cv2.LINE_AA)
                    cv2.imshow("Démonstration IA", frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break

            else:
                boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
                classes = results[0].boxes.cls.cpu().numpy().astype(str)
                skeletons = results_pose[0].keypoints.xy.cpu().numpy()

                if results_pose[0].keypoints.conf is not None:
                    confidence_skeleton = results_pose[0].keypoints.conf.cpu().numpy().astype(float)

                for box, classe, skeleton in zip(boxes, classes, skeletons):
                    # Draw the bounding box and id on the frame
                    color_box = (int(colors.pose_palette[int(float(classe))%len(colors.pose_palette)][0]), int(colors.pose_palette[int(float(classe))%len(colors.pose_palette)][1]), int(colors.pose_palette[int(float(classe))%len(colors.pose_palette)][2]))
                    cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), color_box, 2, lineType=cv2.LINE_AA)
                    cv2.putText(
                        frame,
                        f"{names[int(float(classe))]}",
                        (box[0]+5, box[1]+20),
                        0,
                        0.9,
                        [85, 45, 255],
                        2,
                        lineType=cv2.LINE_AA
                    )
                    for skeleton in skeletons:
                        if len(skeleton)==17:
                            for i in range(len(skeleton_lines)):
                                #print(confidence_skeleton[0])
                                if confidence_skeleton[0][int(skeleton_lines[i][0]-1)]>0.25 and confidence_skeleton[0][int(skeleton_lines[i][1]-1)]>0.25:
                                    #print(limb_color)
                                    color_limb_to_display = ( int( limb_color[i][0]), int( limb_color[i][1]), int( limb_color[i][2]))
                                    cv2.line(frame, (round(skeleton[int(skeleton_lines[i][0]-1)][0]), round(skeleton[int(skeleton_lines[i][0]-1)][1])), ( round(skeleton[int(skeleton_lines[i][1]-1)][0]),
                                    round(skeleton[int(skeleton_lines[i][1]-1)][1])), color_limb_to_display, thickness=2, lineType=cv2.LINE_AA)
                            for j in range(len(skeleton)):
                                if confidence_skeleton[0][j]>0.25 :
                                    color_pts_to_display = ( int( kpt_color[j][0]), int( kpt_color[j][1]), int( kpt_color[j][2]))
                                    cv2.circle(frame, (round(skeleton[j][0]), round(skeleton[j][1])), 5, color_pts_to_display, -1, lineType=cv2.LINE_AA)
                    cv2.imshow("Démonstration IA", frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break



                cv2.imshow("Démonstration IA", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # Break the loop if the end of the video is reached
            break

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str,
                        help="name of the video source",
                        default="/dev/video0")
    parser.add_argument('--width', type=int,
                        help="width of the source video to use",
                        default=1280)
    parser.add_argument('--height', type=int,
                        help="heigth of the source video to use",
                        default=720)
    parser.add_argument('--pose_weights', type=str,
                        help="model path",default='yolov8m-pose.pt')
    parser.add_argument('--yolo_weights', type=str, default='yolov8m.pt',
                        help='model path')
    parser.add_argument('--tracking', type=str, default='y',
                        help='activate tracking')

    args = parser.parse_args()
    detection(args)
