# Gesture Recognition to Control a Robotic Arm

## Project Overview 

This project was developed as a undergradutate dissertation for the Instrumentation, Automation and Robotics Engineering course at the Federal University of ABC (UFABC).

The goal of this project is to control entirely by computer vision a robotic arm developed using 3D printing and electronics with Arduino as microcontroller, controlling the joints of the robotic arm by capturing dynamic images of both hands of an operator. 

![tg (2)](https://user-images.githubusercontent.com/21988243/216859550-2ce9c3ab-a173-4321-9151-e3057e26f753.gif)

The left hand is responsible for indicating which joint will be moved by through a preconfigured gesture while the right hand is responsible for controlling joint expansion and contraction.

The joint to be controlled is selected according to the gestures below:

|                                                     Gesture                                                     |  Joint |
|:---------------------------------------------------------------------------------------------------------------:|:------:|
| ![image](https://user-images.githubusercontent.com/21988243/216859724-1a280361-cd66-4fb7-bfc4-12f60466469d.png) |  Wrist |
| ![image](https://user-images.githubusercontent.com/21988243/216859765-6505d3da-10bd-4140-96a3-855d32de1e1c.png) |  Thumb |
| ![image](https://user-images.githubusercontent.com/21988243/216859796-c2c76a18-52bb-413f-b7d9-3108460b4a61.png) |  Index |
| ![image](https://user-images.githubusercontent.com/21988243/216859809-26d539a8-4dc7-4fb7-bea6-2f4e2e4953da.png) | Middle |
| ![image](https://user-images.githubusercontent.com/21988243/216859818-c12ebcb0-889c-41b5-aa30-126806a4085a.png) |  Ring  |
| ![image](https://user-images.githubusercontent.com/21988243/216859822-6c409318-c611-495a-bac4-5eaaffbca52a.png) |  Pinky |

The expansion and contraction of the joint selected by the left hand is controlled by the distance between the thumb and index finger of the right hand, being that the greater the distance between these two fingers, the greater will be the expansion of the joint until
maximum expansion or maximum contraction occurs, as shown below:

![diversos-graus](https://user-images.githubusercontent.com/21988243/216860314-194199ea-ea06-4f00-9d69-bf5e62d8cf5e.png)

P.S.: the project was developed in group, the other members of the group were responsible for developing the robotics arm with 3D printing and building its electronic with Arduino as microcontroller while I was responsible for developing the entire code of this repository, doing the computer vision script and its interaction with the Arduino.
