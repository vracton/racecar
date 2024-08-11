import sys

sys.path.insert(1, "../library")
import racecar_core
import racecar_utils as rc_utils

rc = racecar_core.create_racecar()

max_speed = 0
update_slow_time = 0
show_triggers = False
show_joysticks = False

def start():
    global max_speed
    global update_slow_time
    global show_triggers
    global show_joysticks

    print("Start function called")
    max_speed = 0.25
    update_slow_time = 0.5
    show_triggers = False
    show_joysticks = False

    rc.set_update_slow_time(update_slow_time)
    rc.drive.set_max_speed(max_speed)
    rc.drive.stop()

    # Print start message
    print(
        ">> Test Core: A testing program for the racecar_core library.\n"
        "\n"
        "Controls:\n"
        "    Right trigger = accelerate forward\n"
        "    Left trigger = accelerate backward\n"
        "    Left joystick = turn front wheels\n"
        "    Left bumper = decrease max speed\n"
        "    Right bumper = increase max speed\n"
        "    Left joystick click = print trigger values\n"
        "    Right joystick click = print joystick values\n"
        "    A button = Display color image\n"
        "    B button = Display depth image\n"
        "    X button = Display lidar data\n"
        "    Y button = Display IMU data\n"
    )


def update():
    """
    After start() is run, this function is run every frame until the back button
    is pressed
    """
    global max_speed
    global update_slow_time
    global show_triggers
    global show_joysticks

    # Check if each button was_pressed or was_released
    for button in rc.controller.Button:
        if rc.controller.was_pressed(button):
            print(f"Button [{button.name}] was pressed")
        if rc.controller.was_released(button):
            print(f"Button [{button.name}] was released")

    # Click left and right joystick to toggle showing trigger and joystick values
    left_trigger = rc.controller.get_trigger(rc.controller.Trigger.LEFT)
    right_trigger = rc.controller.get_trigger(rc.controller.Trigger.RIGHT)
    left_joystick = rc.controller.get_joystick(rc.controller.Joystick.LEFT)
    right_joystick = rc.controller.get_joystick(rc.controller.Joystick.RIGHT)

    if rc.controller.was_pressed(rc.controller.Button.LJOY):
        show_triggers = not show_triggers

    if rc.controller.was_pressed(rc.controller.Button.RJOY):
        show_joysticks = not show_joysticks

    if show_triggers:
        print(f"Left trigger: [{left_trigger}]; Right trigger: [{right_trigger}]")

    if show_joysticks:
        print(f"Left joystick: [{left_joystick}]; Right joystick: [{right_joystick}]")

    


def update_slow():
    # Check if each button is_down
    for button in rc.controller.Button:
        if rc.controller.is_down(button):
            print(f"Button [{button.name}] is down")

if __name__ == "__main__":
    rc.set_start_update(start, update, update_slow)
    rc.go()