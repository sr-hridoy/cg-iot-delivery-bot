# IoT Medicine Delivery & Caregiver Bot Tracker

![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyOpenGL](https://img.shields.io/badge/OpenGL-PyOpenGL-red.svg)
![Computer Graphics](https://img.shields.io/badge/Computer%20Graphics-Simulation-green.svg)
![Track B](https://img.shields.io/badge/Track%20B-Research%20Visualizer-orange.svg)

## 📌 Project Overview

This project is a **2D Computer Graphics simulation of a medical delivery robot** navigating through a hospital environment.

The simulation demonstrates how a healthcare delivery robot can move between different hospital zones, detect environmental boundaries, and generate an emergency route to the ICU.

The project focuses on Computer Graphics concepts such as **2D transformations, line clipping, Bezier curves, geometric modeling, keyboard interaction, and state-based color changes**.

> **Note:** This project is a graphical simulation inspired by an IoT-based medical delivery system. It does not represent a physical IoT robot or real medical device.

## 📊 Simulation Environment

The hospital environment is created using **PyOpenGL and GLUT** and contains three main zones:

* **Pharmacy:** The dark-gray starting/base station of the delivery robot.
* **General Ward:** Blue patient-room area used as a normal hospital zone.
* **ICU:** The emergency target room. Its visual state changes when an emergency alert is triggered.

## 🧠 Methodology & Computer Graphics Concepts

### 1. 2D Transformations

The robot uses OpenGL transformation functions such as:

* `glTranslatef()` for movement
* `glRotatef()` for rotation

These transformations allow the robot to move forward/backward according to its current direction and rotate around its center.

### 2. Cohen-Sutherland Line Clipping

The simulation uses the **Cohen-Sutherland line clipping algorithm** to calculate region codes and determine where sensor/FOV lines intersect the hospital boundary.

The algorithm uses **4-bit region codes** to classify points relative to the clipping boundary.

### 3. Cubic Bezier Curve

A **Cubic Bezier Curve** is used to generate a smooth emergency routing path from the Pharmacy toward the ICU.

The curve is calculated using four control points and provides a smoother route than a simple straight-line path.

### 4. OpenGL Shape Drawing

OpenGL primitives such as:

* `GL_QUADS`
* `GL_POLYGON`

are used to construct the hospital environment and the robot body.

The robot is modeled using a polygon-based chassis, while different colors represent different hospital areas and system states.

### 5. State-Based Emergency Alert

When the emergency alert is activated, the ICU changes its visual state and the emergency routing path is displayed.

This represents a simplified caregiver/emergency notification scenario.

## 🚀 Controls & Interaction

| Action | Key / Input | Function |
|---|---|---|
| Rotate Left | `UP Arrow` | Rotates the robot counter-clockwise |
| Rotate Right | `DOWN Arrow` | Rotates the robot clockwise |
| Move Forward | `RIGHT Arrow` | Moves the robot forward |
| Move Backward | `LEFT Arrow` | Moves the robot backward |
| Toggle Emergency Alert | `E` | Changes ICU state and displays the emergency route |

## ⚙️ Installation & Usage

### 1. Clone the Repository

```bash
git clone https://github.com/sr-hridoy/cg-iot-delivery-bot.git
cd cg-iot-delivery-bot
```

### 2. Install Dependencies

Make sure Python 3.8 or later is installed.

Install the required packages:

```bash
pip install PyOpenGL PyOpenGL_accelerate
```

### 3. Run the Project

Run the main Python file:

```bash
python main.py
```

## 📁 Project Structure

```text
cg-iot-delivery-bot/
│
├── .gitignore
├── README.md
└── main.py
```

## 🎯 Learning Objectives

This project demonstrates practical implementation of:

* 2D geometric transformations
* OpenGL primitives
* Keyboard interaction
* Cohen-Sutherland line clipping
* Cubic Bezier curves
* Coordinate systems
* Robot movement and rotation
* State-based graphical changes
* Real-time computer graphics simulation

## 👨‍💻 Author

**Md. Shaifur Rahman Hridoy**

B.Sc. in Computer Science and Engineering
Leading University, Bangladesh

**Focus:** Computer Graphics, Artificial Intelligence & Autonomous Systems

## 📄 License

This project is developed for educational and academic purposes.
