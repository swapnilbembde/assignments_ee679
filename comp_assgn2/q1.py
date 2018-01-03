from scipy import signal
import numpy as np
from math import pi
import matplotlib.pyplot as plt
from scipy.io.wavfile import read

# Define the autocorrelation function
def autocorr(x):
    op = np.correlate(x, x, mode='full')
    return op[op.size/2:]

# Read data and set parameters
harmFreq = 300
[fSamp, data] = read('a-'+str(harmFreq)+'.wav');
winTime = 30.0/1000.0 #ms
nSamp = fSamp*winTime
#filterOrder = 8 #4, 6, 8, 10

# Window the first nSamp samples
win = data[:nSamp]*np.hamming(nSamp)

fig1 = plt.figure()
plt.title('Frequency Response for /a/ at '+str(harmFreq)+' Hz')
plt.ylabel('Amplitude [dB]')
plt.xlabel('Frequency [rad/sample]')

colors = {2: 'r', 4: 'g', 6: 'b', 8: 'y', 10: 'm'}

for filterOrder in [2, 4, 6, 8, 10]:
    # Use Levinson's algorithm to calculate a[k]
    r = autocorr(win)
    a = np.zeros(filterOrder+1)
    ao = np.zeros(a.shape)
    E = r[0]

    for i in range(1, filterOrder+1):
        k = 0
        Eo = E
        ao[1:len(a)] = a[1:len(a)]      
        # finding K
        for l in range(1, i):
            k = k + ao[l]*r[i-l]
        k = (r[i] - k)/Eo

        # calculation of a's
        a[i] = k

        for l in range(1, i):
            a[l] = ao[l] - k*ao[i-l]

        E = (1-k*k)*Eo

    a[0] = 1.0
    a[1:len(a)] = -a[1:len(a)]
    b = np.zeros(a.shape)
    b[0] = 1

    w, h = signal.freqz(b, a)

    plt.plot(fSamp*w/(2*pi), 10*filterOrder + 20 * np.log10(abs(h)), colors[filterOrder])

formants = np.asarray([730, 1090, 2440])
bandwidths = np.asarray([50, 50, 50])

# Calculate pole angles and radii
R = np.exp(-pi*bandwidths/fSamp)
theta = 2*pi*formants/fSamp

# Get poles and an equal number of zeros
poles = np.concatenate([R * np.exp(1j*theta), R * np.exp(-1j*theta)])
zeros = np.zeros(poles.shape, poles.dtype)

# Get transfer function
b, a = signal.zpk2tf(zeros, poles, 1)

# Get frequency response
wf, hf = signal.freqz(b, a)

# Plot
plt.plot(fSamp*wf/(2*pi), 120 + 20 * np.log10(abs(hf)), 'c')
for t in range(0,len(formants)):
    plt.axvline(formants[t],color='c',linestyle='--')
plt.legend(['Order 2', 'Order 4', 'Order 6', 'Order 8', 'Order 10', 'Orig'])
plt.grid()
#plt.savefig('1-'+str(harmFreq)+'.png')

plt.show()