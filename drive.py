import sys

sys.path.insert(0, '../library')
import racecar_core

rc = racecar_core.create_racecar()

counter = 0
def start():
    global counter
    counter = 0
    rc.drive.set_max_speed(0.5)
    rc.drive.stop()

def update():
    global counter

    (lx, ly) = rc.controller.get_joystick(rc.controller.Joystick.LEFT)
    (rx, ry) = rc.controller.get_joystick(rc.controller.Joystick.RIGHT)
    #keyboard
    rc.drive.set_speed_angle(ly, lx)

    #joy cons arcade
    #rc.drive.set_speed_angle(-ly, lx)

    #joy cons tank
    #rc.drive.set_speed_angle(-ly, rx)

    
def update_slow():
    pass

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()
