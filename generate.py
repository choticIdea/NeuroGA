import random
import math;
import xlrd;
import copy;

def decodeKromosom(k):
    weights = [];
    start = len(k)-1;
    bitsPerElement = 10;
    maxBitsVal  = math.pow(2,bitsPerElement);
    minWeight = -1;
    maxWeight = 1;
    w = 0;
    for i in range(start,-1,-1):
        w += math.pow(2, (i % bitsPerElement)) * k[i];
        if(i % bitsPerElement == 0 and i < start):
            w = (w / maxBitsVal) * (maxWeight - minWeight);
            w = w - maxWeight;
            weights.append(w);
            w = 0;
    return weights;

all_weights = decodeKromosom([1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1])

initial_avg = [697, 714, 714]

hidden_weights = [all_weights[0:3], all_weights[3:6], all_weights[6:9]]
output_weights = all_weights[9:12]

print "hidden weights", hidden_weights
print "output weights", output_weights

for x in range(7):
    current_input = initial_avg[-3:]
    a = [0 for i in range(len(hidden_weights))]
    output = 0
    for i in range(len(hidden_weights)):
        tmp = [0 for z in range(len(hidden_weights[i]))]
        tmpSum = [0 for z in range(len(hidden_weights[i]))]
        for j in range(len(hidden_weights[i])):
            tmp[j] = hidden_weights[i][j] * current_input[j]
        for j in range(len(hidden_weights[i])):
            tmpSum[j] = (tmp[j] - min(tmp)) / abs((max(tmp) - min(tmp)))
        a[i] = sum(tmpSum)
        a[i] /=  float(j+1)
    print a
    for i in range(len(output_weights)):
        output += output_weights[i] * a[i]
    output /= float(i+1)
    current_input_avg = (abs(current_input[0] - current_input[1]) + abs(current_input[1] - current_input[2])) / float(2)
    initial_avg.append((output * current_input_avg) + current_input[-1])

print initial_avg