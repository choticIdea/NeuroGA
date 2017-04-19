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
    while i < len(k):
        inc += k[i] + k[i+1];
        i+=1;
    return inc;
def createZeros(size):
    mat = []
    for i in range(size):
        mat.append(0);
    return mat;
def prepareWeight(maxHiddenLayer,o,kromosom):
    offset = o * maxHiddenLayer;
    w = []
    for i in range(offset,offset+maxHiddenLayer-1):
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
    for i in range(start,0,-1):
        if(i % bitsPerElement == 0 and i < start):
            w = (w / maxBitsVal) * (maxWeight - minWeight);
            w = w - maxWeight;
            weights.append(w);
            w = 0;
        else :
            w += math.pow(2,(i%bitsPerElement))*i;

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
    pops.append(a);
    pops.append(b);
    mut = random.randint(0,100);
    if(mut > mutationChance):
        pops.append(mutate(a));
        pops.append(mutate(b));
def mutate(k):
    rng = random.randint(1,100);
    for i in range(len(k)):
       if(rng > mutationChance):
        if(k[i] == 0):
               k[i] = 1;
        else :
                k[i]=0;
input = 6;
minWeight = -1;
maxWeight = 1;
inputBits = 3;
maxHiddenLayer = 16;
hiddenLayer = 3;
timeWindow = 3;
maxTimeWindow = 10;
numWeights = (input*hiddenLayer)+hiddenLayer;
bitsPerElement = 10;
maxBitsVal  = math.pow(2,bitsPerElement);
epoch = 0;
maxEpoch = 300;
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
    msePop = createZeros(len(pops));
    for p in pops:
        last = 0;
        first = 0;
        while (last < len(data)):
            last = timeWindow - 1;
            row = getData(first,last);
            first = last+1;
            inValue = createZeros(hiddenLayer);
            for i in range(len(row)):
                t = decodeKromosom(p);
                print(len(t));
                w = prepareWeight(maxHiddenLayer,i,t);
                for i in range(len(inValue)):
                    inValue[i] += w[i]* row[i];

            sum = 0;
            temp = copy.copy(inValue);
            temp.sort();
            min = temp[0];
            max = temp.pop();
            for i in range(len(inValue)):
                inValue[i] = (inValue[i] - min)/(max-min);
                sum+= inValue[i];
            mean = sum/hiddenLayer;
            avg = mean * getIncrement(row)+row[last];# k is the whole input, or every avg coloumn in a time window;
            e = abs(data[last+1] - avg);
            sumSE += e*e;
        mse = sumSE/(len(data) - timeWindow);
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
    #cull weak individuals
    pops = pops[:startingPops];
    epoch+= 1;
