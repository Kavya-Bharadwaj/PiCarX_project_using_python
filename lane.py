from picarx import Picarx
import carinstance
from time import sleep

last_state = None
current_state = None
#kvy5kor: this value is taken from modules.py. Adjust this based on the track settings
REFERENCE_DEFAULT = [80]*3

def isBotNearRightLane(fl_list):
    if(fl_list[0] < fl_list[2]):
        return True
    else:
        return False

def isBotNearLeftLane(fl_list):
    if(fl_list[2] < fl_list[0]):
        return True
    else:
        return False

def isBotInMiddleOfTheLane(fl_list):
    if(fl_list[0]>=REFERENCE_DEFAULT & fl_list[1]>=REFERENCE_DEFAULT & fl_list[2]>=REFERENCE_DEFAULT):
        return True
    else:
        return False
    


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
        my_car.backward(5)
    elif last_state == 'right':
        my_car.set_dir_servo_angle(30)
        my_car.backward(5)
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
    my_car.set_grayscale_reference(75)  
    # px.grayscale.reference = 1400  
    px_power = carinstance.DEFAULT_POWER
    offset = 20

    try:
        while True:
            gm_val_list = my_car.get_grayscale_data()
            gm_state = get_line_status(gm_val_list)
            print("gm_val_list: %s, %s"%(gm_val_list, gm_state))

            if gm_state != "STOP":
                last_state = gm_state

            if gm_state == 'FORWARD':
                print("follow_lane() : Recieved Direction FORWARD")
                my_car.set_dir_servo_angle(0)
                my_car.forward(px_power)
                break 
            elif gm_state == 'LEFT':
                print("follow_lane() : Recieved Direction LEFT")
                my_car.set_dir_servo_angle(offset)
                my_car.forward(px_power) 
            elif gm_state == 'RIGHT':
                print("follow_lane() : Recieved Direction RIGHT")
                my_car.set_dir_servo_angle(-offset)
                my_car.forward(px_power) 
            else:
                print("follow_lane() : Recieved Direction NONE, outHandle() will be called")
                outHandle(my_car)
            sleep(0.001)
    except Exception as e:
        print("Exception received : ",e)

def get_line_status(fl_list):
    
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
        print("Car is on the lane, move to last known direction. CUrrently hardcoding to Right, FIX ME!!!")
        direction = 'RIGHT'
    elif value == [1, 0, 0] or value == [1, 1, 0]: # Here, car id close to the right lane, or it is on the right lane. so move left
        print("car is close to the left lane, or it is on the left lane. so move right")
        print("grayscale values:")
        print(value)
        direction = 'LEFT'
    elif value == [0, 0, 1] or value == [0, 1, 1]:
        print("car is close to the right lane, or it is on the right lane. so move left")
        print("grayscale values:")
        print(value)
        direction = 'RIGHT'
    elif value == [0, 0, 0]:
        print("None of the sensors detect lane, so we are probably good to move forward")
        print("grayscale values:")
        print(value)
        direction = 'FORWARD'

    return direction

def get_line_status_bkp(fl_list):
    #kvy5kor: this value is taken from modules.py. Adjust this based on the track settings
    #REFERENCE_DEFAULT = [1000]*3
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
        print("Car is on the lane")
        if(fl_list[0]<fl_list[2]):
            print("Car is close to Right lane strip, hence move left")
            direction = 'LEFT'
        elif(fl_list[2]<fl_list[0]):
            print("Car is close to Left lane strip, hence move right")
            direction = 'RIGHT'
        else:
            print("Unable to detect direction, THIS SHOULD NOT HAPPEN, FIX ME!!!!!!!!!!!")
            direction = 'STOP'

    elif value == [1, 0, 0] or value == [1, 1, 0]: # Here, car id close to the right lane, or it is on the right lane. so move left
        print("car is close to the left lane, or it is on the left lane. so move right")
        print("grayscale values:")
        print(value)
        direction = 'LEFT'
    elif value == [0, 0, 1] or value == [0, 1, 1]:
        print("car is close to the right lane, or it is on the right lane. so move left")
        print("grayscale values:")
        print(value)
        direction = 'RIGHT'
    elif value == [0, 0, 0]:
        print("None of the sensors detect lane, so we are probably good to move forward")
        print("grayscale values:")
        print(value)
        direction = 'FORWARD'

    return direction