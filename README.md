# FTDI-Python-Example
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