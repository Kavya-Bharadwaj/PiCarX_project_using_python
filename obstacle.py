from picarx import Picarx
import carinstance
import time

POWER = 50
SafeDistance = 40   # > 30 safe
DangerDistance = 20 # > 20 && < 30 turn around, 
                    # < 20 backward

# def avoid_obstacle(car_instance):
#     my_distance_sensor = distance_sensor.Distance_Sensor()
#     distance = my_distance_sensor.get_distance()

#     if distance < 15:  # Adjust the threshold distance as needed
#         car_instance.stop()
#         print("Obstacle detected. Stopping the car.")
#         return True  # Indicate that an obstacle was detected
#     return False


# True return value indicates that there is an obstacle ahead, hence control
# should come back to this function until the path ahead is clear
def avoid_obstacle():
    px = carinstance.my_car_instance

    
    try:
        # px = Picarx(ultrasonic_pins=['D2','D3']) # tring, echo
        distance = round(px.ultrasonic.read(), 2)
        print("distance: ",distance)
        if distance >= SafeDistance:
            px.set_dir_servo_angle(0)
            px.forward(POWER)
            return False
        elif distance >= DangerDistance:
            px.set_dir_servo_angle(40)
            px.forward(POWER)
            time.sleep(0.1)
            return True
        else:
            px.set_dir_servo_angle(-40)
            px.backward(POWER)
            time.sleep(0.5)
            return True

    finally:
        px.forward(0)