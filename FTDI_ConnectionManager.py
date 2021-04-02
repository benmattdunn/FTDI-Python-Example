0#handles connections for FTDI devices; just simple wrapper functions for ease of use, and wrapped into a class allowing
"""
DESCRIPTION: Basically this is a 'FTDI to serial' connection manager. Allows the user to connect (in this example)
to an arduino nano with very little hassle by directly connecting to the USB to serial (FTDI) on the device.  

I created this project as I am very familiar with FTDI connections and I noticed that the documentation for this 
is quite lacking (Very much so for python). This project was made in windows (and tested in) - but provided 
the drivers are installed, linux should be supported as well because of the FTDI_DirectDLL is designed as such.

For this connection style to work, you must install the FTDI drivers that can be found here: 
https://www.ftdichip.com/FTDrivers.htm

if you install this program an ardunio_nano with the serial event example this code will run straight out of the box.

It should be noted that this is a EXAMPLE program and is limited by the fact that it only scans for a single device.
Devices with shared names (multiple nanos) are not controlled for. The solution for this is to list all the devices 
then select each that applies OR rename the device using the FTDI config (not recommended). 

if you have different FTDI devices - you should be able to create multiple connection managers to connect to them. 

(Standard MIT liscence)  
Copyright 2020: Ben Dunn 

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the 
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED 
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.

Common questions:
why do you use |= for error checking even though error codes for FTDI devices are not in byte format? 
-Ease of use. I don't care what the code is - just that one happened. 
"""


import FTDI_DirectDLL as FTDI
import ctypes
import time
#from ctypes.wintypes import *

#mini manager class I put here rather then in the FTDI_DirectDLL to keep the data 'isolated'.
#Basically this is what controllers the connection and when you set it (see below) you need to match the devices
#settings (this is in the documentation of each device).
class _FTDI_CONNECTION_SETTINGS(ctypes.Structure):
    pass
_FTDI_CONNECTION_SETTINGS._fields_ = [
    ('Baud', ctypes.c_uint32),
    ('FT_BITS', ctypes.c_ubyte),
    ('FT_STOP_BITS', ctypes.c_ubyte),
    ('FT_PARITY', ctypes.c_ubyte),
    ('FLOW_CONTROL', ctypes.c_ubyte),
    ('FT_XON', ctypes.c_ubyte),
    ('FT_XOFF', ctypes.c_ubyte),
]

    #ardunio standard. For most purposes you really only need to change the baud rate.
    #baudRate = 9600, FT_Bits = 8, FT_STOP_BITS = 0, FT_PARTIY = 0, FLOW_CONTROL = 0, FT_XON = 0, FT_XOFF = 0

