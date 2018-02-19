import ev3dev.ev3 as ev3
import time
import robot_controller as robo
from PIL import Image
import traceback

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com

class PcDelegate(object):
    def __init__(self):
        self.running = True

def main():
    pc_delegate = PcDelegate()
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3("mosquitto.csse.rose-hulman.edu", 8)

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=30, relief='raised')
    main_frame.grid()

    drive_color = ttk.Label(main_frame, text= "Enter an island to swim to")
    drive_color.grid(row=0, column=0)
    drive_color = ttk.Entry(main_frame, width=5)
    drive_color.insert(0, "Blue")
    drive_color.grid(row=1, column=0)


    LED_color = ttk.Label(main_frame, text= "Enter Starting LED Color ")
    LED_color.grid(row=5, column=0)
    LED_color_entry = ttk.Entry(main_frame, width=5, justify=tkinter.RIGHT)
    LED_color_entry.insert(0, "RED")
    LED_color_entry.grid(row=6, column=0)

    mid_button = ttk.Button(main_frame, text="Drive")
    mid_button.grid(row=4, column=8)
    mid_button['command'] = lambda: buttons(mqtt_client, drive_color, LED_color_entry)

    root.mainloop()

def buttons(mqtt_client, drive_color, LED_color_entry):
    mqtt_client.send_message("drive_to_the_island", [drive_color.get(), LED_color_entry.get()])
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()