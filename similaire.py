import itertools
import csv
import numpy as np

words = {}
i=1
for row in open("csv/skills_no_duplicate_sorted.csv"):
    i=i+1
    print(i)
    parts = row.rstrip().split(',')
    for a,b in itertools.combinations(parts,2):
        if(a!='' and b!=''):
            if a not in words:
                words[a] = [b]
            else:
                words[a].append( b )
            if b not in words:
                words[b] = [a]
            else:
                words[b].append( a )

print("words done")
size = len(words)
keys = list(words.keys())
track = np.zeros((size,size))

for i,k in enumerate(keys):
    track[i,i] = len(words[k])
    for j in words[k]:
        track[i,keys.index(j)] += 1
        track[keys.index(j),i] += 1


print("keys done")

# Scale to [0,1].

for row in range(track.shape[0]):
    track[row,:] /= track[row,row]

# Create a csv with the results.

fout = open('correspendentFinalCleanSorted.csv','a')
print( ','.join([' ']+keys), file=fout )
for row in range(track.shape[0]):
    print( keys[row], file=fout, end=',')
    print( ','.join(f"{track[row,i]}" for i in range(track.shape[1])), file=fout )
fout.close()
