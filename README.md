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
