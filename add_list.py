#!/usr/bin/env python3
# this program import give an number array, and expect a combine of element to add  get the result of  a certain number..
import itertools

print("请输入一维数组以,分隔:")
arr = input("")
arrlist = [float(n) for n in arr.split(',')]
# print(arrlist)
print("请输入求和结果:")
equValue = float(input(""))

reslist = []

for i in range(1,len(arrlist)+1):
    iter = itertools.combinations(arrlist,i)
    reslist.append(list(iter)) 


print("如下组合相加,可以得到结果:",equValue)
for a in reslist:
    for b in a:
        if round(sum(b),2) == equValue :
        #if sum(b) < 2 and sum(b) > -2:
            #print(b,sum(b))
            print(b,round(sum(b),2))
