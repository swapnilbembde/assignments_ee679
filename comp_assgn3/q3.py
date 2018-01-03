from scipy import signal
from scipy.io.wavfile import read, write
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import sys

# annotate the maximum
def annot_max(x,y, ax=None):
    xmax = x[np.argmax(y)]
    ymax = y.max()
    text= "x={:.3f}, y={:.3f}".format(xmax, ymax)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
    ax.annotate(text, xy=(xmax, ymax), xytext=(0.94,0.96), **kw)

wave_file = {'a': 'machali_male_8k_a.wav', 'n': 'machali_male_8k_n.wav', 'i': 'machali_male_8k_i.wav', 's': 'machali_male_16k_s.wav'}

# Reading data 
file = sys.argv[1]
[SampFre, data] = read(wave_file[file]);
data = data/32768
winTime = 30.0/1000.0 #ms
SampWin = SampFre*winTime

# Windowing the middle samples
win = data[int((len(data)-SampWin)/2):int((len(data)+SampWin)/2)]*np.hamming(SampWin)

# Calculating the real cepstrum
dft_c = np.log10(np.abs(np.fft.fft(win, 1024)))
cep = np.real(np.fft.ifft(dft_c))
#plt.plot(cep)
#plt.grid()
#x = np.linspace(0, 1023, num = 1024)
#annot_max(np.linspace(0, 1023, num = 1024),cep)

#plt.savefig('2-'+file+'-realCep.png')
#plt.show()

# Liftering the cepstrum
lift = 30
cep[lift:(cep.shape[-1]-lift)] = 0

# Take the DFT
dft_cep_lift = np.abs(np.fft.fft(cep, 1024))
freq_cep_lift = np.fft.fftfreq(dft_cep_lift.shape[-1], 1/float(SampFre))

plt.plot(freq_cep_lift[:len(freq_cep_lift)/2], 20*np.abs(dft_c[:len(dft_c)/2]), 'r')
plt.plot(freq_cep_lift[:len(freq_cep_lift)/2], 20*np.abs(dft_cep_lift[:len(dft_cep_lift)/2]), 'b')

# Define the autocorrelation 
def autocorr(x):
    op = np.correlate(x, x, mode='full')
    return op[op.size/2:]

filterOrder = 10

if sys.argv[1] == 's':
    filterOrder = 18

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
plt.plot(SampFre*w/(2*pi), 20 * np.log10(abs(h)), 'g')
plt.ylabel('DFT Amplitude')
plt.xlabel('Frequency')
plt.legend(['Original DFT', 'Cepstral Envelope', 'LPC Envelope'])
plt.grid()
plt.show()
#plt.savefig('2-'+file+'-env.png')

