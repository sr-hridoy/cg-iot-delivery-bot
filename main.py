import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Global variables
is_emergency = False
# Start the bot inside the new Pharmacy room facing downwards
bot_x = 150.0  
bot_y = 480.0  
bot_angle = -90.0 

# Cohen-Sutherland Clipping Region Codes
INSIDE = 0 
LEFT = 1   
RIGHT = 2  
BOTTOM = 4 
TOP = 8    

# Hospital Outer Boundary Limits (Clipping Window)
X_MIN = 50
X_MAX = 750
Y_MIN = 50
Y_MAX = 550

def init():
    glClearColor(0.12, 0.12, 0.12, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluOrtho2D(0, 800, 0, 600)
    glMatrixMode(GL_MODELVIEW) 

def draw_hospital_rooms():
    global is_emergency
    
    # 1. Pharmacy / Base Station (Top Left)
    glColor3f(0.2, 0.2, 0.3) # Dark Blue-Gray
    glBegin(GL_QUADS)
    glVertex2f(50, 350); glVertex2f(300, 350)
    glVertex2f(300, 550); glVertex2f(50, 550)
    glEnd()

    # 2. General Ward - Non-Emergency (Bottom Right)
    glColor3f(0.15, 0.4, 0.6) # Standard Blue
    glBegin(GL_QUADS)
    glVertex2f(500, 200); glVertex2f(750, 200)
    glVertex2f(750, 350); glVertex2f(500, 350)
    glEnd()

    # 3. ICU / Target Room (Top Right)
    # What it does: Fills the target ICU room with red if the alarm is active.
    # Why it is needed: Visual dashboard indicator for urgent care routing.
    # Real-world application: Smart caregiver monitoring system dashboards.
    if is_emergency:
        glColor3f(0.8, 0.1, 0.1) # Bright Red
    else:
        glColor3f(0.2, 0.6, 0.2) # Safe Green
        
    glBegin(GL_QUADS)
    glVertex2f(500, 350); glVertex2f(750, 350)
    glVertex2f(750, 550); glVertex2f(500, 550)
    glEnd()

    # Draw solid borders for all rooms
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(3.0)
    
    # Pharmacy Border
    glBegin(GL_LINE_STRIP)
    glVertex2f(300, 550); glVertex2f(300, 350); glVertex2f(50, 350)
    glEnd()
    
    # General Ward Border
    glBegin(GL_LINE_LOOP)
    glVertex2f(500, 200); glVertex2f(750, 200)
    glVertex2f(750, 350); glVertex2f(500, 350)
    glEnd()
    
    # ICU Border
    glBegin(GL_LINE_LOOP)
    glVertex2f(500, 350); glVertex2f(750, 350)
    glVertex2f(750, 550); glVertex2f(500, 550)
    glEnd()

def draw_hospital_layout():
    glColor3f(1.0, 1.0, 1.0) 
    glLineWidth(3.0)
    
    glBegin(GL_LINES)
    # Outer Boundary walls
    glVertex2f(X_MIN, Y_MIN); glVertex2f(X_MAX, Y_MIN)
    glVertex2f(X_MAX, Y_MIN); glVertex2f(X_MAX, Y_MAX)
    glVertex2f(X_MAX, Y_MAX); glVertex2f(X_MIN, Y_MAX)
    glVertex2f(X_MIN, Y_MAX); glVertex2f(X_MIN, Y_MIN)
    
    # Bottom Corridor Line
    glVertex2f(50, 200); glVertex2f(500, 200)
    glEnd()

def draw_bezier_curve():
    global is_emergency
    
    if not is_emergency:
        return
        
    # Updated coordinates to navigate out of the Pharmacy and into the ICU
    p0 = (150, 450) # Start in Pharmacy
    p1 = (150, 275) # Drive down into the main corridor
    p2 = (625, 275) # Drive right through the corridor
    p3 = (625, 450) # Turn up into the ICU
    
    glColor3f(1.0, 0.8, 0.0) 
    glLineWidth(2.5)
    
    glBegin(GL_LINE_STRIP)
    for i in range(101):
        t = i / 100.0
        x = ((1-t)**3 * p0[0]) + (3 * (1-t)**2 * t * p1[0]) + (3 * (1-t) * t**2 * p2[0]) + (t**3 * p3[0])
        y = ((1-t)**3 * p0[1]) + (3 * (1-t)**2 * t * p1[1]) + (3 * (1-t) * t**2 * p2[1]) + (t**3 * p3[1])
        glVertex2f(x, y)
    glEnd()

def compute_region_code(x, y):
    code = INSIDE
    if x < X_MIN: code |= LEFT
    elif x > X_MAX: code |= RIGHT
    if y < Y_MIN: code |= BOTTOM
    elif y > Y_MAX: code |= TOP
    return code

def cohen_sutherland_clip(x1, y1, x2, y2):
    code1 = compute_region_code(x1, y1)
    code2 = compute_region_code(x2, y2)
    accept = False

    while True:
        if code1 == 0 and code2 == 0:
            accept = True
            break
        elif (code1 & code2) != 0:
            break
        else:
            x = 1.0
            y = 1.0
            code_out = code1 if code1 != 0 else code2

            if code_out & TOP:
                x = x1 + (x2 - x1) * (Y_MAX - y1) / (y2 - y1) if (y2 - y1) != 0 else x1
                y = Y_MAX
            elif code_out & BOTTOM:
                x = x1 + (x2 - x1) * (Y_MIN - y1) / (y2 - y1) if (y2 - y1) != 0 else x1
                y = Y_MIN
            elif code_out & RIGHT:
                y = y1 + (y2 - y1) * (X_MAX - x1) / (x2 - x1) if (x2 - x1) != 0 else y1
                x = X_MAX
            elif code_out & LEFT:
                y = y1 + (y2 - y1) * (X_MIN - x1) / (x2 - x1) if (x2 - x1) != 0 else y1
                x = X_MIN

            if code_out == code1:
                x1, y1 = x, y
                code1 = compute_region_code(x1, y1)
            else:
                x2, y2 = x, y
                code2 = compute_region_code(x2, y2)
                
    if accept:
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)

