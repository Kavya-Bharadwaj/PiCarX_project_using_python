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
            gm_state = my_car.get_line_status(gm_val_list)
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
