import cv2
import numpy as np
def create_mask(file):
    path = '/home/pi/picar-x/tests/tmp/'
    name = 'track_mask2.png'
    frame = cv2.imread(file)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_black = np.array([0,0,0])
    upper_black = np.array([255, 255, 50])
    mask = cv2.inRange(hsv, lower_black, upper_black)
    print("Image detected\n")
    cv2.imwrite(f'{path}{name}', mask) # saving image in local storage
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    create_mask('/home/pi/picar-x/tests/test_photos/track_2.jpg')
