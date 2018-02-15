import mqtt_remote_method_calls as com
import robot_controller as robo
import robot_controller as robo
import ev3dev.ev3 as ev3

class DataContainer(object):
    """ Helper class that might be useful to communicate between different callbacks."""

    def __init__(self):
        self.running = True

def main():
    robot = robo.Snatch3r()
    dc = DataContainer()
    btn = ev3.Button()
    btn.on_backspace = lambda state: handle_shutdown(state, dc)
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    # mqtt_client.connect_to_pc("35.194.247.175")  # Off campus IP address of a GCP broker
    while dc.running:
        btn.process()  # Calls a function that has a while True: loop within it to avoid letting the program end.


def handle_shutdown(button_state, dc):
        """
        Exit the program.

        Type hints:
          :type button_state: bool
          :type dc: DataContainer
        """
        if button_state:
            ev3.Sound.speak("Goodbye").wait()
            dc.running = False
# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
