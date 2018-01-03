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

Tested = 0;
incorrect = 0;
%rows predicted(output) class & columns target class 
confusionMatrix = zeros(10, 10);

for leftOut = 1:16
    
    complete_data = {};
    ids = [];
    ptr = 1;

    for speakerIndex = 1:16
        if speakerIndex ~= leftOut
            for recordings = 1:2
                for digit = 0:9
                    for utterance = 0:1
                        
                        [extracted_data, fSampling] = audioread(strcat('bof/', speakers{speakerIndex}, num2str(recordings), num2str(digit), num2str(utterance), '.wav'));
                        disp(strcat('Training/', speakers{speakerIndex}, num2str(recordings), num2str(digit), num2str(utterance), '.wav'));
                        complete_data{ptr} = extracted_data;
                        ids(ptr) = digit;
                        ptr = ptr + 1;
                        
                    end
                end
            end
        end
    end
    
    
    disp('Trained!!!');
    
    % Test
    for recordings = 1:2
        for digit = 0:9
            for utterance = 0:1

                [extracted_data, fSampling] = audioread(strcat('bof/', speakers{leftOut}, num2str(recordings), num2str(digit), num2str(utterance), '.wav'));
                disp(strcat('Testing/', speakers{leftOut}, num2str(recordings), num2str(digit), num2str(utterance), '.wav'));
                
                minDistIds = 0;
                minDistance = Inf;
                for i = 1:size(complete_data, 2)
                    
                    disp([strcat('checking/',speakers{leftOut}, num2str(recordings), num2str(digit), num2str(utterance), '.wav')]);
                    
                    tempDistance = DTWdist(extracted_data, complete_data{i}, fSampling, lowf, highf, nFilt, fftSize);
                    if tempDistance < minDistance
                        
                        minDistance = tempDistance;
                        minDistIds = i;
                        
                    end
                    
                end
                PredictedDigit = ids(minDistIds);
                
                % Statistics
                Tested = Tested + 1;
                incorrect = incorrect + (PredictedDigit ~= digit);
                
                % confusion matrix
                confusionMatrix(1+digit, 1+PredictedDigit) = confusionMatrix(1+digit, 1+PredictedDigit) + 1;
                              
            end
        end
    end
end
wer = sum(incorrect)/sum(Tested) * 100; disp(wer);
filename = 'test.mat';
save(filename);