from micropython import const
import utime

class MPU9250():
    MPU9250_ADDRESS = const(0x68)
    DEVICE_ID       = const(0x71)

    SMPLRT_DIV     = const(0x19)
    CONFIG         = const(0x1A)
    GYRO_CONFIG    = const(0x1B)
    ACCEL_CONFIG   = const(0x1C)
    ACCEL_CONFIG_2 = const(0x1D)
    LP_ACCEL_ODR   = const(0x1E)
    WOM_THR        = const(0x1F)
    FIFO_EN        = const(0x23)
    I2C_MST_CTRL   = const(0x24)
    I2C_MST_STATUS = const(0x36)
    INT_PIN_CFG    = const(0x37)
    INT_ENABLE     = const(0x38)
    INT_STATUS     = const(0x3A)
    ACCEL_OUT      = const(0x3B)
    TEMP_OUT       = const(0x41)
    GYRO_OUT       = const(0x43)

    I2C_MST_DELAY_CTRL = const(0x67)
    SIGNAL_PATH_RESET  = const(0x68)
    MOT_DETECT_CTRL    = const(0x69)
    USER_CTRL          = const(0x6A)
    PWR_MGMT_1         = const(0x6B)
    PWR_MGMT_2         = const(0x6C)
    FIFO_R_W           = const(0x74)
    WHO_AM_I           = const(0x75)

    GFS_250  = const(0x00)
    GFS_500  = const(0x01)
    GFS_1000 = const(0x02)
    GFS_2000 = const(0x03)
    AFS_2G   = const(0x00)
    AFS_4G   = const(0x01)
    AFS_8G   = const(0x02)
    AFS_16G  = const(0x03)

    def __init__(self, i2c, address = MPU9250_ADDRESS):
        self.i2c = i2c
        self.address = address
        self.setting(self.GFS_250, self.AFS_2G)
        self.ak8963 = AK8963(self.i2c)

    def searchDevice(self):
        who_am_i = self.i2c.readfrom(self.address, self.WHO_AM_I)
        if(who_am_i == self.DEVICE_ID):
            return True
        else:
            return False

    def setting(self, gfs, afs):
        if gfs == self.GFS_250:
            self.gres = 250.0/32768.0
        elif gfs == self.GFS_500:
            self.gres = 500.0/32768.0
        elif gfs == self.GFS_1000:
            self.gres = 1000.0/32768.0
        else:  # gfs == GFS_2000
            self.gres = 2000.0/32768.0

        if afs == self.AFS_2G:
            self.ares = 2.0/32768.0
        elif afs == self.AFS_4G:
            self.ares = 4.0/32768.0
        elif afs == self.AFS_8G:
            self.ares = 8.0/32768.0
        else: # afs == AFS_16G:
            self.ares = 16.0/32768.0

        buffer = bytearray(1)
        self.i2c.writeto_mem(self.address, self.PWR_MGMT_1, b'\x00') # sleep off
        utime.sleep_ms(100)
        self.i2c.writeto_mem(self.address, self.PWR_MGMT_1, b'\x01') # auto select clock source
        utime.sleep_ms(100)
        self.i2c.writeto_mem(self.address, self.CONFIG, b'\x03') # DLPF_CFG
        self.i2c.writeto_mem(self.address, self.SMPLRT_DIV, b'\x04') # sample rate divider
        buffer[0] = gfs << 3
        self.i2c.writeto_mem(self.address, self.GYRO_CONFIG, buffer) # gyro full scale select
        buffer[0] = afs << 3
        self.i2c.writeto_mem(self.address, self.ACCEL_CONFIG, buffer) # accel full scale select
        self.i2c.writeto_mem(self.address, self.ACCEL_CONFIG_2, b'\x03') # A_DLPFCFG
        self.i2c.writeto_mem(self.address, self.INT_PIN_CFG, b'\x02') # BYPASS_EN
        utime.sleep_ms(100)

    def check_data_ready(self):
        drdy = self.i2c.readfrom(self.address, self.INT_STATUS)
        if drdy & 0x01:
            return True
        else:
            return False
            
    def read_accel(self):
        data = self.i2c.readfrom_mem(self.address, self.ACCEL_OUT, 6)
        x = self.data_convert(data[1], data[0])
        y = self.data_convert(data[3], data[2])
        z = self.data_convert(data[5], data[4])

        x = round(x*self.ares, 3)
        y = round(y*self.ares, 3)
        z = round(z*self.ares, 3)

        return {"x":x, "y":y, "z":z}

    def read_gyro(self):
        data = self.i2c.readfrom_mem(self.address, self.GYRO_OUT, 6)

        x = self.data_convert(data[1], data[0])
        y = self.data_convert(data[3], data[2])
        z = self.data_convert(data[5], data[4])

        x = round(x*self.gres, 3)
        y = round(y*self.gres, 3)
        z = round(z*self.gres, 3)

        return {"x":x, "y":y, "z":z}

    def read_magnet(self):
        return self.ak8963.read_magnet()

    def data_convert(self, data1, data2):
        value = data1 | (data2 << 8)
        if(value & (1 << 16 - 1)):
            value -= (1<<16)
        return value

