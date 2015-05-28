__author__ = 'Phillip'

import numpy as np,matplotlib.pyplot as plt
from pylab import figure
import math,scipy

from zigbee.WaveformGenerator import WaveformGenerator2400MHZ as wave
from scipy.fftpack import fft
import matplotlib.pyplot as plt
plt.figure(1)
def findingXValue(desiredValue,list):
    for x in list:
        if x > desiredValue:
            return list.index(x)
def graph(x_domain, y_domain):
    plt.plot(x_domain,y_domain)
    plt.grid()
    plt.show()
# shifting half pulse sine
def pulseSine():
    a = wave('0xB')
    A =  a.DATA_Q
    A0 = ([0]*10) + (A[:51] + ([0]*10))
    A1 = ([0]*20) + (A[:51])
    A2 = (A[:51]) + ([0]*20)
    FA0 = fft(A0)[:6]
    FA1 = abs(fft(A1))
    FA2 = fft(A2)
    # graph(np.linspace(0,71,71),FA1)
    # graph(np.linspace(0,71,71),A2)
def test1():
    FFTList = list()
    N = 1000
    T = 1.0 / 800
    x = np.linspace(0.0, N*T, N )
    xlist = list()
    for i in x:
        xlist.append(i)
    xlist= ([0]*4) + x
    freq = 1
    y = np.sin(2.0*np.pi*x*freq)
    yf = fft(y)
    xf = np.linspace(0,1/(2*T), N/2)
    for x in yf:
        FFTList.append(abs(x))
    print findingXValue(100,FFTList)
    print FFTList[61]
    # print xf
    # graph(np.linspace(0,T, N), y )
    # graph(xf[:N/2],FFTList[:N/2])
def arrayToList(lst):
    A = list()
    for x in lst:
        A.append(x)
    return A
def scipyTest():
    t = np.arange(256)
    sp = np.fft.fft(np.sin(t))
    freq = np.fft.fftfreq(t.shape[-1])
    plt.plot(freq, sp.real, freq, sp.imag)
    # plt.show()
    print t.shape(-1)


scipyTest()