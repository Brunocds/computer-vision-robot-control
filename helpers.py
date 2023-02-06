from itertools import chain
import cv2
import numpy as np
import mediapipe as mp
import argparse

def get_coordinates(joint, hand_index, results, video_width, video_height):
    """
    Params:
        joint: the joint name (WRIST, THUMB_CMC, INDEX_FINGER_MCP, etc)
        hand_index = the positional index of the hand identified in the 
        results.multi_hand_landmarks list. If two hands were detected 
        for example, the hand in the second position of the array will 
        have index 1, and the first index 0
        results = the output of mp.solutions.hands.Hands(...).process(image)
        video_width = the width of the video output. Usually gotten from 
        cap.get(cv2.CAP_PROP_FRAME_WIDTH) 
        video_height = the height of the video output. Usually gotten from 
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    Outputs:
        (x,y)
            - x -> x axis coordinate in pixel 
            - y -> y axis coordinate in pixel
    """
    normalized_coordinates = results.multi_hand_landmarks[hand_index].landmark[mp.solutions.hands.HandLandmark[joint]]
    coordinates = tuple(
                      np.multiply(
                          [normalized_coordinates.x, normalized_coordinates.y],
                          [video_width,video_height]
                      ).astype(int)
                  )
    return coordinates

def get_handedness(hand_index, results):
    """
    Params:
        hand_index = the positional index of the hand identified in the 
        results.multi_hand_landmarks list. If two hands were detected 
        for example, the hand in the second position of the array will 
        have index 1, and the first index 0
        results = the output of mp.solutions.hands.Hands(...).process(image)
        video_width = the width of the video output. Usually gotten from 
        cap.get(cv2.CAP_PROP_FRAME_WIDTH) 
        video_height = the height of the video output. Usually gotten from 
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    Outputs:
        - handedness = if the hand is 'left' or 'right'        
        
    Observation: the results.multi_hand_landmarks is an array in which each 
    element represents one hand, and each hand will have an array with 21 
    coordinates of the hand landmarks. The results.multi_handedness is similar, 
    is an array in which each element represents one hand and each hand will have 
    a label with the handedness and the score of the classification. 
    The relationship between both is based on the position of the hand in the array, 
    for example the results.multi_hand_landmarks[0] will have the landmarks of the 
    same hand in the results.multi_handedness[0]
    """
    output = None
  
    # Getting handedness label
    label = results.multi_handedness[hand_index].classification[0].label
    #score = round(results.multi_handedness[hand_index].classification[0].score,2)
    output = f'{label}'

    return output

def draw_normalized_coordinates(image, coordinates, normalized_coordinates):
    """
    Params:
        image = the image to draw the normalized coordinates 
        coordinates = list of tuples containing the original coordinates in 
        which the normalized coordinates will be drawn
        normalized_coordinates = list of tuples with the coordinates normalized
    
    Outputs:
        - handedness = if the hand is 'left' or 'right'
    """
    for coordinate, normalized_coordinate in zip(coordinates,normalized_coordinates):    
        norm_x, norm_y = normalized_coordinate
        image = cv2.putText(
            img = image, 
            text = f'x:{norm_x} y:{norm_y}',
            org = coordinate, 
            fontFace = cv2.FONT_HERSHEY_SIMPLEX,
            fontScale = 0.4, 
            color = (255,255,255), 
            thickness = 1, 
            lineType = cv2.LINE_AA
        )
    return image 

def pre_process_hand_landmarks(hand_index, results, video_width, video_height):
    """
    Params:
        hand_index = the positional index of the hand identified in the 
        results.multi_hand_landmarks list. If two hands were detected 
        for example, the hand in the second position of the array will 
        have index 1, and the first index 0
        results = the output of mp.solutions.hands.Hands(...).process(image)
        video_width = the width of the video output. Usually gotten from 
        cap.get(cv2.CAP_PROP_FRAME_WIDTH) 
        video_height = the height of the video output. Usually gotten from 
        cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    Output:
        processed_hand_landmarks: flatten, normalized and traslated coordinates
        that will be used as input for the MLP model. Is an array with 42 points, 
        ordered by the joint index, in the following way -> [wrist.x, wrist.y, 
        thumb_cmc.x, thumb_cmc.y, ..., pinky_dip.x, pinky_dip.y, pinky_dip.x, 
        pinky_dip.y].
    """
    # Extract the x and y coordinates from the results
    hand_landmarks_coordinates = []
    for coordinates in results.multi_hand_landmarks[hand_index].landmark:
        x_coord = coordinates.x * video_width
        y_coord = coordinates.y * video_height
        hand_landmarks_coordinates.append((x_coord, y_coord))

    # Translate the coordinates making the wrist coordinates the origin
    hand_landmarks_translated_coordinates = []
    for idx, coordinate_pair in enumerate(hand_landmarks_coordinates):
        if idx==0:
            base_coordinate_pair = coordinate_pair
            hand_landmarks_translated_coordinates.append((0,0))
        else:
            translated_coordinate_pair = np.subtract(coordinate_pair, base_coordinate_pair)
            hand_landmarks_translated_coordinates.append(tuple(translated_coordinate_pair))
        
    # Flat array and normalize all coordinates using the min-max normalization   
    flatted_hand_landmarks_translated_coordinates = list(chain.from_iterable(hand_landmarks_translated_coordinates))
    array = np.array(flatted_hand_landmarks_translated_coordinates)
    processed_hand_landmarks = (array-array.min())/(array.max()-array.min())
    
    return processed_hand_landmarks

def get_args():
    """
    Output:
        args: object with the attribute device capturing the int number
        of the device passed by the user when executing the python script. 
        E.g. of usage: 
        $ python3 print-args.py --device 0 
        args.device = 0
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--device", type=int, default=0)
    parser.add_argument("--arduino_mode", type=int, default=0)

    args = parser.parse_args()

    return args