class FTDI_ConnectionManger():
    #true inherited items from FTDI
    deviceInfoTemp = FTDI._ft_device_list_info_node()           #see FTDI_DirectDLL
    deviceIndex = -1                                            #same default value used for no device;
    deviceHandle = ctypes.c_void_p()                            #windows handle (or whatever) pointer
    FTDI_status = 0                                             #current device status code
    connectionSettings = _FTDI_CONNECTION_SETTINGS()
    bytesWritten = ctypes.c_uint32()
    p_bytesWritten = ctypes.pointer(bytesWritten)
    deviceName = "" #nada the constructor sets this.


    #standard constructor takes a device description and connects to it.
    def __init__ (self, deviceName = "ARDUINO NANO"):
        self.deviceName = deviceName

    #two standard getters and setters
    def setDeviceName(self, deviceName = "ARDUINO NANO"):
        self.deviceName = deviceName

    def getDeviceName(self):
        return self.deviceName

    def connect(self):
        self.deviceIndex = self.findDeviceByDescription(self.deviceName)
        # reconnect after cycling through devices with a real match
        if self.deviceIndex != -1:
            print(self.deviceIndex)
            self.connectToDeviceByIndex(self.deviceIndex)
        else:
            print("Device was not found - try changing description")


    #prints all devices so the user can see the names. Included to allow people to change the code with ease.
    def printAllFTDIDevices(self):
        print("FTDI_DEVICE_LIST is as follows:")
        handle = ctypes.c_void_p() #pointer to what will become the opened window port.
        numDev = ctypes.c_ulong()
        p_numDev = ctypes.pointer(numDev)
        deviceInfoTemp = FTDI._ft_device_list_info_node() #create a data structure to hold the list of devices in.
        p_deviceInfo = ctypes.pointer(deviceInfoTemp)
        currentDev = ctypes.c_ulong()
        p_currentDev = ctypes.pointer(currentDev)

        FTDI.FT_CreateDeviceInfoList(p_numDev)
        if(numDev.value >=1 ):
            for k in range(numDev.value):
                FTDI.FT_Open(k, handle)
                currentDev.value = k
                FTDI.FT_GetDeviceInfoList(p_deviceInfo, p_currentDev)
                print(deviceInfoTemp.Description)
                FTDI.FT_Close(handle)
        else:
            print("No FTDI devices  Found.")





    # finds the current FTDI device index of the described device, this is ideal as it allows multiple connections with ease

    #while this DOES find the index - the connectToDeviceByIndex() function actually keeps the port open.
    def findDeviceByDescription(self, deviceName="ARDUINO NANO"):
        print("checking devices")
        devicesFoundIndex = -1 #note that this is usually an error where devices are not defined properally;
        handle = ctypes.c_void_p()
        self.FTDI_status = 0 #status flags are in documentation - this can help with debugging.
        numDev = ctypes.c_ulong()
        p_numDev = ctypes.pointer(numDev)
        currentDev = ctypes.c_ulong()
        p_currentDev = ctypes.pointer(currentDev)
        #item and pointer // because of the CTYPE it's easier just to pass this way and pull the entire structure
        deviceInfoTemp = FTDI._ft_device_list_info_node()
        p_deviceInfo = ctypes.pointer(deviceInfoTemp)
        #note the syntax in below (unlike most pl - python allows inline creation - this is pure black magic.).
        #pull number of devices
        status = FTDI.FT_CreateDeviceInfoList(p_numDev)
        print(numDev.value)
        #convert deviceName into charArray for check //last step basically
        b_deviceName = deviceName.encode('utf-8')
        #print (b_deviceName)
        for k in range(numDev.value):
            self.FTDI_status |= FTDI.FT_Open(k, handle)
            #self.FTDI_status |= FTDI.FT_ResetDevice(handle) #this can be pretty useful if you did not close the device in a session.
            currentDev.value = k
            if self.FTDI_status == 0:
                FTDI.FT_GetDeviceInfoList(p_deviceInfo, p_currentDev)
                if deviceInfoTemp.Description == b_deviceName:
                    print("device found on index ", k)
                    devicesFoundIndex =k #store found index
                    break
            else:
                self.dumpFTDICode(self.FTDI_status)
            self.FTDI_status |= FTDI.FT_Close(handle)

        self.FTDI_status |= FTDI.FT_Close(handle) #close the handle as this can be used to find more then one device by starting off outside the found index range (same name) or
        return devicesFoundIndex

        #FTDI.FT_Close(handle)

    #call second - once the index has been found use that to connect to the device;
    def connectToDeviceByIndex(self, index):
        print("Connecting on index: ", index)
    #standard glitch with FTDI, occassionally in applications the open can get glitched after the detection due to time.
        for k in range(10):
            self.FTDI_status = 0  # reset FTDI codes incase of bleed over (rare)
            #self.FTDI_status |= FTDI.FT_set
            self.FTDI_status |= FTDI.FT_Open(index, self.deviceHandle)
            #setup code goes here.
            if self.FTDI_status == 0:
               break
            else: #sleep for a second and try again
                FTDI.FT_Close(self.deviceHandle)
                time.sleep(1)
                pass
                print("reconnecting...")

        if self.FTDI_status != 0:
            self.dumpFTDICode(self.FTDI_status)
        else:
            print("connection established")

    #sets underlying device properties for the FTDI chipset, this stores the value before programming the chip set.
    #pretty standard ardunio defaults chosen. Call this method first.
    def setDeviceConnectionSettings(self,  baudRate = 9600, FT_Bits = 8, FT_STOP_BITS = 0, FT_PARTIY = 0, FLOW_CONTROL = 0, FT_XON = 0, FT_XOFF = 0):
        print("Setting connection properties:")
        self.connectionSettings.Baud              = baudRate
        self.connectionSettings.FT_BITS           = FT_Bits
        self.connectionSettings.FT_STOP_BITS      = FT_STOP_BITS
        self.connectionSettings.FT_PARITY         = FT_PARTIY
        self.connectionSettings.FLOW_CONTROL      = FLOW_CONTROL
        self.connectionSettings.FT_ON             = FT_XON
        self.connectionSettings.FT_OFF            = FT_XOFF
        #dump to make sure values are set. (Not really worried about FT_CON/OFF status)
        print("Baud: ",             self.connectionSettings.Baud )
        print("FT_BITS: ",          self.connectionSettings.FT_BITS )
        print("FT_STOP_BITS: ",     self.connectionSettings.FT_STOP_BITS)
        print("FT_Parity: ",        self.connectionSettings.FT_PARITY)
        print("FLOW_CONTROL",       self.connectionSettings.FLOW_CONTROL)
        print("XON",                self.connectionSettings.FT_XON)
        print("XOFF",               self.connectionSettings.FT_XOFF)


    def applyDeviceConnectionSettings(self): #quicly applies the above settings... (you can use a direct access to FTDI.(method) for other settings.
        self.FTDI_status = 0
        print("Applying device Connection Settings...")
        self.FTDI_status |= FTDI.FT_SetBaudRate(self.deviceHandle, self.connectionSettings.Baud)
        self.FTDI_status |= FTDI.FT_SetDataCharacteristics(self.deviceHandle, self.connectionSettings.FT_BITS, self.connectionSettings.FT_STOP_BITS, self.connectionSettings.FT_PARITY)
        self.FTDI_status |= FTDI.FT_SetFlowControl(self.deviceHandle, self.connectionSettings.FLOW_CONTROL,self.connectionSettings.FT_ON,self.connectionSettings.FT_OFF)

    def disconnect(self):
        #self.purgeBuffers() #purge any remaining data then close.
        FTDI.FT_Close(self.deviceHandle)

    #sends any string data
    def writeTestString(self, buffer = 'test \n'):
        b_buffer = buffer.encode('utf-8') #encoude the data to real data so the program can read it. (switch from python strings basically).
        self.FTDI_status |= FTDI.FT_Write(self.deviceHandle, b_buffer, len(buffer), self.p_bytesWritten)

    def readTestString(self):
        bytesWaiting = ctypes.c_uint32()
        p_bytesWaiting = ctypes.pointer(bytesWaiting)
        bytesReturned = ctypes.c_uint32()

        self.FTDI_status |= FTDI.FT_GetQueueStatus(self.deviceHandle, p_bytesWaiting)
        buffer = ctypes.create_string_buffer(bytesWaiting.value) #initalize buffer to read data.
        self.FTDI_status |= FTDI.FT_Read(self.deviceHandle, buffer, bytesWaiting, bytesReturned)
        return repr(buffer.raw) #return item as basic string



    def purgeBuffers(self, FT_PURGE_MODE = 3):
        modeFTP = ctypes.c_char()
        modeFTP.value = FT_PURGE_MODE
        p_modeFTP = ctypes.pointer(modeFTP)
        FTDI.FT_Purge(self.deviceHandle, p_modeFTP)

    def dumpFTDICode (self, code):
        print("Device Error: FTDI chip has thrown an error code: ", code )