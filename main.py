"""
DESCRIPTION: Main entry point.

this Section of code accomplishes three things.
First it creates a thread for the communication.
Second it lets TK call it's thread (main)
after the thread has been completed the program advances and closes the listener.

However if you DO NOT want the TK window. Delete the code for it.
If you do not want the thread code - you can place it in main.

Most of the documentation is in the FTDI_connectionManager.py or the read me that describes exactly how this is done.


known issues:

FTDI write/read functions are asynchronous as would be expected of USB / Serial communication (UART) with the arduino.
if the return message comes back "split up - or garbled" not enough time was given in
regards to time.sleep() extending this should fix that Tx Rx Issue.

the ardunio sends back at the end of the message "\n\r\n" : why is this?
the serial event from ardunio looks for a new line character to pong back the message(and stores it).
Because the println function from the arduino uses return \r and new line itself (\n) you end up with this message tail.

*changing the ardunio code to print will remove the last \n at very least.

why is python displaying b'(message)'
the response is in byte format. Convert it to a string to remove this.

My device is just displaying b''
most likely something has gone wrong with the connection. Check the documentation of the device. Usually this
is caused by a 'bad' FTDI port. Try closing the program / and use the usual IT crowed goto of 'unplugging it
and plugging it back in'.

The device is still giving me errors!
Try praying to god -> satan and sacraficing a small child. Usually works for me. (Jokes - send me a message via github).

"""



#project includes for functionality.
import FTDI_ConnectionManager as CM
import TestWindow
import sharedDataFile
import threading
import time
import tkinter as tk


#import FTDI_DirectDLL as DirectCallManager

programRunning = True



def comThread():
    while programRunning:
        #note read and write methods can hang up for a second or so if the device is not connected.
        FTDI_ardunio.writeTestString("Hello! from my device~! \n") #sends a standard test string.
        time.sleep(0.08)
        temp = FTDI_ardunio.readTestString()
        #print(temp) #renable this code if you want to see the data in the console.
        if temp == b'': #if the device is not connected - do not update the default text.
            sharedDataFile.sharedDataWindowListener = "connection error"
        else:
            sharedDataFile.sharedDataWindowListener = temp

        try:
            TWindow.repaint() #Java type update for graphics.
        except:
            print("window was trying repaint when closed: an exception occured yet was caught.")
    FTDI_ardunio.disconnect()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #call connection manager
    FTDI_ardunio = CM.FTDI_ConnectionManger("ARDUINO NANO")
    FTDI_ardunio.printAllFTDIDevices()              #use this function to "explore" your connected FTDI devices. By calling it you can figure up what to set the name of the connection too.
    FTDI_ardunio.connect()                          #while this might seem funny - you actually have to connect to an FTDI chip before you can set the connection parameters
    FTDI_ardunio.setDeviceConnectionSettings()      #set the internal managers settings to these values.
    FTDI_ardunio.applyDeviceConnectionSettings()    #apply the settings (which finalizes the mode of communication) and means that the port is now properally set up and can be written too / read from.
    #connect to the device

    #initalize main window via class handler
    mainWindowEntry = tk.Tk();
    mainWindowEntry.geometry('400x200')
    mainWindowEntry.title("EXAMPLE FOR ARDUNIO DATA")
    mainWindowEntry.resizable(width=False, height=False)

    #call packer and setup methods
    TWindow = TestWindow.GUI(mainWindowEntry)
    TWindow.pack(fill="both", expand=True)
    #create the listening thread.
    listeningLoop = threading.Thread(target=comThread)
    listeningLoop.start()
    tk.mainloop() #TKs main thread is used as the blocking code to keep the mointering thread open.
    programRunning = False


