# IoT Medicine Delivery & Caregiver Bot Tracker

![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg) ![OpenGL](https://img.shields.io/badge/OpenGL-PyOpenGL-red.svg) ![Computer Graphics](https://img.shields.io/badge/Computer_Graphics-Simulation-green.svg) ![Track B](https://img.shields.io/badge/Track_B-Research_Visualizer-orange.svg)

### 📌 Project Overview
---
This repository contains a 2D Computer Graphics simulation of an autonomous medical delivery robot navigating a hospital floor plan. The project acts as a Research Visualizer to simulate how IoT robots process spatial boundaries, calculate kinematics, and generate navigation algorithms in real-time. 

To ensure mathematical accuracy and hardware-like behavior, the robot's movement and sensor boundaries are strictly calculated using coordinate matrices and bitwise region codes.

### 📊 Simulation Environment
---
The models and environment are rendered using the standard PyOpenGL and GLUT libraries.

*   The hospital architecture is mapped to a 3-zone standard system:
    *   **Pharmacy:** The dark-gray starting base station for the delivery unit.
    *   **General Ward:** Standard blue non-emergency patient rooms.
    *   **ICU (Target Room):** The emergency destination that dynamically alters visual states during caregiver alerts.

### 🧠 Methodology & Architecture
---
*   **2D Transformations (Kinematics):** Utilizes `glTranslatef` and `glRotatef` matrix operations to handle the forward, backward, and rotational movement of the robot based on its local center axis (simulating Automated Guided Vehicle mechanics).
*   **Cohen-Sutherland Line Clipping (Dynamic Sensor FOV):** Implements bitwise operations to calculate 4-bit region codes, mathematically slicing the robot's green LiDAR sensor rays at the exact pixel they intersect with the hospital's outer boundaries.
*   **Bezier Curves (Emergency Routing):** Uses a Cubic Bezier polynomial mathematical equation across four control points to generate a smooth, non-angular delivery trajectory from the pharmacy to the ICU.
*   **Color Fill & Shape Drawing:** Uses OpenGL primitives (`GL_QUADS`, `GL_POLYGON`) to construct the hospital layout and the octagonal bot chassis. Features state-based color filling that instantly floods the ICU room with red pixels when triggered.

### 🚀 Controls & Interaction
---
The simulation achieves real-time interactivity with the following keyboard listener mappings:

| Action | Key / Input | Function |
| :--- | :--- | :--- |
| **Rotate Left** | `UP Arrow` | Rotates the robot counter-clockwise on its axis |
| **Rotate Right** | `DOWN Arrow` | Rotates the robot clockwise on its axis |
| **Move Forward** | `RIGHT Arrow` | Drives forward in the current facing direction |
| **Move Backward** | `LEFT Arrow` | Drives backward in the current facing direction |
| **Toggle Alert** | `E` | Triggers ICU color flood and Bezier routing path |

### ⚙️ Installation & Usage
---
1. Clone the repository:
   ```bash
   git clone [https://github.com/sr-hridoy/cg-iot-delivery-bot.git](https://github.com/sr-hridoy/cg-iot-delivery-bot.git)
   cd cg-iot-delivery-bot
