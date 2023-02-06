import mediapipe as mp
import numpy as np 
import pandas as pd
import cv2 
import csv
import os
from helpers import get_coordinates, get_handedness, draw_normalized_coordinates, pre_process_hand_landmarks, get_args

# Object that let us draw landmarks in our image 
mp_drawing = mp.solutions.drawing_utils

# Object with all hand tracking methods of mediapipe
mp_hands = mp.solutions.hands

# The cv2.VideoCapture needs an number representing which device will be used 
# if the program does not work for you, try specifying a device other than 0 
args = get_args()
device = args.device
# Object that reads from the webcam
cap = cv2.VideoCapture(device)

# Get the width and height so we can draw on the image using opencv
video_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
video_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# Hand gesture label map 
gesture_label = pd.read_csv('data/gesture-label.csv', encoding = 'latin1')

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    model_complexity=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.5
) as hands:
    while cap.isOpened():             
        # cap.read() return two variables, the 'results' which is a boolean
        # identifying if the image was read and the frame that is a cv2 image
        # object of the frame captured
        ret, frame = cap.read()

        # Before processing our image with mediapipe is necessary to convert it 
        # from BGR to RGB, because mediapipe works with RGB and opencv with BGR
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Flip on horizontal so the lib detects correct handness
        image = cv2.flip(image, 1)

        # Setting the writable flag to false before process with mediapipe leads 
        # to improvement in the performance 
        image.flags.writeable = False

        # Do the actual processing with the mediapipe lib 
        results = hands.process(image)

        # Setting back the flag of writable so we can draw in the image
        image.flags.writeable = True
        
        # Writing that is waiting for the key to save the coordinates 
        image = cv2.putText(
            img = image, 
            text = 'Press a number from 0 to 9 to save gesture data',
            org = (50,50), #coordinates
            fontFace = cv2.FONT_HERSHEY_SIMPLEX,
            fontScale = 0.5, 
            color = (0, 0, 0), #RGB
            thickness = 2, 
            lineType = cv2.LINE_AA
        )

        # Drawing landmarks to the image
        ## If any hand was detected
        if results.multi_hand_landmarks:
            # The enumerate is used to multi hand detection, the hand variable
            # is basically all the landmarks from one hand
            for hand_index, hand_landmarks in enumerate(results.multi_hand_landmarks):
                                
                # Get handedness label
                handedness_label = get_handedness(
                    hand_index = hand_index,
                    results = results
                )
                
                # Drawing handedness on the wrist
                image = cv2.putText(
                            img = image, 
                            text = handedness_label,
                            org = get_coordinates('WRIST', hand_index, results, video_width, video_height), #coordinates
                            fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale = 0.8, 
                            color = (255, 255, 255), #RGB
                            thickness = 2, 
                            lineType = cv2.LINE_AA
                        )
                           
                # Pre process the hand landmarks coordinates 
                processed_hand_landmarks = pre_process_hand_landmarks(hand_index, results, video_width, video_height)
                
                # Draw the pre-processed coordinates according to the joint list
                joint_list = ['INDEX_FINGER_TIP','THUMB_TIP', 'MIDDLE_FINGER_TIP', 'RING_FINGER_TIP', 'PINKY_TIP']
                coordinates = []
                normalized_coordinates = []
                for joint in joint_list:
                    coordinates.append(
                        get_coordinates(
                            joint, 
                            hand_index, 
                            results, 
                            video_width, 
                            video_height
                        )
                    )
                    joint_index = mp_hands.HandLandmark[joint].numerator
                    normalized_coordinates.append(
                        tuple(processed_hand_landmarks[(joint_index*2):((joint_index*2)+2)])
                    )
                    
                normalized_coordinates = np.around(normalized_coordinates,2)

                image = draw_normalized_coordinates(
                    image = image, 
                    coordinates = coordinates, 
                    normalized_coordinates = normalized_coordinates
                )
                
                # Utility used to draw the image based on the landmark values
                mp_drawing.draw_landmarks(
                    image = image,
                    landmark_list = hand_landmarks,
                    connections = mp_hands.HAND_CONNECTIONS,
                    landmark_drawing_spec = mp_drawing.DrawingSpec(
                                                color = (1, 190, 255),
                                                thickness = 2,
                                                circle_radius = 4
                                            ),
                    connection_drawing_spec = mp_drawing.DrawingSpec(
                                                color = (86, 213, 0),
                                                thickness = 2,
                                                circle_radius = 2
                                            )
                )
                    
        # Converting it back to BGR so we can display using opencv
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Display the output frame of the webcam
        cv2.imshow('Hand Tracking', image)

        # - If 'q' is pressed the window is closed;
        # - If 'e' is pressed all training data will be erased;
        # - If a number from 0 to 9 is pressed then the coordinates
        #   will be saved  in the training sv file with those coordinates 
        #   associated to the number label pressed.
        key = cv2.waitKey(10)
        if key==ord('q'):
            break
        if key==ord('e'):
            os.remove('training-data.csv')
        if key>=ord('0') and key<=ord('9'):
            # Create the headers of the csv with the joint landmark names 
            headers = ['gesture_id']
            for joint in mp_hands.HandLandmark:
                headers.append(joint.name.lower()+'_x')
                headers.append(joint.name.lower()+'_y')

            if not os.path.exists('data'):
                os.makedirs('data')
            with open('data/training-data.csv','a',newline='') as file:
                writer = csv.writer(file)
                row = np.append(int(chr(key)),processed_hand_landmarks) 
                # If file was created from scratch, append header. If not, 
                # only append row
                if file.tell()==0:
                    writer.writerow(headers)
                    writer.writerow(row)
                else:
                    writer.writerow(row)
            
            # Erase the coordinates after saving it, to avoid write duplicate data 
            # when no hand be captured by the video 
            processed_hand_landmarks = None 
            
            try:
                label = gesture_label.loc[gesture_label[gesture_label.Label==int(chr(key))].index[0],'Gesture']
                print(f'Gesture saved to label {label}')
            except:
                print(f'No label detected. Update the "gesture-label.csv" file with the label of "{chr(key)}".')

cap.release()
# Destroy all the windows
cv2.destroyAllWindows()