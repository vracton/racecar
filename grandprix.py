#   /$$$$$$                                     /$$       /$$$$$$$           /$$                               /$$$$$$$$                                        /$$    /$$$$$$ 
#  /$$__  $$                                   | $$      | $$__  $$         |__/                              |__  $$__/                                      /$$$$   /$$__  $$
# | $$  \__/  /$$$$$$  /$$$$$$  /$$$$$$$   /$$$$$$$      | $$  \ $$ /$$$$$$  /$$ /$$   /$$                       | $$  /$$$$$$   /$$$$$$  /$$$$$$/$$$$       |_  $$  |__/  \ $$
# | $$ /$$$$ /$$__  $$|____  $$| $$__  $$ /$$__  $$      | $$$$$$$//$$__  $$| $$|  $$ /$$/       /$$$$$$         | $$ /$$__  $$ |____  $$| $$_  $$_  $$        | $$    /$$$$$$/
# | $$|_  $$| $$  \__/ /$$$$$$$| $$  \ $$| $$  | $$      | $$____/| $$  \__/| $$ \  $$$$/       |______/         | $$| $$$$$$$$  /$$$$$$$| $$ \ $$ \ $$        | $$   /$$____/ 
# | $$  \ $$| $$      /$$__  $$| $$  | $$| $$  | $$      | $$     | $$      | $$  >$$  $$                        | $$| $$_____/ /$$__  $$| $$ | $$ | $$        | $$  | $$      
# |  $$$$$$/| $$     |  $$$$$$$| $$  | $$|  $$$$$$$      | $$     | $$      | $$ /$$/\  $$                       | $$|  $$$$$$$|  $$$$$$$| $$ | $$ | $$       /$$$$$$| $$$$$$$$
#  \______/ |__/      \_______/|__/  |__/ \_______/      |__/     |__/      |__/|__/  \__/                       |__/ \_______/ \_______/|__/ |__/ |__/      |______/|________/

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
COLOR_PRIORITY = [GREEN, RED, BLUE]
MAX_SPEED = 0.6
kP = 1.5

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
    global initCrop
    if not preserveAngle:
        contour_center = (10,320)
    if image is None:
        contour_center = None
        contour_area = 0
    else:
        depthImage = rc.camera.get_depth_image()
        image = rc_utils.crop(image, (250,0+200*initCrop), (rc.camera.get_height(),rc.camera.get_width()))
        depthImage = rc_utils.crop(depthImage, (250,0), (rc.camera.get_height(),rc.camera.get_width()))
        hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        allContours = []
        backup = []
        for i in COLOR_PRIORITY:
            mask=cv.inRange(hsv,i[0],i[1])
            contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                #first red so change stuff
                if i[0][0]==0:
                    color = "red"
                test = []
                for j in contours:
                    test.append([j, i[2]])
                    backup.append([j, i[2]])
                    #rc_utils.draw_contour(image,j)
                c = rc_utils.get_largest_contour(contours)
                if c is not None:
                    if cv.contourArea(c) > 1500 or i[0]==90:
                        allContours = test
                        break
        if len(allContours)==0 and len(backup)>0:
            allContours = backup
        if color=="red":
            mask=cv.inRange(hsv,BLUE[0],BLUE[1])
            contours, _ = cv.findContours(mask, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                #first green so change stuff
                test = []
                for j in contours:
                    test.append([j, i[2]])
                    backup.append([j, i[2]])
                    #rc_utils.draw_contour(image,j)
                c = rc_utils.get_largest_contour(contours)
                if c is not None:
                    if cv.contourArea(c) > 1500 or i[0]==90:
                        allContours = test
    largest = None
    followColor = None
    for i in allContours:
        tCenter = rc_utils.get_contour_center(i[0])
        if cv.contourArea(i[0]) > contour_area:
            if depthImage[int(tCenter[0])][int(tCenter[1])] < 100:
                contour_area = cv.contourArea(i[0])
                contour_center=tCenter
                followColor = i[1]
                largest = i[0]
            else:
                pass
    if followColor == "green":
        speedMult = 0.7*0.8/MAX_SPEED
        preserveAngle = False
        initCrop = 0
    if contour_area < 500:
        speedMult = -1
        #print("lower")
    else:
        if followColor != "blue":
            speedMult = 0.7*0.8/MAX_SPEED
        else:
            speedMult = 1
    if largest is not None:
        rc_utils.draw_contour(image,largest)
    if contour_center is not None:
        rc_utils.draw_circle(image, contour_center)
    rc.display.show_color_image(image)

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
        """
   ___                  _   ___     _             _____                 _ ___ 
  / __|_ _ __ _ _ _  __| | | _ \_ _(_)_ __  ___  |_   _|__ __ _ _ __   / |_  )
 | (_ | '_/ _` | ' \/ _` | |  _/ '_| \ \ / |___|   | |/ -_) _` | '  \  | |/ / 
  \___|_| \__,_|_||_\__,_| |_| |_| |_/_\_\         |_|\___\__,_|_|_|_| |_/___|
        """
    )
#0.5 = 2.5, 0,3
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