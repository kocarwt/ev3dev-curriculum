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



left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
assert left_motor.connected
assert right_motor.connected

class Snatch3r(object):
    'This is called by m3_drive_inches_via_library and uses its inputs to tell the robot how fast to go and how far using a class def'
    def drive_inches(self, distance, speed):
        sp = speed
        deg = distance * 90
        left_motor.run_to_rel_pos(position_sp=deg, speed_sp=sp, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        right_motor.run_to_rel_pos(position_sp=deg, speed_sp=sp, stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        ev3.Sound.speak("Timed turn").wait()

        time_s = 1
        while time_s != 0:
            if degrees_to_turn > 0:
                left_motor.run_to_rel_pos(speed_sp=turn_speed_sp,position_sp=-degrees_to_turn*4.3,
                                          stop_action=ev3.Motor.STOP_ACTION_BRAKE)
                right_motor.run_to_rel_pos(speed_sp=turn_speed_sp,position_sp=degrees_to_turn*4.3,
                                           stop_action=ev3.Motor.STOP_ACTION_BRAKE)
                left_motor.wait_while(ev3.Motor.STATE_RUNNING)
                right_motor.wait_while(ev3.Motor.STATE_RUNNING)
                ev3.Sound.beep().wait()
                time_s=0


            elif degrees_to_turn < 0:
                left_motor.run_to_rel_pos(speed_sp=turn_speed_sp,position_sp=-degrees_to_turn*4.3,
                                          stop_action=ev3.Motor.STOP_ACTION_BRAKE)
                right_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=degrees_to_turn*4.3,
                                           stop_action=ev3.Motor.STOP_ACTION_BRAKE)
                left_motor.wait_while(ev3.Motor.STATE_RUNNING)
                right_motor.wait_while(ev3.Motor.STATE_RUNNING)
                ev3.Sound.beep().wait()
                time_s=0


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------

