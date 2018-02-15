import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com



def main():
    # DONE: 2. Setup an mqtt_client.  Notice that since you don't need to receive any messages you do NOT need to have
    # a MyDelegate class.  Simply construct the MqttClient with no parameter in the constructor (easy).
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3("mosquitto.csse.rose-hulman.edu", 8)


    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    main_frame2 = ttk.Frame(root, padding=5)
    main_frame2.grid()

    # The values from the Pixy range from 0 to 319 for the x and 0 to 199 for the y.
    canvas = tkinter.Canvas(main_frame2, background="lightgray", width=450, height=300)
    canvas.grid(columnspan=2)

    canvas.create_line(225,150,265,150)
    canvas.create_line(265,150,265,190)
    canvas.create_line(265,190,225,190)
    canvas.create_line(225,150,225,190)

    slider_label = ttk.Label(main_frame, text="Speed")
    slider_label.grid(row=0,column=1)
    slider = tkinter.Scale(main_frame,from_=100 ,to=600, orient=tkinter.HORIZONTAL )
    slider.grid(row=1, column = 1)


    # DONE: 3. Implement the callbacks for the drive buttons. Set both the click and shortcut key callbacks.
    #
    # To help get you started the arm up and down buttons have been implemented.
    # You need to implement the five drive buttons.  One has been writen below to help get you started but is commented
    # out. You will need to change some_callback1 to some better name, then pattern match for other button / key combos.




    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: handle_forward_button(mqtt_client, slider, slider)
    root.bind('<Up>', lambda event: handle_forward_button(mqtt_client, slider, slider))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    # left_button and '<Left>' key
    left_button['command'] = lambda: handle_left_button(mqtt_client, slider, slider)
    root.bind('<Down>'), lambda event: handle_left_button(mqtt_client, slider, slider)
    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: handle_stop_button(mqtt_client)
    root.bind('<space>'), lambda event: handle_stop_button(mqtt_client)
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    # right_button and '<Right>' key
    right_button['command'] = lambda : handle_right_button(mqtt_client, slider, slider)
    root.bind('<Right>'), lambda event: handle_right_button(mqtt_client, slider, slider)
    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    back_button['command'] = lambda: handle_back_button(mqtt_client, slider, slider)
    root.bind('<Down>'), lambda event: handle_back_button(mqtt_client, slider, slider)
    # back_button and '<Down>' key

    close_button = ttk.Button(main_frame, text="Close")
    close_button.grid(row=4, column=0)
    close_button['command'] = lambda: handle_close_button(mqtt_client)

    open_button = ttk.Button(main_frame, text="Open")
    open_button.grid(row=4, column=2)
    open_button['command'] = lambda: handle_open_button(mqtt_client)
    root.mainloop()



# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------
# Arm command callbacks
def handle_forward_button(mqtt_client, left_speed_entry, right_speed_entry):
    print("foward button")
    mqtt_client.send_message("forward", [int(left_speed_entry.get()), int(right_speed_entry.get())])


def handle_left_button(mqtt_client, left_speed_entry, right_speed_entry):
    print("left button")
    mqtt_client.send_message("left", [int(left_speed_entry.get()), int(right_speed_entry.get())])


def handle_right_button(mqtt_client, left_speed_entry, right_speed_entry):
    print("right button")
    mqtt_client.send_message("right",[int(left_speed_entry.get()), int(right_speed_entry.get())])


def handle_back_button(mqtt_client, left_speed_entry, right_speed_entry):
    print("back button")
    mqtt_client.send_message("backward", [int(left_speed_entry.get()), int(right_speed_entry.get())])


def handle_stop_button(mqtt_client):
    print("stop button")
    mqtt_client.send_message("stop")


def handle_close_button(mqtt_client):
    print("close")
    mqtt_client.send_message("arm_close")


def handle_open_button(mqtt_client):
    print("open")
    mqtt_client.send_message("arm_down")


def pressed(event, mqtt_client, left_speed_entry, right_speed_entry):
    print("Pressed")
    if event.keysym == "Up":
        mqtt_client.send_message("forward", [int(left_speed_entry.get()), int(right_speed_entry.get())])
    elif event.keysym == "Down":
        mqtt_client.send_message("backward", [int(left_speed_entry.get()), int(right_speed_entry.get())])
    elif event.keysym == "Right":
        mqtt_client.send_message("right_move", [int(left_speed_entry.get()), int(right_speed_entry.get())])
    elif event.keysym == "Left":
        mqtt_client.send_message("left_move", [int(left_speed_entry.get()), int(right_speed_entry.get())])
    elif event.keysym == 'q':
        mqtt_client.send_message("shutdown")
        mqtt_client.close()
        exit()
    elif event.keysym == 'u':
        print("arm_up")
        mqtt_client.send_message("arm_up")
    elif event.keysym == 'j':
        print("arm_down")
        mqtt_client.send_message("arm_down")
# Quit and Exit button callbacks








# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()