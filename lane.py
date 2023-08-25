from picarx import Picarx
import carinstance
from time import sleep

# def follow_lane_old(car_instance):
#     my_grayscale_sensor = grayscale_sensor.Grayscale_Sensor()
#     values = my_grayscale_sensor.read()

#     if values[0] > 200 and values[4] > 200:
#         car_instance.forward()
#     elif values[0] < 200:
#         car_instance.turn_left()
#     elif values[4] < 200:
#         car_instance.turn_right()

def outHandle(my_car):
    global last_state, current_state
    if last_state == 'left':
        my_car.set_dir_servo_angle(-30)
        my_car.backward(10)
    elif last_state == 'right':
        my_car.set_dir_servo_angle(30)
        my_car.backward(10)
    while True:
        gm_val_list = my_car.get_grayscale_data()
        gm_state = my_car.get_line_status(gm_val_list)
        print("outHandle gm_val_list: %s, %s"%(gm_val_list, gm_state))
        currentSta = gm_state
        if currentSta != last_state:
            break
    sleep(0.001)

def follow_lane():
    my_car = carinstance.my_car_instance
    # px = Picarx(grayscale_pins=['A0', 'A1', 'A2']) 
    my_car.set_grayscale_reference(1400)  
    # px.grayscale.reference = 1400  
    last_state = None
    current_state = None
    px_power = 10
    offset = 20

    try:
        while True:
            gm_val_list = my_car.get_grayscale_data()
            gm_state = get_line_status(gm_val_list)
            print("gm_val_list: %s, %s"%(gm_val_list, gm_state))

            if gm_state != "stop":
                last_state = gm_state

            if gm_state == 'forward':
                my_car.set_dir_servo_angle(0)
                my_car.forward(px_power)
                break 
            elif gm_state == 'left':
                my_car.set_dir_servo_angle(offset)
                my_car.forward(px_power) 
            elif gm_state == 'right':
                my_car.set_dir_servo_angle(-offset)
                my_car.forward(px_power) 
            else:
                outHandle(my_car)
    finally:
        my_car.stop()

def get_line_status(self,fl_list):
    #kvy5kor: this value is taken from modules.py. Adjust this based on the track settings
    #REFERENCE_DEFAULT = [1000]*3
    REFERENCE_DEFAULT = 500
    reference = REFERENCE_DEFAULT
    if (fl_list[0]) <= reference[0]:
        Left = 1
    else:
        Left = 0
    if (fl_list[1]) <= reference[1]:
        Mid = 1
    else:
        Mid = 0
    if (fl_list[2]) <= reference[2]:
        Right = 1
    else:
        Right = 0
    value = [Left, Mid, Right]

    if value == [0, 1, 0] or value == [1, 1, 1]: #TODO : Here, car is on the line. Detect if it's left lane or right lane and decide the direction to move
        direction = 'STOP'
    elif value == [1, 0, 0] or value == [1, 1, 0]: # Here, car id close to the right lane, or it is on the right lane. so move left
        print("car is close to the right lane, or it is on the right lane. so move left")
        print("grayscale values:")
        print(value)
        direction = 'LEFT'
    elif value == [0, 0, 1] or value == [0, 1, 1]:
        print("car is close to the left lane, or it is on the left lane. so move right")
        print("grayscale values:")
        print(value)
        direction = 'RIGHT'
    elif value == [0, 0, 0]:
        print("None of the sensors detect lane, so we are probably good to move forward")
        print("grayscale values:")
        print(value)
        direction = 'FORWARD'

    return direction

