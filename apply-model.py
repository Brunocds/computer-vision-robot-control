import mediapipe as mp 
import cv2 
import numpy as np 
import pandas as pd
import joblib
from helpers import get_handedness, pre_process_hand_landmarks, get_args

args = get_args()
arduino_mode = args.arduino_mode

# Arduino mode passed when executing the script is used to run the code with an Arduino connected. 
# This variable is used to be able to run the script without an Arduino connected, passing a variable 
# different than 1. 
if arduino_mode==1:
    import pyfirmata 
    from pyfirmata import SERVO

    # Variable used to control the time in which the servo motor will be triggered
    ref = None
    # Initializing variable that will contain the gesture recognized
    gesture = None
    # Initializing variable that will contain the module in which the servo will be moved
    module = None

    # Dictionary containing the pins for each articulation
    articulation_dict = {
    'Mindinho' : {
        'pin': 2,
        'fator': 1.3
    },
    'Anelar' : {
        'pin': 3,
        'fator': 1
    },
    'Medio' : {
        'pin': 4,
        'fator': 1.4
    },
    'Indicador' : {
        'pin': 5,
        'fator': 1.1
    },
    'Polegar' : {
        'pin': 6,
        'fator': 1
    },
    'Pulso' : {
        'pin': 7,
        'fator': 1
    },
    }

    # Specifying what port the Arduino is connected
    port = 'COM3' 
    board = pyfirmata.Arduino(port) 

    # Setting Arduino's pins
    for info in articulation_dict.values(): 
        board.digital[info['pin']].mode = SERVO

# Object that let us draw landmarks in our image 
mp_drawing = mp.solutions.drawing_utils

# Object with all hand tracking methods of mediapipe
mp_hands = mp.solutions.hands

# Loading gesture recognition model 
gesture_classifier = joblib.load('model/clf.pkl')

