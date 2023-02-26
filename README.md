# Gesture Recognition to Control a Robotic Arm

## Project Overview 

This project was developed as an undergradutate dissertation for the Instrumentation, Automation and Robotics Engineering course at the Federal University of ABC (UFABC).

The goal of this project is to control entirely by computer vision a robotic arm developed using 3D printing and electronics with Arduino as microcontroller, controlling the joints of the robotic arm by capturing dynamic images of both hands of an operator. 

![tg](https://user-images.githubusercontent.com/21988243/216863371-609cd738-44ab-485f-bbc1-a5000a6fc4ab.gif)

The left hand is responsible for indicating which joint will be moved by through a preconfigured gesture while the right hand is responsible for controlling joint expansion and contraction.

The joint to be controlled is selected according to the gestures below:

<div align="center">
<table>
  <thead>
    <tr>
      <th>Gesture</th>
      <th>Joint</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center"><img src="https://user-images.githubusercontent.com/21988243/216859724-1a280361-cd66-4fb7-bfc4-12f60466469d.png" width=60%></td>
      <td align="center">Wrist</td>
    </tr>
    <tr>
      <td align="center"><img src="https://user-images.githubusercontent.com/21988243/216859765-6505d3da-10bd-4140-96a3-855d32de1e1c.png" style="width:60%"></td>
      <td align="center">Thumb</td>
    </tr>
    <tr>
      <td align="center"><img src="https://user-images.githubusercontent.com/21988243/216859796-c2c76a18-52bb-413f-b7d9-3108460b4a61.png" style="width:60%"></td>
      <td align="center">Index</td>
    </tr>
    <tr>
      <td align="center"><img src="https://user-images.githubusercontent.com/21988243/216859809-26d539a8-4dc7-4fb7-bea6-2f4e2e4953da.png" style="width:60%"></td>
      <td align="center">Middle</td>
    </tr>
    <tr>
      <td align="center"><img src="https://user-images.githubusercontent.com/21988243/216859818-c12ebcb0-889c-41b5-aa30-126806a4085a.png" style="width:60%"></td>
      <td align="center">Ring</td>
    </tr>
    <tr>
      <td align="center"><img src="https://user-images.githubusercontent.com/21988243/216859822-6c409318-c611-495a-bac4-5eaaffbca52a.png" style="width:60%"></td>
      <td align="center">Pinky</td>
    </tr>
  </tbody>
</table>
</div>

The expansion and contraction of the joint selected by the left hand is controlled by the distance between the thumb and index finger of the right hand, being that the greater the distance between these two fingers, the greater will be the expansion of the joint until
maximum expansion or maximum contraction occurs, as shown below:

![diversos-graus](https://user-images.githubusercontent.com/21988243/216860314-194199ea-ea06-4f00-9d69-bf5e62d8cf5e.png)

**P.S.**: the project was done in group, the other members of the group were responsible for developing the robotics arm with 3D printing and building its electronic with Arduino as microcontroller while **I was responsible for developing the entire code of this repository, doing the computer vision script and its interaction with the Arduino**. For information about the construction of the robotic arm and its design please refer to the [monography.pdf](https://github.com/Brunocds/computer-vision-robot-control/blob/main/reports/monography.pdf) file in the reports folder.

## Architecture

The computer vision of the project has the following architecture:

![general-architecture](https://user-images.githubusercontent.com/21988243/216868930-633dfbce-9c69-4331-ab5c-cbc0ba73785a.png)

* **Image capture and processing:** using OpenCV through Python is possible to capture an image from the webcam as a vector or matrix of pixels, each pixel containing information about the values of the red, green and blue colors (from 0 to 255 for each of them) using the RGB system. 
* **Hand recognition:** the matrix of pixels in the previous step is used as input to MediaPipe, a ready-to-use cutting-edge ML solution framework that has in one of its solutions the hand recognition. The output of the MediaPipe is the coordinates x,y and z of 21 joints of the hands identified in the image.
* **Gesture recognition:** a MLP (Multilayer Perceptron) artificial neural network model is trained using the joints coordinates captured by MediaPipe and uses it as input to detect what hand gesture was done.
* **Distance ratio between finger tips:** the coordinates captured by MediaPipe are used to calculate the distance ratio between the thumb and index tips through Python using Numpy and simple geometry. 

## Getting started (on Windows)

1. Clone the source code by running:
```bash
$ git clone https://github.com/Brunocds/computer-vision-robot-control.git
```
2. Navigate to the project root folder by running:
```bash
$ cd computer-vision-robot-control
```
3. Setup a virtual environment:
```bash
$ python -m venv venv 
$ source venv/Scripts/activate
$ pip install -r requirements.txt
```
4. Run the application:
```bash
$ python apply-model.py 
```
When running the application you can specify two options:
* --device: the camera device number used by OpenCV. Usually is 0, but if the code don't run you can try other, e.g.:
 ```bash
 $ python apply-model.py --device 0
 ```
* --arduino_mode: if you'd like to run only the computer vision side of the application use any parameter different than 1 (default is already different than 1). If you'd like to run the application using Arduino, change the ports used by the servo motors in the "articulation_dict" dictionary inside the apply-model.py and the specify the arduino_mode 1, e.g.:
 ```bash
 $ python apply-model.py --arduino_mode 1
 ```
 
 5. When you're done, to quit the opened window just select it and press "Q".
 
 ## Project Structure
 <pre>
├── README.md
├── apply-model.py
├── collect-train-data.py
├── data
│   ├── gesture-label.csv
│   └── training-data.csv
├── helpers.py
├── model
│   └── clf.pkl
├── model-training.ipynb
├── reports
│   └── monography.pdf
└── requirements.txt
</pre>

#### apply-model.py
It's the main program of the application, which can be run using an Arduino or not. 

#### collect-train-data.py
It's the python script used to collect training data for the MLP model training. It is responsible to pre process the coordinates and save then into the **data/training-data.csv** file. 

#### model-training.ipynb
It's a notebook that trains a MLP model using the training-data.csv obtained by the collect-train-data.py. The output of this notebook is the **model/clf.pkl** file, which is imported by the apply-model to identify the hand gesture.  

#### gesture-label.csv
It's a csv file mapping the gestures that the model will identify to numbers, as the MLP model uses numbers as output. The labeling filled in this file will be shown in the image processing. 

#### helpers.py
It's a helper file containing functions used by both apply-model.py and collect-train-data.py.

 ## Model Training

Although the project already contains a trained model for the gestures listed in the project overview, it's possible to use the **collect-train-data.py**, **model-training.ipynb** and **gesture-label.csv** to collect data of other gestures and create and train a new model using it. 
 
### Data Collection 

#### 1. Strategy

As discussed in the archictecure topic the input of the gesture recognition model is the output of the MediaPipe Hands solution, which is the coordinates in width, height and depth of the hand's joints. However for the recognition of gestures the depth is irrelevant because a gesture will be the same regardless of the evaluated depth, so the input data of the model will be the x and y coordinates of each of the 21 joints, totaling 42 entries to result in the classification of one of the six possible gestures, as shown in the example below:

![processing](https://user-images.githubusercontent.com/21988243/221391221-c6e90848-781c-4d33-9f4f-a8926ca4af81.png)

It's not possible to use the raw coordinates gotten from the MediaPipe as input for the model because the coordinates are global based on the position of the hand in the camera view and this way a same gesture will have completely different coordinates if we move the hand position, as shown in the example below for a joint coordinate in a same gesture:

<div align="center"><img src="https://user-images.githubusercontent.com/21988243/221391648-a74d1d7a-8d9f-417d-badf-d1dbc76b0a12.png" width="40%" height="auto"></div>

The input desired to train the model are coordinates that varies only when a gesture change occurs and one way to achieve this is to use relative coordinates. The strategy used to get the relative coordinates is to subtract all coordinates by the coordinates of the wrist, making the wrist coordinate the origin (0,0), and all other coordinates relative to it, as shown in the example below:

<div align="center"><img src="https://user-images.githubusercontent.com/21988243/221392433-d55259f9-be30-4b76-a6c6-14cfa489dd80.png" width="80%" height="auto"></div>

After obtaining the relative coordinates, a good practice to improve the model's performance is to normalize the input data. The objective of normalization is to change the values of the numeric columns to a common scale without causing distortion in the value ranges. This is useful for the perceptron neural network model in question, as it uses linear combinations of inputs and associates weights to them. Since the coordinates can have several distinct value ranges, such as the Y-coordinate of the middle finger having values in the range of 0 to 100 and the thumb having values in the range of 300 to 400, the thumb coordinate can significantly influence the result due to its larger values, not necessarily because it is more important as a predictor. That being said, the method used to normalize the coordinates is the min-max normalization, in which all variables are placed in values between 0 and 1 using the following formula:

$$
coordinate_{scaled}  = \dfrac{coordinate - coordinate_{min}}{coordinate_{max} - coordinate_{min}}
$$

Below there is an example of applying this normalization to the relative coordinates of a hand gesture:

<div align="center"><img src="https://user-images.githubusercontent.com/21988243/221393267-5324cd49-06aa-4dbe-b762-9c7c16a58d62.png" width="70%" height="auto"></div>

#### 2. How to Collect
