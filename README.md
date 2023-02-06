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

**P.S.**: the project was developed in group, the other members of the group were responsible for developing the robotics arm with 3D printing and building its electronic with Arduino as microcontroller while **I was responsible for developing the entire code of this repository, doing the computer vision script and its interaction with the Arduino**. For information about the construction of the robotic arm and its design please refer to the [monography.pdf](https://github.com/Brunocds/computer-vision-robot-control/blob/main/reports/monography.pdf) file in the reports folder.
