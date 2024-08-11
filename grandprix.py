#   /$$$$$$                                     /$$       /$$$$$$$           /$$          
#  /$$__  $$                                   | $$      | $$__  $$         |__/          
# | $$  \__/  /$$$$$$  /$$$$$$  /$$$$$$$   /$$$$$$$      | $$  \ $$ /$$$$$$  /$$ /$$   /$$
# | $$ /$$$$ /$$__  $$|____  $$| $$__  $$ /$$__  $$      | $$$$$$$//$$__  $$| $$|  $$ /$$/
# | $$|_  $$| $$  \__/ /$$$$$$$| $$  \ $$| $$  | $$      | $$____/| $$  \__/| $$ \  $$$$/ 
# | $$  \ $$| $$      /$$__  $$| $$  | $$| $$  | $$      | $$     | $$      | $$  >$$  $$ 
# |  $$$$$$/| $$     |  $$$$$$$| $$  | $$|  $$$$$$$      | $$     | $$      | $$ /$$/\  $$
#  \______/ |__/      \_______/|__/  |__/ \_______/      |__/     |__/      |__/|__/  \__/

import sys
import cv2 as cv
import numpy as np
sys.path.insert(1, "../../library")
import racecar_core
import racecar_utils as rc_utils

rc = racecar_core.create_racecar()

BLUE = [(90, 120, 120), (120, 255, 255),"blue"]  # The HSV range for the color blue
GREEN = [(60,150,50), (80,255,255),"green"]  # The HSV range for the color green
RED = [(0,150,150), (0,255,255),"red"]  # The HSV range for the color red

# Color priority: Red >> Green >> Blue
COLOR_PRIORITY = []
MAX_SPEED = 1
kP = 1

# >> Variables
speed = 0.0  # The current speed of the car
angle = 0.0  # The current angle of the car's wheels
contour_center = None  # The (pixel row, pixel column) of contour
contour_area = 0  # The area of contour
cur = 0


#  /$$$$$$$$                              /$$     /$$                              
# | $$_____/                             | $$    |__/                              
# | $$    /$$   /$$ /$$$$$$$   /$$$$$$$ /$$$$$$   /$$  /$$$$$$  /$$$$$$$   /$$$$$$$
# | $$$$$| $$  | $$| $$__  $$ /$$_____/|_  $$_/  | $$ /$$__  $$| $$__  $$ /$$_____/
# | $$__/| $$  | $$| $$  \ $$| $$        | $$    | $$| $$  \ $$| $$  \ $$|  $$$$$$ 
# | $$   | $$  | $$| $$  | $$| $$        | $$ /$$| $$| $$  | $$| $$  | $$ \____  $$
# | $$   |  $$$$$$/| $$  | $$|  $$$$$$$  |  $$$$/| $$|  $$$$$$/| $$  | $$ /$$$$$$$/
# |__/    \______/ |__/  |__/ \_______/   \___/  |__/ \______/ |__/  |__/|_______/ 

speedMult = 1
counter = 0
preserveAngle = True
initCrop = 1
def update_contour():
    global contour_center
    global contour_area
    global cur
    global speedMult
    global counter
    global preserveAngle
    counter+=rc.get_delta_time()

    image = rc.camera.get_color_image()
    allContours = []
    contour_area = 0
    color = ""
    

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

def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    global speed
    global angle
    global speedMult

    update_contour()

    rc.drive.set_max_speed(MAX_SPEED)
    if contour_center is not None:
        pidError = rc_utils.clamp(kP * (((contour_center[1]+200*initCrop) / (rc.camera.get_width()) * 2)-1), -1, 1)
        pidDrive = (kP * pidError)
        angle = rc_utils.clamp(pidDrive, -1, 1)

    speed = speedMult
    rc.drive.set_speed_angle(speed, angle)

def update_slow():
    # Print a line of ascii text denoting the contour area and x-position
    if rc.camera.get_color_image() is None:
        # If no image is found, print all X's and don't display an image
        print("X" * 10 + " (No image) " + "X" * 10)
    else:
        # If an image is found but no contour is found, print all dashes
        if contour_center is None:
            print("-" * 32 + " : area = " + str(contour_area))

        # Otherwise, print a line of dashes with a | indicating the contour x-position
        else:
            s = ["-"] * 32
            s[int(contour_center[1] / 20)] = "|"
            print("".join(s) + " : area = " + str(contour_area))

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()