class AK8963():
    AK8963_SLAVE_ADDRESS = const(0x0C)
    AK8963_ST1           = const(0x02)
    AK8963_MAGNET_OUT    = const(0x03)
    AK8963_CNTL1         = const(0x0A)
    AK8963_CNTL2         = const(0x0B)
    AK8963_ASAX          = const(0x10)
    AK8963_MODE_DOWN     = const(0x00)
    AK8963_MODE_ONE      = const(0x01)
    AK8963_MODE_C8HZ     = const(0x02)
    AK8963_MODE_C100HZ   = const(0x06)
    AK8963_BIT_14        = const(0x00)
    AK8963_BIT_16        = const(0x01)

    def __init__(self, i2c, address=0x76):
        self.i2c = i2c
        self.address = address
        self.setting(self.AK8963_MODE_C8HZ, self.AK8963_BIT_16)

    def setting(self, mode, mfs):
        if mfs == self.AK8963_BIT_14:
            self.mres = 4912.0/8190.0
        else: #  mfs == AK8963_BIT_16:
            self.mres = 4912.0/32760.0

        self.i2c.writeto_mem(self.AK8963_SLAVE_ADDRESS, self.AK8963_CNTL1, b'\x00')
        utime.sleep_ms(10)
        self.i2c.writeto_mem(self.AK8963_SLAVE_ADDRESS, self.AK8963_CNTL1, b'\x0F') # set read FuseROM mode
        utime.sleep_ms(10)
        data = self.i2c.readfrom_mem(self.AK8963_SLAVE_ADDRESS, self.AK8963_ASAX, 3) # read coef data

        self.magXcoef = (data[0] - 128) / 256.0 + 1.0
        self.magYcoef = (data[1] - 128) / 256.0 + 1.0
        self.magZcoef = (data[2] - 128) / 256.0 + 1.0

        self.i2c.writeto_mem(self.AK8963_SLAVE_ADDRESS, self.AK8963_CNTL1, b'\x00') # set power down mode
        utime.sleep_ms(10)
        buffer = bytearray(1)
        buffer[0] = (mfs << 4 | mode)
        self.i2c.writeto_mem(self.AK8963_SLAVE_ADDRESS, self.AK8963_CNTL1, buffer) # set scale&continous mode
        utime.sleep_ms(10)

    def read_magnet(self):
        x, y, z=0, 0, 0
        
        data = self.i2c.readfrom_mem(self.AK8963_SLAVE_ADDRESS, self.AK8963_MAGNET_OUT, 7)

        # check overflow
        if (data[6] & 0x08)!=0x08:
            x = self.data_convert(data[0], data[1])
            y = self.data_convert(data[2], data[3])
            z = self.data_convert(data[4], data[5])

            x = round(x * self.mres * self.magXcoef, 3)
            y = round(y * self.mres * self.magYcoef, 3)
            z = round(z * self.mres * self.magZcoef, 3)

        return {"x":x, "y":y, "z":z}

    def data_convert(self, data1, data2):
        value = data1 | (data2 << 8)
        if(value & (1 << 16 - 1)):
            value -= (1<<16)
        return value

if __name__ == "__main__":

    mpu9250 = MPU9250(None)

    accel = mpu9250.read_accel()
    gyro = mpu9250.read_gyro()
    mag = mpu9250.read_magnet()
    
    print(accel, gyro, mag)
