import sys
import cv2 as cv
import numpy as np

# If this file is nested inside a folder in the labs folder, the relative path should
# be [1, ../../library] instead.
sys.path.insert(1, "../../library")
import racecar_core
import racecar_utils as rc_utils

########################################################################################
# Global variables
########################################################################################

rc = racecar_core.create_racecar()

# >> Constants
# The smallest contour we will recognize as a valid contour (Adjust threshold!)
MIN_CONTOUR_AREA = 10

# TODO Part 1: Determine the HSV color threshold pairs for ORANGE, GREEN, RED, YELLOW, and PURPLE
# Colors, stored as a pair (hsv_min, hsv_max)
BLUE = [(90, 150, 150), (120, 255, 255),"blue"]  # The HSV range for the color blue
GREEN = [(45,50,50), (75,255,255),"green"]  # The HSV range for the color green
RED = [(0,50,50), (10,255,255),"red"]  # The HSV range for the color red
ORANGE = [(10,50,50), (20,255,255),"orange"] # The HSV range for the color orange
YELLOW = [(20,50,50), (30,255,255),"yellow"] # The HSV range for the color yellow
PURPLE = [(140,50,50), (160,255,255),"purple"] # The HSV range for the color purple

# >> Variables
contour_center = None  # The (pixel row, pixel column) of contour
contour_area = 0  # The area of contour
alreadyHandled = False

queue = [] # The queue of instructions
stoplight_color = "" # The current color of the stoplight

########################################################################################
# Functions
########################################################################################

# [FUNCTION] Finds contours in the current color image and uses them to update 
# contour_center and contour_area
def update_contour():
    global contour_center
    global contour_area
    global alreadyHandled

    image = rc.camera.get_color_image()

    if image is None:
        contour_center = None
        contour_area = 0
    else:
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        allContours = []
        for i in [BLUE, GREEN, ORANGE, PURPLE, YELLOW, RED]:
            mask=cv.inRange(hsv,i[0],i[1])
            contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
            for j in contours:
                allContours.append([j, i[2]])
            cv.drawContours(image, contours, -1, i[1], 3)
        # TODO Part 2: Search for line colors, and update the global variables
        # contour_center and contour_area with the largest contour found
        contour_area = 0
        stoplight_color="none"
        for i in allContours:
            if cv.contourArea(i[0]) > contour_area:
                contour_area = cv.contourArea(i[0])
                contour_center=rc_utils.get_contour_center(i[0])
                stoplight_color = i[1]
        if contour_area > 27000 or ((stoplight_color!="blue" and stoplight_color!="orange" and stoplight_color!="green") and contour_area>23000):
            if not alreadyHandled:
                alreadyHandled = True
                if stoplight_color == "blue":
                    turnRight()
                elif stoplight_color=="orange":
                    turnLeft()
                elif stoplight_color=="green":
                    goStraight()
                else:
                    stopNow()
        else:
            alreadyHandled = False
            if contour_area >500 and len(queue)==0:
                queue.append([0.01,1,0])
        # TODO Part 3: Repeat the search for all potential traffic light colors,
        # then select the correct color of traffic light detected.

        # Display the image to the screen
        #image = rc_utils.crop(image, (0,0), (rc.camera.get_height(),rc.camera.get_width()))
        #rc.display.show_color_image(image)

# [FUNCTION] The start function is run once every time the start button is pressed
def start():

    # Set initial driving speed and angle
    rc.drive.set_speed_angle(0,0)

    # Set update_slow to refresh every half second
    rc.set_update_slow_time(0.5)

    # Print start message (You may edit this to be more informative!)
    print(
        ">> Lab 3 - Stoplight Challenge\n"
        "\n"
        "Controls:\n"
        "   A button = print current speed and angle\n"
        "   B button = print contour center and area"
    )

def update_slow():
    pass

# [FUNCTION] After start() is run, this function is run once every frame (ideally at
# 60 frames per second or slower depending on processing speed) until the back button
# is pressed  
def update():
    global queue

    update_contour()

    (lx, ly) = rc.controller.get_joystick(rc.controller.Joystick.LEFT)
    speed = ly
    angle = lx
    rc.drive.set_speed_angle(speed, angle)

    # Print the current speed and angle when the A button is held down
    if rc.controller.is_down(rc.controller.Button.A):
        print("Speed:", speed, "Angle:", angle)

    # Print the center and area of the largest contour when B is held down
    if rc.controller.is_down(rc.controller.Button.B):
        if contour_center is None:
            print("No contour found")
        else:
            print("Center:", contour_center, "Area:", contour_area)

    if len(queue) > 0:
        speed = queue[0][1]
        angle = queue[0][2]
        queue[0][0] -= rc.get_delta_time()
        if queue[0][0] <= 0:
            queue.pop(0)
        # Send speed and angle commands to the RACECAR
        rc.drive.set_speed_angle(speed, angle)

# [FUNCTION] Appends the correct instructions to make a 90 degree right turn to the queue
def turnRight():
    global queue
    queue.append([1.35, 1, 1])
    # TODO Part 4: Complete the rest of this function with the instructions to make a right turn

# [FUNCTION] Appends the correct instructions to make a 90 degree left turn to the queue
def turnLeft():
    global queue
    queue.append([1.225, 1, -1])
    # TODO Part 5: Complete the rest of this function with the instructions to make a left turn

# [FUNCTION] Appends the correct instructions to go straight through the intersectionto the queue
def goStraight():
    global queue

    # TODO Part 6: Complete the rest of this function with the instructions to make a left turn

# [FUNCTION] Clears the queue to stop all actions
def stopNow():
    global queue
    queue.clear()
    queue.append([1, -1, 0])
    queue.append([1,0,0])

########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()