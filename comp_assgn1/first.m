%%Q1
fontSize = 15;
fs = 16e3;
b1 =200 ;
f1 = 1e3;
T = 1/fs;
r =exp(-pi*b1*T);
theta = 2*pi*f1*T;
z = zpk('z',T);
h = 1/((1-r*exp(1i*theta)*z^-1)*(1-r*exp(-1i*theta)*z^-1));
hi = real(impulse(h));
plot(hi)
title('Impulse Response', 'FontSize', fontSize)
%[mag,phase,w]= bode(h);
%plot(mag,w)
%[n,d]= tfdata(h,'v');
%Hw =abs(freqz(n,d,1000));

%plot(linspace(0,pi,size(Hw,1)),20*log10(Hw));
%title('Magnitude(dB) vs frequency plot'); 
%%%%%%%%%%%%%%%%

