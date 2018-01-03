clc;
workspace;
close all;
speakers = { 'Mayur','Shrikant','Vedhas', 'Niramay',...
    'divyansh','Jatin', 'Hitesh', 'Kaustuv', 'Ankita',...
    'Kamini','Mansi','Pragya','Prarthana','Reshma',...
    'Richa','Shradha'};
lowf = 150;
highf = 7000;
nFilt = 40;
fftSize = 1024;
nClusters = 80;

Tested = 0;
incorrect = 0;
%rows predicted(output) class & columns target class 
confusionMatrix = zeros(10, 10);

for leftOut = 1:16
    
    MfccVectors = [];
    MfccIndex = [];
    
    for digit = 0:9
        for recordings = 1:2
            for speakerIndex = 1:16
                if speakerIndex ~= leftOut
                    for utterance = 0:1

                         % Training
                        [extracted_data, fSampling] = audioread(strcat('bof/', speakers{speakerIndex}, num2str(recordings), num2str(digit), num2str(utterance), '.wav'));
                        mfccs = calcMFCC(extracted_data, fSampling, lowf, highf, nFilt, fftSize);
                        MfccVectors = [MfccVectors; mfccs']; 
                        MfccIndex = [MfccIndex; repmat(digit, size(mfccs, 2), 1)];
                        
                    end
                end
            end
        end
    end
    disp('Trained!!!')   
    % Vector Quantization using kmeans
    MfccVectorsK = zeros(10*nClusters, 13);
    MfccIndexK = zeros(10*nClusters, 1);
    
    for digit = 0:9
        tempIndex = find(MfccIndex == digit);
        tempVectors = MfccVectors(tempIndex(1):tempIndex(end), :);
        
        [~, centers] = kmeans(tempVectors, nClusters);%,'MaxIter',1000);
        MfccVectorsK((digit*nClusters+1:digit*nClusters+nClusters), :) = centers;
        disp([strcat('vectors ',num2str(digit),num2str(leftOut))]);
        MfccIndexK(digit*nClusters+1:digit*nClusters+nClusters) = digit;
        
    end
    MfccVectors = MfccVectorsK;
    MfccIndex = MfccIndexK;
    
    for recordings = 1:2
        for digit = 0:9
            for utterance = 0:1
                % Testing
                [extracted_data, fSampling] = audioread(strcat('bof/', speakers{leftOut}, num2str(recordings), num2str(digit), num2str(utterance), '.wav'));
                mfccs = calcMFCC(extracted_data, fSampling, lowf, highf, nFilt, fftSize);
                mfccRec = knnsearch(MfccVectors, mfccs');
                PredictedDigit = mode(MfccIndex(mfccRec));
                
                % Results 
                Tested = Tested + 1;
                incorrect = incorrect + (PredictedDigit ~= digit);
                
                % confusion matrix
                confusionMatrix(1+digit, 1+PredictedDigit) = confusionMatrix(1+digit, 1+PredictedDigit) + 1;
                    
            end
        end
    end
    
end

wer = sum(incorrect)/sum(Tested) * 100; disp(wer);