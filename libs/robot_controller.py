"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""


import ev3dev.ev3 as ev3
import time
import math
MAX_SPEED = 900

class Snatch3r(object):

    def __init__(self):
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.beacon_seeker = ev3.BeaconSeeker(channel=1)
        self.pixy = ev3.Sensor(driver_name='pixy-lego')
        assert self.color_sensor
        assert self.ir_sensor
        assert self.pixy
    def drive_inches(self, distance, speed):
        """This is called by m3_drive_inches_via_library and uses its inputs to tell the robot how fast to go and how
        far using a class def'"""
        assert self.left_motor.connected
        assert self.right_motor.connected
        sp = speed
        deg = distance * 90
        self.left_motor.run_to_rel_pos(position_sp=deg, speed_sp=sp, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.right_motor.run_to_rel_pos(position_sp=deg, speed_sp=sp, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        assert self.left_motor.connected
        assert self.right_motor.connected

        time_s = 1
        while time_s != 0:
            if degrees_to_turn > 0:
                self.left_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=-degrees_to_turn*4.3,
                                               stop_action=ev3.Motor.STOP_ACTION_BRAKE)
                self.right_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=degrees_to_turn*4.3,
                                                stop_action=ev3.Motor.STOP_ACTION_BRAKE)
                self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
                self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
                ev3.Sound.beep().wait()
                time_s = 0

            elif degrees_to_turn < 0:
                self.left_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=-degrees_to_turn*4.3,
                                               stop_action=ev3.Motor.STOP_ACTION_BRAKE)
                self.right_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=degrees_to_turn*4.3,
                                                stop_action=ev3.Motor.STOP_ACTION_BRAKE)
                self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
                self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
                ev3.Sound.beep().wait()
                time_s = 0

    def arm_calibration(self):
        assert self.arm_motor.connected
        assert self.touch_sensor
        self.arm_motor.run_forever(speed_sp=MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)

        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

        self.arm_motor.position = 0

    def arm_up(self):

        assert self.arm_motor.connected
        assert self.touch_sensor
        self.arm_motor.run_to_rel_pos(position_sp=14.5 * 360, speed_sp=MAX_SPEED)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

    def arm_close(self):

        assert self.arm_motor.connected
        assert self.touch_sensor
        self.arm_motor.run_to_rel_pos(position_sp=7 * 360, speed_sp=MAX_SPEED)


    def arm_down(self):
        assert self.arm_motor.connected
        self.arm_motor.run_to_abs_pos(position_sp=0)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running


    def loop_forever(self):
        self.running = True
        while self.running:
            time.sleep(0.1)

    def shutdown(self):
        self.running = False

    def forward(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def backward(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    def left(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def right(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    def stop(self):
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')

    def seek_beacon(self):

            forward_speed = 200
            turn_speed = 100

            beacon_seeker = ev3.BeaconSeeker(channel=1)

            while not self.touch_sensor.is_pressed:
                current_heading = beacon_seeker.heading
                current_distance = beacon_seeker.distance
                if current_distance == -128:
                    print("IR Remote not found. Distance is -128")
                    self.stop()
                else:

                    if math.fabs(current_heading) < 2:
                        print("On the right heading. Distance: ", current_distance)
                        if math.fabs(current_distance) == 0:
                            print("you have found the beacon!")
                            self.stop()
                            self.drive_inches(2.7,forward_speed)
                            return True
                        else:
                            self.forward(forward_speed, forward_speed)

                    if 2 < math.fabs(current_heading) < 10:
                        print("Adjusting heading: ", current_heading)
                        if current_heading < 0:
                            self.left(-turn_speed, -turn_speed)
                        else:
                            self.right(-turn_speed, -turn_speed)

                    if math.fabs(current_heading) > 10:
                        print("Heading is too far off to fix: ", current_heading)
                        self.stop()
                        print('Heading too far off')

                time.sleep(0.2)

            print("Abandon ship!")
            self.stop()
            return False
