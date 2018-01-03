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
#fileKey = 'a'
fileKey = sys.argv[1]
[fSamp, data] = read(files[fileKey]);
print fSamp
data = data/32768
winTime = 30.0/1000.0 #ms
nSamp = fSamp*winTime

# Window the middle nSamp samples
win = data[int((len(data)-nSamp)/2):int((len(data)+nSamp)/2)]*np.hamming(nSamp)


if fileKey in ['a', 'b', 'c']:
    for i in range(1, len(win)):
        win[i] = win[i] - 0.95 * win[i-1]

dft2 = np.fft.fft(win, 1024)
freq2 = np.fft.fftfreq(dft2.shape[-1], 1/float(fSamp))
plt.plot(freq2[:len(freq2)/2], 20*np.log10(np.abs(dft2[:len(dft2)/2])) + 120, 'c')
#plt.savefig('figs/2a-'+str(fileKey)+'.png');

#filterOrder = int(sys.argv[2]) #4, 6, 8, 10, 12, 20

#fig2 = plt.figure()
plt.title('LPC Filters: Frequency Response for '+displays[fileKey])
plt.ylabel('Amplitude [dB]')
plt.xlabel('Frequency [rad/sample]')

for filterOrder in np.asarray([4, 6, 8, 10, 12, 20])*(fSamp/8000):

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
    G[m] = b[0]
    #print a,G

    # Pole-zero plot
    z, p, k = signal.tf2zpk(b, a)

    #fig1 = plt.figure()
    #plt.plot(np.real(z), np.imag(z), 'xb')
    #plt.plot(np.real(p), np.imag(p), 'or')
    #plt.legend(['Zeros', 'Poles'], loc=2)
    #plt.title('Pole / Zero Plot')
    #plt.ylabel('Real')
    #plt.xlabel('Imaginary')
    #plt.grid()

    #if filterOrder == 6 or filterOrder == 10:
    #    plt.savefig('2ba-'+fileKey+'-'+str(filterOrder)+'.png')

    # Frequency response of LPC filter
    #w, h = signal.freqz(b, a)

    #plt.plot(fSamp*w/(2*pi), displacements[filterOrder*8000/fSamp] + 20 * np.log10(abs(h)), colors[filterOrder*8000/fSamp])
    #plt.show()

print G
#plt.legend(['Orig', 'Order 4', 'Order 6', 'Order 8', 'Order 10', 'Order 12', 'Order 20'])
#plt.grid()
#plt.show()
#plt.savefig('2bb-'+fileKey+'-'+str(filterOrder)+'.png')