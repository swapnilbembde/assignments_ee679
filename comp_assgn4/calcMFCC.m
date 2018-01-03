function mfcc = calcMFCC(input_data, fSampling, lowf, highf, nFilts, fftSize)

    FrameSize = fSampling/100;
    nVectors = floor(size(input_data, 1)/FrameSize) - 1;
    mfcc = zeros(13, nVectors);

    melFiltBank = melFilter(nFilts, lowf, highf, fSampling, fftSize);

    for i = 1:nVectors

        win = hamming(FrameSize).*input_data(((i-1)*FrameSize/2+1):((i-1)*FrameSize/2+FrameSize));

        winFFT = abs(fft(win, fftSize));
        winFFT = winFFT(1:size(melFiltBank, 2));
        FrameEnergy = (winFFT.^2)/(fftSize);

        melEnergy = log(melFiltBank*FrameEnergy);

        allCoeffs = dct(melEnergy);
        mfcc(:, i) = allCoeffs(1:13);

    end
end

