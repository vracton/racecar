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
# The smallest contour we will recognize as a valid contour
MIN_CONTOUR_AREA = 30

# A crop window for the floor directly in front of the car
CROP_FLOOR = ((360, 0), (rc.camera.get_height(), rc.camera.get_width()))

# TODO Part 1: Determine the HSV color threshold pairs for GREEN and RED
# Colors, stored as a pair (hsv_min, hsv_max) Hint: Lab E!
BLUE = [(90, 120, 120), (120, 255, 255),"blue"]  # The HSV range for the color blue
GREEN = [(60,150,50), (80,255,255),"green"]  # The HSV range for the color green
RED = [(0,50,50), (0,255,255),"red"]  # The HSV range for the color red

# Color priority: Red >> Green >> Blue
COLOR_PRIORITY = [BLUE, GREEN, RED, BLUE]

# >> Variables
speed = 0.0  # The current speed of the car
angle = 0.0  # The current angle of the car's wheels
contour_center = None  # The (pixel row, pixel column) of contour
contour_area = 0  # The area of contour
cur = 0


########################################################################################
# Functions
########################################################################################

# [FUNCTION] Finds contours in the current color image and uses them to update 
# contour_center and contour_area
def update_contour():
    global contour_center
    global contour_area
    global cur
    global speedMult

    image = rc.camera.get_color_image()
    allContours = []
    nextContours = []
    contour_area = 0
    ncontour_area = 0
    contour_center = (240,320)
    if image is None:
        contour_center = None
        contour_area = 0
    else:
        image = rc_utils.crop(image, (200,0), (rc.camera.get_height(),rc.camera.get_width()))
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        allContours = []
        for i in [COLOR_PRIORITY[cur]]:
            mask=cv.inRange(hsv,i[0],i[1])
            contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
            for j in contours:
                allContours.append([j, i[2]])
            #cv.drawContours(hsv, contours, -1, i[1], 3)
        if cur<len(COLOR_PRIORITY)-1:
            for i in [COLOR_PRIORITY[cur+1]]:
                mask=cv.inRange(hsv,i[0],i[1])
                contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
                for j in contours:
                    nextContours.append([j, i[2]])
            #cv.drawContours(hsv, contours, -1, i[1], 3)
        else:
            pass
            #search for cone
    largest = None
    for i in allContours:
        if cv.contourArea(i[0]) > contour_area:
            contour_area = cv.contourArea(i[0])
            contour_center=rc_utils.get_contour_center(i[0])
            largest = i[0]
    for i in nextContours:
        if cv.contourArea(i[0]) > ncontour_area:
            ncontour_area = cv.contourArea(i[0])
    if ncontour_area>1300:
        print("switch")
        if cur < len(COLOR_PRIORITY)-1:
            cur+=1
    if largest is not None:
        rc_utils.draw_contour(image,largest)
    rc_utils.draw_circle(image, contour_center)
    rc.display.show_color_image(image)

# [FUNCTION] The start function is run once every time the start button is pressed
def start():
    global speed
    global angle

    # Initialize variables
    speed = 0
    angle = 0

    # Set initial driving speed and angle
    rc.drive.set_speed_angle(speed, angle)

    # Set update_slow to refresh every half second
    rc.set_update_slow_time(0.5)

    # Print start message
    print(
        ">> Lab 2A - Color Image Line Following\n"
        "\n"
        "Controls:\n"
        "   Right trigger = accelerate forward\n"
        "   Left trigger = accelerate backward\n"
        "   A button = print current speed and angle\n"
        "   B button = print contour center and area"
    )
def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    global speed
    global angle
    global pid_integral
    global pidLastError
    global speedMult

    # Search for contours in the current color image
    update_contour()

    # TODO Part 3: Determine the angle that the RACECAR should receive based on the current 
    # position of the center of line contour on the screen. Hint: The RACECAR should drive in
    # a direction that moves the line back to the center of the screen.

    # Choose an angle based on contour_center
    # If we could not find a contour, keep the previous angle
    rc.drive.set_max_speed(0.75)

    # Use the triggers to control the car's speed
    rt = rc.controller.get_trigger(rc.controller.Trigger.RIGHT)
    lt = rc.controller.get_trigger(rc.controller.Trigger.LEFT)
    speed = (rt-lt)*speedMult
    #speed = 1

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


########################################################################################
# DO NOT MODIFY: Register start and update and begin execution
########################################################################################

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()