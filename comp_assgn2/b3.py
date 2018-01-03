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
fileKey = sys.argv[1]
[fSamp, data] = read(files[fileKey]);
data = data/32768
winTime = 30.0/1000.0 #ms
nSamp = fSamp*winTime

# Window the middle nSamp samples
win = data[int((len(data)-nSamp)/2):int((len(data)+nSamp)/2)]*np.hamming(nSamp)

# Plot the spectrum of this windowed signal
#dft1 = np.fft.fft(win, 1024)
#freq1 = np.fft.fftfreq(dft1.shape[-1], 1/float(fSamp))
#plt.plot(freq1[:len(freq1)/2], 20*np.log10(np.abs(dft1[:len(dft1)/2])), 'b')
#plt.ylabel('DFT Amplitude', color='b')
#plt.xlabel('Frequency')

if fileKey in ['a', 'b', 'c']:
    for i in range(1, len(win)):
        win[i] = win[i] - 15.0/16.0 * win[i-1]

#dft2 = np.fft.fft(win, 1024)
#freq2 = np.fft.fftfreq(dft2.shape[-1], 1/float(fSamp))
#plt.plot(freq2[:len(freq2)/2], 20*np.log10(np.abs(dft2[:len(dft2)/2])), 'g')
#plt.savefig('figs/2a-'+str(fileKey)+'.png');

filterOrder = 10 #4, 6, 8, 10, 12, 20

#fig2 = plt.figure()
#plt.title('LPC Filters: Frequency Response for ')
#plt.ylabel('Amplitude [dB]')
#plt.xlabel('Frequency [rad/sample]')

# Use Levinson's algorithm to calculate a[k]
R = autocorr(win)

a = np.zeros(filterOrder+1)
ao = np.zeros(a.shape)
E = R[0]

for m in range(1, filterOrder+1):
    k = 0
    ao[1:len(a)] = a[1:len(a)]
    Eo = E

    # Calculate k
    for l in range(1, m):
        k = k + ao[l]*R[m-l]
    k = (R[m] - k)/Eo

    # Calculate a
    a[m] = k

    for l in range(1, m):
        a[l] = ao[l] - k*ao[m-l]

    E = (1-k*k)*Eo

a[0] = 1.0
a[1:len(a)] = -a[1:len(a)]
b = np.zeros(a.shape)
b[0] = np.sqrt(E)
G = b[0]

print a
print b
#sys.exit()

winFilt = signal.lfilter(a, b, win)
#plt.plot(winFilt)
#plt.show()
#dft = np.fft.fft(winFilt, 1024)
#freq = np.fft.fftfreq(dft.shape[-1], 1/float(fSamp))
#plt.plot(freq[:len(freq)/2], 20*np.log10(np.abs(dft[:len(dft)/2])), 'b')
#plt.ylabel('DFT Amplitude', color='b')
#plt.xlabel('Frequency')

#plt.ylabel('Amplitude', color='b')
#plt.xlabel('Sample')
plt.plot(autocorr(winFilt))
plt.grid()
plt.savefig('2c-d-autoc.png')
#plt.show()

# Frequency response of LPC filter
#w, h = signal.freqz(b, a)
#
#plt.plot(fSamp*w/(2*pi), displacements[filterOrder*8000/fSamp] + 20 * np.log10(abs(h)), colors[filterOrder*8000/fSamp])
#
#plt.legend(['Orig', 'Order 4', 'Order 6', 'Order 8', 'Order 10', 'Order 12', 'Order 20'])
#plt.grid()
#plt.show()
#plt.savefig('figs/2bb-'+fileKey+'-'+str(filterOrder)+'.png')