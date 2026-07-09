# Real-Time Robotic Arm Control using MediaPipe Hand Tracking

A computer vision-based robotic arm control system that enables real-time hand gesture control using **MediaPipe**, **OpenCV**, and an **ESP32** over Wi-Fi. The project demonstrates an intuitive human-robot interaction pipeline by translating hand movements captured from a webcam into robotic arm motions.

---

## Overview

This project combines computer vision and embedded systems to create a wireless robotic arm control interface.

Using a standard webcam, the system detects hand landmarks with MediaPipe and maps them to robotic arm movements. Motion commands are transmitted wirelessly to an ESP32, which controls the actuators in real time.

### Key Features

- Real-time hand landmark detection
- Wireless communication with ESP32 over Wi-Fi
- Low-latency robotic arm control
- Computer vision-based human-robot interaction
- Modular software architecture
- OpenCV visualization and debugging

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
Gesture & Landmark Processing
   │
   ▼
Motion Mapping
   │
   ▼
Wi-Fi Communication
   │
   ▼
ESP32 Controller
   │
   ▼
Servo Motors
   │
   ▼
Robotic Arm
```

---

## Repository Contents

| File | Description |
|------|-------------|
| `vision_control.py` | Main computer vision and control program |
| `esp_wifi.ino` | ESP32 firmware for wireless communication |
| `babyarm_nano.ino` | Arduino Nano firmware |
| `robotic_arm_full_architecture.svg` | System architecture diagram |
| `3d_RoboticArm.f3d` | Fusion 360 CAD model |
| `MPMC_Report_Final.pdf` | Project documentation |

---

## Technologies Used

### Software

- Python
- OpenCV
- MediaPipe
- NumPy

### Hardware

- ESP32
- Arduino Nano
- Servo Motors
- USB Webcam
- Custom Robotic Arm

---

## Installation

Clone the repository

```bash
git clone https://github.com/ashmitsingh7/robotic-arm-vision-control.git
cd robotic-arm-vision-control
```

Install the required Python packages.

```bash
pip install opencv-python mediapipe numpy
```

Upload the appropriate firmware to the ESP32 and Arduino Nano before running the Python application.

Start the vision controller.

```bash
python src/vision_control.py
```

---

## Working Principle

1. Capture live video using a webcam.
2. Detect hand landmarks with MediaPipe.
3. Convert landmark positions into robotic arm commands.
4. Send commands over Wi-Fi to the ESP32.
5. Control the robotic arm in real time.

---

## Applications

- Human-Robot Interaction
- Gesture-Based Robot Control
- Educational Robotics
- Embedded Systems
- Computer Vision
- Robotic Manipulation

---

## Future Improvements

- Inverse Kinematics
- ROS 2 Integration
- Object Detection and Grasping
- Depth Camera Support
- Closed-Loop Position Control
- Multi-Hand Gesture Recognition

---

## License

This project is licensed under the MIT License.

---

## Author

**Ashmit Singh**

B.Tech Electronics Engineering (VLSI Design & Technology)

Interested in Robotics, Computer Vision, Embedded Systems, and Intelligent Automation.

GitHub: https://github.com/ashmitsingh7
