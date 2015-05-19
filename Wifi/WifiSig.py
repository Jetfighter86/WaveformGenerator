__author__ = 'Phillip'

import numpy as np,matplotlib.pyplot as plt
from pylab import figure
import math

from scipy.fftpack import fft
# Number of samplepoints
N = 1000
# sample spacing
T = 1.0 / N
x = np.linspace(0.0, N*T, N )
print x
freq = 100
freq2 = 104
y = np.sin((2.0*np.pi*x*freq)) + np.sin((2.0*np.pi*x*freq2)) + np.sin((2.0*np.pi*x*(freq-4)))
y1 = np.sin(2.0*np.pi*x*freq)

f = fft(y)
f1 = fft(y1)
xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
import matplotlib.pyplot as plt
plt.figure(1)
plt.subplot(2,1,1)
plt.plot(xf, 2.0/N * np.abs(f[0:N/2]))
plt.subplot(2,1,2)
plt.plot(xf, 2.0/N * np.abs(f1[0:N/2]))
# plt.grid()
plt.show()