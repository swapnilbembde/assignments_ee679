format longg;
format compact;
clc;	% Clear command window.
workspace;	
close all;
fs = 16e3;
b1 = 100 ;
f1 = 300;
f0 = 180;
T = 1/fs;
r =exp(-pi*b1*T);
theta = 2*pi*f1*T;
%%%% triangular pulse
triang = bartlett(9);
n = fs/f0;
imp=zeros(1,8000);
for i= 1:n:8000
    imp(uint16(i):uint16(i)+8)= triang;
end

y(1)=imp(1);
y(2)=(r*exp(1i*theta)+r*exp(-1i*theta))*y(1)+imp(2);

for k=3:8000
   y(k)=-r*r*y(k-2)+(r*exp(1i*theta)+r*exp(-1i*theta))*y(k-1)+imp(k);
end
%audiowrite('3c.wav',y,fs);
x = 0 : length(y)-1;
plot(x,y);