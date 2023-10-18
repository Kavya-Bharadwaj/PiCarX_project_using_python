# Test file to check working of PiCamera using the cv2 interfaces
import cv2

def test_photo():
    path = '/home/pi/picar-x/tests/tmp/'
    name = 'test_image.png'
    cam_port = 0
    cam = cv2.VideoCapture(cam_port) 
    result, image = cam.read() 
    if result:
        print("Image detected. Saving !!")
        cv2.imwrite(f'{path}{name}', image) # saving image in local storage 
        cv2.waitKey(0) 
        cv2.destroyAllWindows()
    else: 
        print("No image detected. Please! try again") 
    

def main():
    test_photo()

if __name__ == '__main__':
    main()