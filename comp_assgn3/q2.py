from scipy import signal
from scipy.io.wavfile import read, write
import numpy as np
import matplotlib.pyplot as plt
from math import pi

# Reading data
[SampFre, data] = read('a10.wav');
data = data/32768.0
winTime = 30.0/1000.0 #ms
SampWin = SampFre*winTime

# Windowing the middle samples
win = data[int((len(data)-SampWin)/2):int((len(data)+SampWin)/2)]*np.hamming(SampWin)

for i in range(1, len(win)):
        win[i] = win[i] - 0.95 * win[i-1]

# Calculating the real cepstrum
dft_c = np.log10(np.abs(np.fft.fft(win, 1024)))
cep = np.real(np.fft.ifft(dft_c))
#plt.plot(cep)
plt.grid()
#x = np.linspace(0, 1023, num = 1024)
#annot_max(np.linspace(0, 1023, num = 1024),cep)

#plt.savefig('2a-'+'-realCep.png')
#plt.show()

# Window the cepstrum

#cep[lift:(cep.shape[-1]-lift)] = 0

# Take the DFT
dft_cep_lift = np.abs(np.fft.fft(cep, 1024))
freq_cep_lift = np.fft.fftfreq(dft_cep_lift.shape[-1], 1/float(SampFre))
plt.plot(freq_cep_lift[:len(freq_cep_lift)/2], 20*np.abs(dft_c[:len(dft_c)/2]), 'k')

for i in range (3,0,-1):
	lift = 20 + i*10
	# Window the cepstrum
	cep[lift:(cep.shape[-1]-lift)] = 0 
	dft_cep_lift = np.abs(np.fft.fft(cep, 1024))
	freq_cep_lift = np.fft.fftfreq(dft_cep_lift.shape[-1], 1/float(SampFre))
	plt.plot(freq_cep_lift[:len(freq_cep_lift)/2], 20*np.abs(dft_cep_lift[:len(dft_cep_lift)/2]))


# Define the autocorrelation 
def autocorr(x):
    op = np.correlate(x, x, mode='full')
    return op[op.size/2:]

filterOrder = 10

# Use Levinson's algorithm to calculate a[k]
R = autocorr(win)

a = np.zeros(filterOrder+1)
ao = np.zeros(a.shape)
E = R[0]

for m in range(1, filterOrder+1):
    k = 0
    ao[1:len(a)] = a[1:len(a)]
    Eo = E
    # finding K
    for l in range(1, m):
        k = k + ao[l]*R[m-l]
    k = (R[m] - k)/Eo
    # calculation of a's
    a[m] = k
    
    for l in range(1, m):
        a[l] = ao[l] - k*ao[m-l]
    
    E = (1-k*k)*Eo

a[0] = 1.0
a[1:len(a)] = -a[1:len(a)]

b = np.zeros(a.shape)
b[0] = np.sqrt(E)

w, h = signal.freqz(b, a)
plt.plot(SampFre*w/(2*pi), 20 * np.log10(abs(h)), 'c')
plt.ylabel('DFT Amplitude')
plt.xlabel('Frequency')
plt.legend(['Orig', 'Cepstral Envelope L=50', 'Cepstral Envelope L=40', 'Cepstral Envelope L=30', 'LPC Envelope'])
plt.grid()
#plt.show()
#plt.savefig('2all-'+'-env.png')