import sys
sys.path.append(r'/home/pi/picar-x/lib')
from utils import reset_mcu
reset_mcu()

from picarx import Picarx
from pwm import PWM
from servo import Servo


if __name__ == '__main__':
    P_11 = Servo(PWM('P11'))         #初始化P11
    P_11.angle(0)       #设置P11的角度为0

