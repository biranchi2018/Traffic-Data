import os
import csv

path = '/home/project/traffic/data/'

filename = [path + i for i in os.listdir(path)]

for i in filename:
    with open(i, 'rb') as fopen:
        string = fopen.read().split('\n')
    
    for x in xrange(len(string)):
        string[x] = string[x].split('\t')
        
    with open(i + '.csv', 'wb') as fopen:
        writer = csv.writer(fopen, delimiter = ',')
        for n in string:
            writer.writerow(n)
            
           