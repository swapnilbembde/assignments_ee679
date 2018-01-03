format longg;
format compact;
clc;	% Clear command window.
workspace;	% Make sure the workspace panel is showing.
close all;
fs = 16e3;
f0 = 220;
f1 = 300;
f2 = 870;
f3 = 2240;
b1= 100;
T = 1/fs;
r = exp(-pi*b1*T);
triang = bartlett(9);
n = fs/f0;
imp=zeros(1,8000);
for i= 1:n:8000
    imp(uint16(i):uint16(i)+8)= triang;
end

theta1 = 2*pi*f1*T;
theta2 = 2*pi*f2*T;
theta3 = 2*pi*f3*T;

a = r*exp(1i*theta1);
b = r*exp(1i*theta2);
c = r*exp(1i*theta3);
%%%instead of finding out all the coefficients of DE, convolving is better way  
cof1 = conv([1 -a],[1 -conj(a)]);
cof2 = conv([1 -b],[1 -conj(b)]);
cof3 = conv([1 -c],[1 -conj(c)]);
coefs = conv(cof1,conv(cof2,cof3));

y = zeros(size(imp));
for k = 1:max(size(imp))
    y(k) = imp(k);
    if k>1
        y(k) = y(k) - coefs(2)*y(k-1);
    end
    if k>2
        y(k) = y(k) - coefs(3)*y(k-2);
    end
    if k>3
        y(k) = y(k) - coefs(4)*y(k-3);
    end
    if k>4
        y(k) = y(k) - coefs(5)*y(k-4);
    end
    if k>5
        y(k) = y(k) - coefs(6)*y(k-5);
    end
    if k>6
        y(k) = y(k) - coefs(7)*y(k-6);
    end
    y(k) = y(k)/coefs(1);
end
audiowrite('4u_220hz.wav',y,fs);
x = 0 : length(y)-1;
plot(x,y);