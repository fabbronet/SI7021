# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# SI7021

import smbus2 as smbus
import time


class Si7021():

    _TWI = 0
    _THRH_ADDR = 0x40

    _CMD_RH_HOLD = 0xE5
    _CMD_RH_NOHOLD = 0xF5

    _CMD_TEMP_HOLD = 0xE3
    _CMD_TEMP_NOHOLD = 0xF3



    def __init__(self, twi=_TWI, addr= _THRH_ADDR):
        self._addr = addr


    def getRH(self):
        self._bus = smbus.SMBus(self._TWI)
        rh = self._bus.read_i2c_block_data(self._THRH_ADDR, self._CMD_RH_HOLD, 2)
        time.sleep(0.1)
        self._bus.close()
        # Convert the data
        humidity = ((((rh[0] *256) + rh[1]) * 125) / 65536.0) - 6 
        return humidity


    def getTemp(self,fahrenheit=False):
        self._bus = smbus.SMBus(self._TWI)
        temp = self._bus.read_i2c_block_data(self._THRH_ADDR, self._CMD_TEMP_HOLD,  2)
        time.sleep(0.1)
        # Read data back, 2 bytes, Temperature MSB first
        self._bus.close()
        # Convert the data
        cTemp = (((temp[0]*256 + temp[1]) * 175.72) / 65536.0) - 46.85 
        if fahrenheit:
            fTemp = cTemp * 1.8 + 32
            return fTemp
        else:
            return cTemp


    def getFW(self):
        self._bus = smbus.SMBus(self._TWI)
        self._bus.write_i2c_block_data(self._THRH_ADDR, 0x84, [0xB8])
        time.sleep(0.1)
        fw = self._bus.read_byte(0x40)
        self._bus.close()
        return str(hex(fw))

    def getUr1(self):
        self._bus = smbus.SMBus(self._TWI)
        self._bus.write_byte(self._THRH_ADDR, 0xE7)
        time.sleep(0.1)
        reg = self._bus.read_byte(0x40)
        self._bus.close()
        return str(bin(reg))

    def getHeatReg(self):
        self._bus = smbus.SMBus(self._TWI)
        self._bus.write_byte(self._THRH_ADDR, 0x11)
        time.sleep(0.1)
        reg = self._bus.read_byte(0x40)
        self._bus.close()
        return str(bin(reg))


    def getData(self):
        self._bus = smbus.SMBus(self._TWI)
        self._bus.write_byte_data(self._THRH_ADDR,0,0xE7)
        register = self._bus.read_byte_data(self._THRH_ADDR,0xE7)
        print('register:'+str(bin(register)))

        self._bus.write_byte_data(self._THRH_ADDR, 0, self._CMD_RH_NOHOLD)
        for i in [0xE3,0xE5]:
            rh = self._bus.read_i2c_block_data(self._THRH_ADDR, i, 2)
            for k in rh:
                print(str(hex(i)) + ':' + str(k))
        print('-----')
        self._bus.write_byte_data(self._THRH_ADDR, 0, self._CMD_TEMP_NOHOLD)
        time.sleep(0.1)
        self._bus.read_byte_data(0x40,0)
        for i in [0xE3,0xE5]:

            temp = self._bus.read_i2c_block_data(self._THRH_ADDR, i, 2)
            for k in temp:
                print(str(hex(i)) + ':' + str(k))
        print('*********')
        self._bus.close()
        return

def main():
    thrh = Si7021()
    while True:
        humidity = thrh.getRH()
        cTemp = thrh.getTemp()
        fw = thrh.getFW()

        # Output data to screen
        print("Fw: " + fw)
        #print("Heater reg: " + str(heater_reg))
        print("RH %%RH: %.2f%%" % humidity)
        print("Temp Celsius: %.2f°C" % cTemp)
        #print("Temp Fahrenheit: %.2f°F" % fTemp)

        time.sleep(5)

if __name__ == '__main__':
    main()



