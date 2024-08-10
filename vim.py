
import sys
sys.path.insert(1, '../../library')
import racecar_core

rc = racecar_core.create_racecar()
counter = 0
isDriving = False

def start():
    global counter
    global isDriving

    counter = 0
    isDriving = False
    rc.drive.stop()

# START MADE WITH VIM
def update():
    global counter
    global isDriving

    if rc.controller.was_pressed(rc.controller.Button.A):
        print("The A button was pressed")
    if rc.controller.was_pressed(rc.controller.Button.B):
        counter = 0
        isDriving = True

    if isDriving:
        counter += rc.get_delta_time()  

        if counter < 1:
            rc.drive.set_speed_angle(1, 0)
        elif counter < 2:
            rc.drive.set_speed_angle(1, 1)
        else:
            rc.drive.stop()
            isDriving = False
# END MADE WITH VIM
def update_slow():
    if rc.controller.is_down(rc.controller.Button.RB):
        print("The right bumper is currently down (update_slow)")

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()
