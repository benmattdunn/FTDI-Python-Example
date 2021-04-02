# FTDI-Python-Example
About:

Description is pulled from the "FTDI_ConnectionManager.py" - explains mostly how this works. 
Other the the FTDI DLL that must be installed - this example program runs straight out the box on windows 10. 

I've tried to be as detailed as possible in this description.

Files:

FTDI_DirectDLL.py: is a wrapper so python can interact with the .dll that you will install. (see below).

FTDI_ConnectionManager.py: is an interface that shows how these functions can be linked together to create
a easy communication.

TestWindow.py: calls a basic tkinker window (GUI) to display what the response was from the ardunio.

main.py - entry point. Simply running this with the interpreter present on the system (even the standard windows 10
APP one) should boot the program and start the example.

The Ctypes library and sys lib (which should be in basic python 3.0(?)+ are required.  

If you have further questions send me a message and I'd be happy to answer them. As this is one of the easiest ways
to connect with simple MCUs as FTDI chips are very present in most simple electronic devices. When I was back in
college and university I always wanted a simple - bare bones example of how this stuff is done - I hope this helps
you through those first year projects if you stumble accross this!

Not tested on other OS' other then windows 10. However with python it'll work (likely) on any version of windows, and 
I'd bet on linux as well (well common distros). 

DESCRIPTION: Basically this is a 'FTDI to serial' connection manager. Allows the user to connect (in this example)
to an arduino nano with very little hassle by directly connecting to the USB to serial (FTDI) on the device.  

I created this project as I am very familiar with FTDI connections and I noticed that the documentation for this 
is quite lacking (Very much so for python). This project was made in windows (and tested in) - but provided 
the drivers are installed, linux should be supported as well because of the FTDI_DirectDLL is designed as such.

For this connection style to work, you must install the FTDI drivers that can be found here: 
https://www.ftdichip.com/FTDrivers.htm

if you install this program an ardunio_nano with the "serial event example" this code will run straight out of the box.

(The python window will display the message and the pong back). 

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
-Ease of use. I don't care what the code is - just that one happened. This is a bare min example.