def draw_sensors():
    global bot_x, bot_y, bot_angle
    
    sensor_length = 150.0
    glColor3f(0.0, 1.0, 0.5) 
    glLineWidth(1.5)
    
    glBegin(GL_LINES)
    for angle_offset in [-25, 0, 25]:
        rad = math.radians(bot_angle + angle_offset)
        end_x = bot_x + sensor_length * math.cos(rad)
        end_y = bot_y + sensor_length * math.sin(rad)
        cohen_sutherland_clip(bot_x, bot_y, end_x, end_y)
    glEnd()

def draw_bot():
    global bot_x, bot_y, bot_angle
    
    # What it does: Translates and rotates the delivery robot based on user input to simulate movement.
    # Why it is needed: To dynamically change the bot's position and orientation on the 2D plane using matrix transformations.
    # Real-world application: Automated Guided Vehicles (AGVs) navigating through warehouse or hospital floors.
    
    glPushMatrix() 
    glTranslatef(bot_x, bot_y, 0.0)
    glRotatef(bot_angle, 0.0, 0.0, 1.0)
    
    # 1. Wheels (Dark Gray)
    glColor3f(0.2, 0.2, 0.2) 
    glBegin(GL_QUADS)
    glVertex2f(-8, 14); glVertex2f(8, 14)
    glVertex2f(8, 18); glVertex2f(-8, 18)
    glVertex2f(-8, -18); glVertex2f(8, -18)
    glVertex2f(8, -14); glVertex2f(-8, -14)
    glEnd()

    # 2. Main Octagon Body (Light Gray / Medical White)
    glColor3f(0.9, 0.9, 0.9) 
    glBegin(GL_POLYGON)
    glVertex2f(-12, -8); glVertex2f(-12, 8)
    glVertex2f(-8, 12); glVertex2f(8, 12)
    glVertex2f(12, 8); glVertex2f(12, -8)
    glVertex2f(8, -12); glVertex2f(-8, -12)
    glEnd()

    # 3. Medical Red Cross Logo on top
    glColor3f(0.8, 0.1, 0.1) 
    glBegin(GL_QUADS)
    # Vertical bar
    glVertex2f(-2, -6); glVertex2f(2, -6)
    glVertex2f(2, 6); glVertex2f(-2, 6)
    # Horizontal bar
    glVertex2f(-6, -2); glVertex2f(6, -2)
    glVertex2f(6, 2); glVertex2f(-6, 2)
    glEnd()

    # 4. Front Sensor Scanner (Cyan)
    glColor3f(0.0, 0.8, 1.0) 
    glBegin(GL_QUADS)
    glVertex2f(12, -5); glVertex2f(16, -5)
    glVertex2f(16, 5); glVertex2f(12, 5)
    glEnd()
    
    glPopMatrix() 

def keyboard_listener(key, x, y):
    global is_emergency
    if key == b'e' or key == b'E':
        is_emergency = not is_emergency
        glutPostRedisplay()

def special_key_listener(key, x, y):
    global bot_x, bot_y, bot_angle
    
    speed = 10.0
    rotation_speed = 5.0
    next_x = bot_x
    next_y = bot_y
    
    if key == GLUT_KEY_UP:
        bot_angle += rotation_speed
    elif key == GLUT_KEY_DOWN:
        bot_angle -= rotation_speed
        
    elif key == GLUT_KEY_RIGHT:
        rad = math.radians(bot_angle)
        next_x = bot_x + speed * math.cos(rad)
        next_y = bot_y + speed * math.sin(rad)
    elif key == GLUT_KEY_LEFT:
        rad = math.radians(bot_angle)
        next_x = bot_x - speed * math.cos(rad)
        next_y = bot_y - speed * math.sin(rad)

    # Collision boundary check
    if (X_MIN + 15) < next_x < (X_MAX - 15) and (Y_MIN + 15) < next_y < (Y_MAX - 15):
        bot_x = next_x
        bot_y = next_y

    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity() 
    
    draw_hospital_rooms()
    draw_hospital_layout()
    draw_bezier_curve() 
    
    draw_sensors() 
    draw_bot() 
    
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"IoT Medicine Delivery Robot Simulation")
    
    init()
    
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard_listener) 
    glutSpecialFunc(special_key_listener) 
    
    glutMainLoop()

if __name__ == "__main__":
    main()