import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import mqtt_remote_method_calls as com

ISLAND_COLORS = ["Blue", "Green", "Yellow", "Red", "Green"]


class DataContainer(object):
    def __init__(self):
        self.running = True


class MyDelegate(object):
    def __init__(self):
        self.robot = robo.Snatch3r()

    def loop_forever(self):
        self.running = True
        while self.running:
            time.sleep(.1)

    def drive_to_the_island(self, color_to_seek, LED_color_entry):
        btn = ev3.Button
        time.sleep(3)
        while True:
            length = len(str(color_to_seek))
            ev3.Sound.speak("Seeking " + color_to_seek + "Island")
            time.sleep(1)
            if LED_color_entry == "ORANGE":
                ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.ORANGE)
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.ORANGE)
            if LED_color_entry == "RED":
                ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
            if LED_color_entry == "GREEN":
                ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
            if LED_color_entry == "YELLOW":
                ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW)
            if LED_color_entry == "BLACK":
                ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)
            if color_to_seek == "Red":
                color_to_seek = 5
            if color_to_seek == "Yellow":
                color_to_seek = 4
            if color_to_seek == "Green":
                color_to_seek = 3
            if color_to_seek == "Blue":
                color_to_seek = 2
            if color_to_seek == "Green":
                color_to_seek = 1

            self.robot.left_motor.run_forever(speed_sp=200)
            self.robot.right_motor.run_forever(speed_sp=200)
            while True:
                if self.robot.color_sensor.color == color_to_seek:
                    break
                time.sleep(1)
            self.robot.left_motor.stop()
            self.robot.right_motor.stop()
            ev3.Sound.speak("Ship arrived at the " + ISLAND_COLORS[color_to_seek] + "Island")
            self.robot.left_motor.stop()
            self.robot.right_motor.stop()
            ev3.Sound.speak("Searching For Red Island ")
            time.sleep(1)
            self.robot.left_motor.run_forever(speed_sp=200)
            self.robot.right_motor.run_forever(speed_sp=-200)
            drive_time = .2 * length
            time.sleep(drive_time)

            self.robot.left_motor.run_forever(speed_sp=200)
            self.robot.right_motor.run_forever(speed_sp=200)
            while True:
                if self.robot.color_sensor.color == 5:
                    break
            self.robot.left_motor.stop()
            self.robot.right_motor.stop()
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
            ev3.Sound.speak("Ship arrived at the Red Island")
            time.sleep(1)
            self.robot.left_motor.stop()
            self.robot.right_motor.stop()
            ev3.Sound.speak("Searching For Yellow Island ")
            time.sleep(1)
            self.robot.left_motor.run_forever(speed_sp=200)
            self.robot.right_motor.run_forever(speed_sp=200)
            while True:
                if self.robot.color_sensor.color == 4:
                    break
            self.robot.left_motor.stop()
            self.robot.right_motor.stop()
            ev3.Sound.speak("Ship arrived at the Yellow Island")
            time.sleep(1.5)
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW)
            self.robot.left_motor.stop()
            self.robot.right_motor.stop()
            time.sleep(1.5)

            ev3.Sound.speak("Drive into Ocean and Swim around in circles")
            time.sleep(1.5)
            self.robot.left_motor.run_forever(speed_sp=200)
            self.robot.right_motor.run_forever(speed_sp=200)
            while True:
                if self.robot.color_sensor.color == 1:
                    break
            ev3.Sound.speak("In the Ocean")
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)

            ev3.Sound.speak("Swim around in Ocean")
            self.robot.left_motor.run_forever(speed_sp=100)
            self.robot.right_motor.run_forever(speed_sp=100)  # straight
            drive_time = .25 * length
            time.sleep(drive_time)
            self.robot.left_motor.run_forever(speed_sp=500)
            self.robot.right_motor.run_forever(speed_sp=250)  # straight
            drive_time = 6 * length
            time.sleep(drive_time)

            self.robot.left_motor.stop()
            self.robot.right_motor.stop()
            ev3.Sound.speak("Adventure is over")
            time.sleep(3)
            self.robot.stop()
            self.robot.left_motor.stop()
            self.robot.right_motor.stop()


def main():
    print("--------------------------------------------")
    print(" Welcome to the ship adventure")
    print("--------------------------------------------")
    ev3.Sound.speak("Drive to each Island and then swim into the water").wait()
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc("mosquitto.csse.rose-hulman.edu", 8)
    my_delegate.loop_forever()
    robot = robo.Snatch3r()
    dc = DataContainer()


def drive_to_color(button_state, robot, color_to_seek):
    if button_state:
        ev3.Sound.speak("Searching for the " + ISLAND_COLORS[color_to_seek] + "Island").wait()
        robot.left_motor.run_forever(speed_sp=300)
        robot.right_motor.run_forever(speed_sp=300)
        while True:
            if robot.color_sensor.color == color_to_seek:
                robot.left_motor.stop()
                robot.right_motor.stop()
                break
            time.sleep(.01)
        ev3.Sound.speak("Found " + ISLAND_COLORS[color_to_seek]).wait()


# ----------------------------------------------------------------------
# Event handlers
# ----------------------------------------------------------------------

def handle_shutdown(button_state, dc):
    """Exit the program."""
    if button_state:
        dc.running = False


main()
