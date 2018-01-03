function distanceSum = DTWdist(inp1, inp2, fSampling, lowf, highf, nFilts, fftSize)

    mfccinp1 = calcMFCC(inp1, fSampling, lowf, highf, nFilts, fftSize);
    mfccinp2 = calcMFCC(inp2, fSampling, lowf, highf, nFilts, fftSize);
   
    %This is the function directly gives the output
    %%[distanceSum,~,~] = dtw(mfccinp1,mfccinp2);    
    n = size(mfccinp1, 2);
    m = size(mfccinp2, 2);
    distanceMatrix = zeros(n, m);
    for i = 1:n
        for j = 1:m

            distanceMatrix(i, j) = norm(mfccinp1(:, i) - mfccinp2(:, j));
        end
    end
    
    DyanmicWarping = zeros(n+1, m+1);
    
    for i = 2:n+1
        DyanmicWarping(i, 1) = Inf;
    end
    for i = 2:m+1
        DyanmicWarping(1, i) = Inf;
    end
    DyanmicWarping(1, 1) = 0;
    
    for i = 2:n+1
        for j = 2:m+1
            
            cost = distanceMatrix(i-1, j-1);
            DyanmicWarping(i, j) = cost + min(DyanmicWarping(i-1, j), min(DyanmicWarping(i-1, j-1), DyanmicWarping(i, j-1)));
            
        end
    end
    
    distanceSum = DyanmicWarping(n+1, m+1);
  
end