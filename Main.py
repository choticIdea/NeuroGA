import random
import math;
import xlrd;
import copy;

def generateKromosom():
    genotype = [];
    for i in range(0,numWeights*bitsPerElement):
        genotype.append(random.randint(0,1));
    return genotype;
def getIncrement(k):
    i = 0;
    inc = 0;
    while i < len(k) -1:
        inc += k[i+1] - k[i];
        i+=1;
    return inc;
def createZeros(size):
    mat = []
    for i in range(size):
        mat.append(0);
    return mat;
def prepareWeight(h,o,kromosom):
    offset = o * h;
    w = []
    for i in range(offset,offset+h):
        w.append(kromosom[i]);

    return w
def getData(first,last):
    dat =[];
    for i in range(first,last+1):
        dat.append(data[i][10]);
    return dat;
def decodeKromosom(k):
    weights = [];
    start = len(k)-1;
    w = 0;
    for i in range(start,-1,-1):
        w += math.pow(2, (i % bitsPerElement)) * k[i];
        if(i % bitsPerElement == 0 and i < start):

            w = (w / maxBitsVal) * (maxWeight - minWeight);
            w = w - maxWeight;

            weights.append(w);
            w = 0;

    return weights;
def crossover(pops,a,b):
    rng = random.randint(1,100);
    cutting = len(a) *(rng/100);
    if(cutting == len(a) - 1):
        cutting = cutting -1;
    x = createZeros(len(a));
    y  = createZeros(len(a));
    for i in range(len(x)):
        if(i < cutting):
            x[i] = a[i];
            y[i] = b[i];
        else :
            x[i] = b[i];
            y[i] = a[i];
    pops.append(x);
    pops.append(y);
    mut = random.randint(0,100);
    if(mut > mutationChance):
        ma = mutate(x);
        mb = mutate(y);
        pops.append(ma);
        pops.append(mb);
def mutate(k):
    rng = random.randint(1,100);
    for i in range(len(k)):
       if(rng > mutationChance):
        if(k[i] == 0):
               k[i] = 1;
        else :
                k[i]=0;
    return k;

minWeight = -1;
maxWeight = 1;
inputBits = 3;
maxHiddenLayer = 16;
hiddenLayer = 3;
timeWindow = 3;
maxTimeWindow = 10;
numWeights = (timeWindow*hiddenLayer)+hiddenLayer;
bitsPerElement = 10;
maxBitsVal  = math.pow(2,bitsPerElement);
epoch = 0;
maxEpoch = 150;
mutationChance = 40;
book = xlrd.open_workbook("DataHistorisANTAM.xlsx");
sheet = book.sheet_by_index(0);
data = []
drow = []
for row in range(1, sheet.nrows):
    drow = [];
    for col in range(sheet.ncols):
        drow.append(sheet.cell_value(row, col));
    data.append(drow);
startingPops = 50;
pops = [];
sumSE = 0;
bestMSE = -1;
for i in range(startingPops):
    pops.append(generateKromosom());


while epoch < maxEpoch:
    clone = copy.copy(pops);
    while len(clone) != 0:
        crossover(pops,clone.pop(),clone.pop());
    #examining pops
    msePop = [];

    for p in pops:
        last = timeWindow-1;
        first = 0;
        while (last < len(data)-1):
            row = getData(first,last);
            first += 1;
            last+=1
            if(last >= len(data)-1):
                last = len(data)-1
            inValue = createZeros(hiddenLayer);
            t = decodeKromosom(p);
            hidden_neuron = [t[0:3], t[3:6], t[6:9]]
            output_neuron = t[-3:]
            a = [0 for i in range(len(hidden_neuron))]
            output = 0
            for i in range(len(hidden_neuron)):
                tmp = [0 for z in range(len(hidden_neuron[i]))]
                tmpSum = [0 for z in range(len(hidden_neuron[i]))]
                for j in range(len(hidden_neuron[i])):
                    tmp[j] = hidden_neuron[i][j] * row[j]
                for j in range(len(hidden_neuron[i])):
                    tmpSum[j] = (tmp[j] - min(tmp)) / abs((max(tmp) - min(tmp)))
                a[i] = sum(tmpSum)
                a[i] /=  float(j+1)
            # print a
            for i in range(len(output_neuron)):
                output += output_neuron[i] * a[i]
            output /= float(i+1)
            current_input_avg = (abs(row[0] - row[1]) + abs(row[1] - row[2])) / float(2)
            avg = output * current_input_avg + row[-1];

            # for i in range(len(row)):


            #     w = prepareWeight(hiddenLayer,i,t);

            #     for j in range(len(row)):
            #         inValue[j] += w[j]* row[j];

            # sum = 0;
            # temp = copy.copy(inValue);
            # temp.sort();
            # min = temp[0];
            # max = temp.pop();
            # for i in range(len(inValue)):
            #     inValue[i] = (inValue[i] - min)/abs((max-min));

            #     sum+= inValue[i];

            # output_sum = 0
            # for nz in range(len(output_neuron)):
            #     output_sum += output_neuron[nz] * inValue[nz]
            # # mean = sum/hiddenLayer;
            # mean = output_sum / (nz+1)
            # avg = mean * getIncrement(row)+row[len(row)-1];# k is the whole input, or every avg coloumn in a time window;

            e = 0;
            if(last+1 <= len(data) -1):
                e = abs(data[last+1][10] - avg);
            else:
                e = 0;
            sumSE += e*e;
            # print(temp);
            # print(max);
            # print(min);

        mse = sumSE/(len(data));
        sumSE = 0;
        msePop.append(mse);

    #select parents, generate new pop, replace old one
    idx = 0;
    for i in range(len(pops)):
        for k in range(i, len(pops)):
            if (bestMSE == -1 or bestMSE > msePop[k]):
                bestMSE = msePop[k];
                idx = k;

        t = pops[i];
        pops[i] = pops[idx];
        pops[idx] = t;
        t = msePop[i];
        msePop[i] = msePop[idx];
        msePop[idx] = t;

        idx = -1;
        bestMSE = -1;
    print(msePop);
    #cull weak individuals
    pops = pops[:startingPops];
    msePop = msePop[:startingPops];
    print(msePop);
    epoch+= 1;
print pops[0]