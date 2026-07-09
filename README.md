# 🤖 AI Vision-Based Robotic Arm Control

> A real-time computer vision system that enables intuitive robotic arm control using hand gesture tracking and embedded motor control.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange)
![Arduino](https://img.shields.io/badge/Arduino-Servo%20Control-teal)

---

## Overview

This project implements a **vision-based robotic arm control system** where a user's hand movements are tracked in real time using a webcam and translated into robotic arm motions.

The system combines modern computer vision algorithms with embedded hardware to create a natural Human-Robot Interaction (HRI) interface without requiring traditional joysticks or controllers.

The project was developed as a robotics learning platform covering:

- Computer Vision
- Human Pose Estimation
- Embedded Systems
- Real-Time Serial Communication
- Robotic Manipulation

---

## Features

- ✋ Real-time hand landmark detection
- 🎥 Webcam-based control
- ⚡ Low-latency gesture recognition
- 🤖 Multi-DOF robotic arm control
- 🔌 Arduino-based embedded controller
- 📡 Serial communication between PC and robot
- 🎯 Intuitive human-robot interaction

---

## System Architecture

```
             Webcam
                │
                ▼
        OpenCV Video Stream
                │
                ▼
     MediaPipe Hand Tracking
                │
                ▼
     Gesture Interpretation
                │
                ▼
     Joint Angle Generation
                │
                ▼
        Serial Communication
                │
                ▼
            Arduino
                │
                ▼
         Servo Motor Control
                │
                ▼
          Robotic Arm Motion
```

---

## Tech Stack

### Software

- Python
- OpenCV
- MediaPipe
- NumPy
- PySerial

### Hardware

- Arduino
- Servo Motors
- USB Webcam
- Robotic Arm
- Power Supply

---

## Project Structure

```
robotic-arm-vision-control/

│── Arduino/
│── Python/
│── assets/
│── requirements.txt
│── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/ashmitsingh7/robotic-arm-vision-control.git

cd robotic-arm-vision-control
```

Install dependencies

```bash
pip install -r requirements.txt
```

Upload the Arduino sketch.

Run the Python application.

```bash
python main.py
```

---

## How It Works

1. Webcam captures the user's hand.
2. MediaPipe detects 21 hand landmarks.
3. Landmark positions are converted into joint angles.
4. Commands are transmitted over serial.
5. Arduino receives the commands.
6. Servo motors move the robotic arm accordingly.

---

## Applications

- Human-Robot Interaction
- Educational Robotics
- Gesture-Based Interfaces
- Robotics Research
- Assistive Robotics
- Teleoperation

---

## Future Improvements

- Inverse Kinematics
- ROS2 Integration
- MoveIt Motion Planning
- Object Detection
- Depth Camera Support
- Closed-Loop Feedback Control
- PID Servo Control
- Reinforcement Learning for Motion Planning

---

## Results

- Real-time gesture tracking
- Smooth robotic arm movement
- Low communication latency
- Stable serial interface
- Accurate hand landmark detection

---

## Learning Outcomes

Through this project, I gained practical experience in:

- Computer Vision
- Robotics
- Embedded Programming
- Human-Computer Interaction
- Real-Time Systems
- Serial Communication
- Control Systems

---

## Author

**Ashmit Singh**

B.Tech Electronics Engineering (VLSI Design & Technology)

Robotics | Embedded Systems | Computer Vision | Intelligent Automation

GitHub: https://github.com/ashmitsingh7

LinkedIn: www.linkedin.com/in/ashmitsingh7

---

## License

This project is released under the MIT License.
