#!/usr/bin/env python3
# this program import give an number array, and expect a combine of element to add  get the result of  a certain number..
import itertools

print("Hi,Pigee!")
arrlist = [0.20,29.70,69.25,-9.50,-3.10,12.90,0.05,0.05]
reslist = []

for i in range(1,len(arrlist)+1):
    iter = itertools.combinations(arrlist,i)
    reslist.append(list(iter)) 

for a in reslist:
    for b in a:
        if sum(b) < 2 and sum(b) > -2:
            print(b,round(sum(b),2))
