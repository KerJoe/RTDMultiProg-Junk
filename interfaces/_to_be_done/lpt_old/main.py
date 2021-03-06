from ..InterfaceBase import InterfaceBase
from ctypes import *
import os
import sys

class I2C(InterfaceBase):
    i2ci = None

    AvailableSystems = [ "Windows" ]
    AvailableArchitectures = [ "32bit" ]

    def __init__(self):
        inpout = cdll.LoadLibrary(os.path.dirname(__file__) + "\\inpout32.dll")
        retval = inpout.IsInpOutDriverOpen()
        if (retval == 0):
            raise SystemError("Failed to install/find INPOUT driver. Try running: \"" + os.path.dirname(__file__) + "\\InstallDriver.exe\"")
        self.i2ci = cdll.LoadLibrary(os.path.dirname(__file__) + "\\i2cinterface.dll")
        pass

    def list_i2c(self):
        return { 0x3BC: "LPT1", 0x378: "LPT2", 0x278: "LPT3" }

    def init_i2c(self, device):
        retval = self.i2ci.I2CInit(device, 0)
        if (retval == 0):
            raise ConnectionError("Failed to initialize I2C")

    def write_i2c(self, address, data):
        if (type(data) == int):
            data = [ data ]
        dat  = (c_ubyte * len(data))(*data)
        retval = self.i2ci.I2CWrite(c_ubyte(address << 1), dat, c_uint32(len(data)))
        pass

    def read_i2c(self, address, count):
        dat  = (c_ubyte * count)(*([0] * count)) #
        retval = self.i2ci.I2CRead(c_ubyte((address << 1) | 1), dat, c_uint32(count))
        data = [i for i in dat]
        return data
        pass