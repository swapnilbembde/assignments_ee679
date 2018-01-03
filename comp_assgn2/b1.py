from scipy import signal
import numpy as np
from math import pi
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
import sys

# Define the autocorrelation function
def autocorr(x):
    result = np.correlate(x, x, mode='full')
    return result[result.size/2:]

files = {'a': 'machali_male_8k_a.wav', 'b': 'machali_male_8k_n.wav', 'c': 'machali_male_8k_i.wav', 'd': 'machali_male_16k_s.wav'}
displays = {'a': '/a/', 'b': '/n/', 'c': '/I/', 'd': '/s/'}
colors = {12: 'r', 4: 'g', 6: 'b', 8: 'y', 10: 'm', 20: 'k'}
displacements = {12: 80, 4: 0, 6: 20, 8: 40, 10: 60, 20: 100}

# Read data and set parameters
fileKey = 'c'
#fileKey = sys.argv[1]
[fSamp, data] = read(files[fileKey])
data = data/32768
winTime = 30.0/1000.0 #ms
nSamp = fSamp*winTime

# Window the middle nSamp samples
print (len(data)-nSamp)/2 , (len(data)+nSamp)/2, len(data), nSamp
win = data[int((len(data)-nSamp)/2):int((len(data)+nSamp)/2)]*np.hamming(nSamp)

# Plot the spectrum of this windowed signal
dft1 = np.fft.fft(win, 1024)
freq1 = np.fft.fftfreq(dft1.shape[-1], 1/float(fSamp))
plt.plot(freq1[:len(freq1)/2], 20*np.log10(np.abs(dft1[:len(dft1)/2])), 'c')
plt.ylabel('DFT Amplitude', color='b')
plt.xlabel('Frequency')

if fileKey in ['a', 'b', 'c']:
    for i in range(1, len(win)):
        win[i] = win[i] - 0.95 * win[i-1]

dft2 = np.fft.fft(win, 1024)
freq2 = np.fft.fftfreq(dft2.shape[-1], 1/float(fSamp))
plt.plot(freq2[:len(freq2)/2], 20*np.log10(np.abs(dft2[:len(dft2)/2])), 'g')
#plt.savefig('2a-'+str(fileKey)+'.png');

#filterOrder = int(sys.argv[2]) #4, 6, 8, 10, 12, 20

plt.show()

