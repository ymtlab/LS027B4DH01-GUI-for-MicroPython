import utime
from machine import Pin, SPI, I2C
from LS027B4DH01 import LS027B4DH01
from joystick import Joystick
from ui_home import Ui_home
from ui_gyro import Ui_gyro
from ui_acceleration import Ui_acceleration
from ui_geomagnetism import Ui_geomagnetism
from mpu9250 import MPU9250

class GUI_test():
    def __init__(self):

        self.lcd = LS027B4DH01(
            spi = SPI(
                2, baudrate=2_000_000, polarity=0, phase=0, bits=8, 
                firstbit=SPI.LSB, sck=Pin(18), mosi=Pin(23), miso=Pin(19)
            ), 
            scs = Pin(32, Pin.OUT), 
            extcomin = Pin(33, Pin.OUT), 
            disp = Pin(25, Pin.OUT)
        )

        self.button = Joystick( 
            x = Pin(34),
            y = Pin(35),
            s = Pin(26, Pin.IN)
        )

        self.mpu9250 = MPU9250(
            I2C(
                scl  = Pin(21), 
                sda  = Pin(22), 
                freq = 100000
            ) 
        )

        self.mpu9250.setting(
            self.mpu9250.GFS_1000, 
            self.mpu9250.AFS_16G
        )

        self.states = {
            'home'         : Ui_home(self), 
            'acceleration' : Ui_acceleration(self), 
            'gyro'         : Ui_gyro(self), 
            'geomagnetism' : Ui_geomagnetism(self)
        }

        self.state = 'home'

    def run(self):
        obj = self.states[self.state]
        obj.control( self.button.read() )
        obj.draw()

    def change_state(self, state):
        self.state = state

def main():

    gui_test = GUI_test()
    
    utime.sleep(1)

    while True:
        gui_test.run()

if __name__ == "__main__":
    main()