# The cv2.VideoCapture needs an number representing which device will be used 
# if the program does not work for you, try specifying a device other than 0 
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

        handedness_detected = [] 
        
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
                
                handedness_detected.append(handedness_label)
                
                # Draw bounding box only to the left hand
                if handedness_label=='Left': 
                    x_max = 0
                    y_max = 0
                    x_min = video_width
                    y_min = video_height
                    for coordinates in hand_landmarks.landmark:
                        x, y = int(coordinates.x * video_width), int(coordinates.y * video_height)
                        if x > x_max:
                            x_max = x
                        if x < x_min:
                            x_min = x
                        if y > y_max:
                            y_max = y
                        if y < y_min:
                            y_min = y
                    cv2.rectangle(image, (x_min-10, y_min-10), (x_max+10, y_max+10), (50, 50, 50), 2)
                    cv2.rectangle(image, (x_min-10, y_min-10), (x_max+10, y_min-50), (50, 50, 50), -1)
                           
                    # Pre process the hand landmarks coordinates 
                    processed_hand_landmarks = pre_process_hand_landmarks(hand_index, results, video_width, video_height)

                    # Predicting the gesture label
                    label_predicted = int(gesture_classifier.predict(processed_hand_landmarks.reshape(1,-1))[0])
                    text_label_predicted = gesture_label[gesture_label.Label==label_predicted].Gesture.to_list()[0]
                    
                    # Updating the gesture with the text_label_predicted
                    gesture = text_label_predicted

                    # Writing the predicted label to the frame 
                    image = cv2.putText(
                        img = image, 
                        text = text_label_predicted,
                        org = (x_min+5,y_min-20), #coordinates
                        fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale = 0.7, 
                        color = (255, 255, 255), #RGB
                        thickness = 2, 
                        lineType = cv2.LINE_AA
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
                elif handedness_label=='Right':                
                    # Drawing a circle in the joints of the THUMB_TIP and INDEX_FINGER_TIP and
                    # storing its coordinates 
                    joints = ['THUMB_TIP', 'INDEX_FINGER_TIP']
                    joints_coordinates = {}
                    for joint in joints:
                        coordinates = {}
                        coordinates['x'] = int(results.multi_hand_landmarks[hand_index].landmark[mp_hands.HandLandmark[joint]].x*video_width)
                        coordinates['y'] = int(results.multi_hand_landmarks[hand_index].landmark[mp_hands.HandLandmark[joint]].y*video_height)
                        joints_coordinates[joint] = coordinates
                        # Drawing circle
                        image = cv2.circle(
                            img = image, 
                            center = (coordinates['x'],coordinates['y']), 
                            radius = 4, 
                            color = (148, 0, 211), 
                            thickness = 2
                        )
                        # Drawing white border for the circle
                        image = cv2.circle(
                            img = image, 
                            center = (coordinates['x'],coordinates['y']), 
                            radius = 6, 
                            color = (255, 255, 255), 
                            thickness = 1
                        )
                    
                    # Draw line between the thumb_tip and index_finger_tip
                    image = cv2.line(
                        img = image, 
                        pt1 = (joints_coordinates['THUMB_TIP']['x'], joints_coordinates['THUMB_TIP']['y']), 
                        pt2 = (joints_coordinates['INDEX_FINGER_TIP']['x'], joints_coordinates['INDEX_FINGER_TIP']['y']), 
                        color = (255,4,163), 
                        thickness = 2
                    )
                    
                    # Drawing circle in the center of the line
                    min_x = min(joints_coordinates['THUMB_TIP']['x'],joints_coordinates['INDEX_FINGER_TIP']['x'])
                    min_y = min(joints_coordinates['THUMB_TIP']['y'],joints_coordinates['INDEX_FINGER_TIP']['y'])
                    diff_x = int(abs(joints_coordinates['THUMB_TIP']['x'] - joints_coordinates['INDEX_FINGER_TIP']['x'])/2)
                    diff_y = int(abs(joints_coordinates['THUMB_TIP']['y'] - joints_coordinates['INDEX_FINGER_TIP']['y'])/2)
                    image = cv2.circle(
                        img = image, 
                        center = (min_x + diff_x, min_y + diff_y), 
                        radius = 6, 
                        color = (148, 0, 211), 
                        thickness = 3
                    ) 
                    
                    # Drawing white border for the circle in the center of the line
                    image = cv2.circle(
                            img = image, 
                            center = (min_x + diff_x, min_y + diff_y), 
                            radius = 8, 
                            color = (255, 255, 255), 
                            thickness = 1
                        )
                    
                    # Draw the rectangle border that will contain the relative distance of the line 
                    # between the thumb_tip and index_finger_tip 
                    
                    beginning_x_coordinate_rect = 85
                    end_x_coordinate_rect = 485
                    
                    image = cv2.rectangle(
                        img = image,
                        pt1 = (beginning_x_coordinate_rect, 30),
                        pt2 = (end_x_coordinate_rect, 70),
                        color = (255,4,163),
                        thickness = 2
                    )
                    
                    # The relative distance will be the line between the thumb tip and index_finger_tip
                    # divided by the line between the wrist and index_finger_dip
                    wrist_coordinates = (results.multi_hand_landmarks[hand_index].landmark[mp_hands.HandLandmark['WRIST']].x * video_width, results.multi_hand_landmarks[hand_index].landmark[mp_hands.HandLandmark['WRIST']].y * video_height)
                    distance_wrist_index = np.sqrt(((wrist_coordinates[0]-joints_coordinates['INDEX_FINGER_TIP']['x'])**2) + ((wrist_coordinates[1]-joints_coordinates['INDEX_FINGER_TIP']['y'])**2))
                    distance_thumb_index = np.sqrt(((joints_coordinates['THUMB_TIP']['x']-joints_coordinates['INDEX_FINGER_TIP']['x'])**2) + ((joints_coordinates['THUMB_TIP']['y']-joints_coordinates['INDEX_FINGER_TIP']['y'])**2))
                    relative_distance_thumb_index = distance_thumb_index/distance_wrist_index
                    #Offset
                    relative_distance_thumb_index = relative_distance_thumb_index - 0.08
                      
                    if relative_distance_thumb_index > 1:
                        relative_distance_thumb_index = 1
                    elif relative_distance_thumb_index < 0:
                        relative_distance_thumb_index = 0
                    
                    linear_interpolation = int(beginning_x_coordinate_rect + ((end_x_coordinate_rect-beginning_x_coordinate_rect)*((relative_distance_thumb_index))))
                    
                    # Draw the rectangle that will fill the base rectangle according to the distance
                    # between the thumb_tip index_finger_tip
                    image = cv2.rectangle(
                        img = image,
                        pt1 = (beginning_x_coordinate_rect, 30),
                        pt2 = (linear_interpolation, 70),
                        color = (255,4,163),
                        thickness = -1
                    )
                    
                    # Writing relative distance
                    image = cv2.putText(
                        img = image, 
                        text = str(int(relative_distance_thumb_index*100))+' %',
                        org = (end_x_coordinate_rect+15,55), #coordinates
                        fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale = 0.8, 
                        color = (255,4,163), #RGB
                        thickness = 2, 
                        lineType = cv2.LINE_AA
                    )
                    
                    # The servo will contract the closest to 1 and expand the closest to 
                    # 0, so we will get the complementary of 1 to the module
                    module = 1 - relative_distance_thumb_index
                    
        # Converting it back to BGR so we can display using opencv
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Display the output frame of the webcam
        cv2.imshow('Hand Tracking', image)                        
        
        if arduino_mode==1:
            # Condition to not write old angles to the servo in case we don't 
            # have hands in the screen
            if 'Right' not in handedness_detected:
                module = None
            if 'Left' not in handedness_detected:
                gesture = None
            
            # Triggering the servo motor
            if (gesture != None and module != None):    
                board.digital[articulation_dict[gesture]['pin']].write(module*90*articulation_dict[gesture]['fator'])
        
        # - If 'q' is pressed the window is closed;
        key = cv2.waitKey(10)
        if key==ord('q'):
            break

cap.release()
# Destroy all the windows
cv2.destroyAllWindows()