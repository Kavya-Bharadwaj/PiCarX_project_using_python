from picarx import Picarx
import time
import lane  # Import the lane module
import obstacle  # Import the obstacle module
import carinstance

# Initialize the car
my_car = carinstance.my_car_instance

# Move the car forward
my_car.forward()
lane.follow_lane(my_car)

# Main code
try:
    while True:
        while obstacle.is_obstacle_exist(my_car):
            time.sleep(0.01)

        # Obstacle is cleared, resume lane following
        lane.follow_lane(my_car)

        time.sleep(0.1)  # Adjust the delay as needed
except KeyboardInterrupt:
    my_car.stop()
