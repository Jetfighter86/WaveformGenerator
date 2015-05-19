__author__ = 'Phillip'

import threading
import time
import serial
LFCR = '\r\n'
class SerialDriver():
    buffer =""
    line = list()
    def __init__(self, portNum, baudrate, timeout=10,  **args):
        self.timeout = timeout
        self.serial = serial.Serial(port='COM'+ str(portNum),baudrate=baudrate,parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,timeout=0.1, **args)
    def readlines(self):
        try:
            tic = time.time()
            while time.time()-tic < self.timeout:
                for c in self.serial.readline():
                    self.line.append(c)
            return self.line
        except Exception:
            return Exception.message
    def write(self,command):
        self.serial.write(command)
    def open(self):
        self.serial.open()
    def close(self):
        try:
            print 'Close Method is called'
            self.serial.close()
        except serial.serialutil.SerialException:
            return serial.SerialException.message
        except serial.portNotOpenError:
            return serial.portNotOpenError.message
        except Exception:
            return Exception.message
            print 'exception was raised'
    def timer(self, name, delay):
        self.Delay = delay
        print 'Timer Started'
        while self.Delay > 0:
            time.sleep(1)
            self.Delay -=1
        print self.line
        try:
            print 'close from timer'
            self.close()
        except serial.portNotOpenError:
            return serial.portNotOpenError.message
    def parseSerial(self,message):
        return ''.join(message)



s = SerialDriver(10,19200,0.4)
# t1 = threading.Thread(target=s.timer, args=('',3))
s.write('0')
s.write('4')
l = s.readlines()
print "".join(l)
s.close()