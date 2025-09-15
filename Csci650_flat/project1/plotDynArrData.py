#Python script to plot time data for dynamic arrays
import matplotlib
matplotlib.use("Agg")

import numpy as np
import matplotlib.pyplot as plt

#read data from stdin
def readData():
    data = {}
    cur = 0
    while True:
        try:
            line = input().strip().split()
            if not line:
                continue
            if line[0] == 'Count': 
                cur = int(line[1])
                data[cur] = []
            elif line[0] == 'Repeat': continue
            else: data[cur].append(list(map(float, line)))
        except EOFError:
            break
    return data

if __name__=='__main__':
    growNames = {0: 'Double', 1: 'Add 1', 2: 'Add 100'}
    data = readData()

    #plot operation number vs time
    plt.figure()
    for k in data:
        X = range(1, len(data[k][0])+1)
        Y = [np.mean([rep[x] for rep in data[k]]) for x in range(len(data[k][0]))]
        E = [np.std([rep[x] for rep in data[k]]) for x in range(len(data[k][0]))]

        plt.plot(X, Y, markersize=2, alpha=0.5, label=growNames[k])        
    
    plt.title('Dynamic Array Runtimes')
    plt.xlabel('Operation Number')
    plt.ylabel('Time (s)')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig('ops_vs_time.png', dpi=200)
    plt.close()

    #plot operation number vs cumulative time
    plt.figure()
    for k in data:
        X = range(1, len(data[k][0])+1)
        Y = [np.mean([rep[x] for rep in data[k]]) for x in range(len(data[k][0]))]
        E = [np.std([rep[x] for rep in data[k]]) for x in range(len(data[k][0]))]

        plt.plot(X, np.cumsum(Y), alpha=0.5, label=growNames[k])

    plt.title('Dynamic Array Runtimes')
    plt.xlabel('Operation Number')
    plt.ylabel('Cumulative Time (s)')
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig('ops_vs_cumtime.png', dpi=200)
    plt.close()
