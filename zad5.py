import sys
from collections import defaultdict
from functools import reduce

def load_txt(fname):
    list2 = []
    with open(fname,'r') as f:
        list2 = [tuple(map(int,line.split(','))) for line in f]
    return list2

def flatmap(lista, f):
    return flatten(collection_map(lista,f))

def flatten(list_of_lists):
    flattened_list = [item for sublist in list_of_lists for item in sublist]
    return flattened_list

def collection_map(lista, f):
    return list(map(f, lista))

def reduceByKey(kolekcja, f):
    result_dict = {}
    result = []
    for key, value in kolekcja:
        if key in result_dict:
            result_dict[key]=f(result_dict[key], value)
        else:
            result_dict[key] = value
    for key, value in result_dict.items():
        result.append((key,value))
    return result

def crossJoinByKey(m1,m2):
    list1 = []
    for k1 in m1:
        for k2 in m2:
            if k1[0] == k2[0]:
                list1.append((k1[0],(k1[1],k2[1])))
    return list1

list1 = load_txt(sys.argv[1])
# [(1,3), (3,5), ..., (4,2)]
#print(list1)

fA = lambda p: ((p[0],p[1]),(p[1],p[0]))
fP1 = lambda p: (p[0],0)
fR = lambda a,b: a+b
fP2 = lambda p: p[0]
fPe = lambda p: (p,p,True)
fT = lambda t: (t[1][1],(t[0],t[1][0]))
fS1 = lambda a,b: (a[0],min(a[1],b[1]))
fS2 = lambda t: (t[0],min(t[1][0],t[1][1]))
fS3 = lambda s: (s[0],(s[0],s[1]))
fZ1 = lambda p: p[2]
fZ2 = lambda p,q: p or q

fW1 = lambda w: (w[1][1],(w[0],(w[1][0],w[1][1])))
fW2 = lambda w: (w[1])
fW3 = lambda w: (w[0][0],w[1])
fPe2 =lambda s: (s[0],min(s[1][0],s[1][1]),s[1][1] < s[1][0]) 

fM1 = lambda s: (s[1][1][1],(s[0],(s[1][0])))
fM2 = lambda s: (s[1][0] == s[1][1][1],(s[0],(s[1][1][0])))
fM3 = lambda a,b: a+b
fM4 = lambda s: s[0]
fM5 = lambda s: (s,0)
fM6 = lambda s: (s[0],s[1][1])
fM7 = lambda s: (s[1][1][1],(s[0],s[1][0]))
fM8 = lambda s: (s[0],s[1][0])
fM9 = lambda s: (s[1][1][0],(min(s[1][0][1],s[1][1])))
fM10 = lambda a,b: b

listA = flatmap(list1, fA)
#print(listA)
# [(1,3), (3,1), ..., (4,2), (2,4)]
listP = collection_map(reduceByKey(collection_map(listA, fP1),fR),fP2)
# [1,3, ...,4,2)]
#print(listP)
listPe = collection_map(listP,fPe)
# [(1,1, True), (3,3, True), ..., (2,2, True)]
#print(listPe)
listT = crossJoinByKey(listPe,listA)
#print(listT)
# [(1, (1,3)), (3, (3,1)), (3, (3,5)),..., (2, (4,2))]

listS = collection_map(collection_map(reduceByKey(listT,fS1),fS2),fS3)
#print("list S: ",listS)
# [(1, (1,1)), (3, (3,1)), ..., (2, (2,2))]


z = reduce(fZ2,collection_map(listPe,fZ1))
#print("list Z1: ", z)
while z:
    print("--------------------------------------------")
    listW1 = collection_map(listS,fW1)
    #print("list W1: ", listW1)
    # [(1, (1, (1,1))), (1, (3, (3,1)), ..., (2, 2, (2,2))]
    listW2 = collection_map(crossJoinByKey(listW1,listS),fW2)
    #print("list W2: ",listW2)
    # [((1, (1,1)), (1,1)), ((3, (3,1)), (1,1)), ..., ((2, (2,2)), (2,2))]
    listS = collection_map(listW2,fW3)
    print("list S: ",listS)
    # [(1, (1,1)), (3, (1,1)), ..., (2, (2,2))]
    listPe = collection_map(listS, fPe2)
    z = reduce(fZ2,collection_map(listPe,fZ1))
    #print("list Z2: ",z)
    if z == False:
        listM = collection_map(crossJoinByKey(listS,listT),fM1)
        #print(listM)
        listM2 = collection_map(crossJoinByKey(listS,listM),fM2)
        #print(listM2)
        listM3 = reduceByKey(listM2,fM3)
        #print(listM3)
        z = reduce(fZ2,collection_map(listM3,fM4))
        #print("list Z3: ",z)
        if len(listM3) == 1:
            break
        listM4 = [listM3[1]]
        listM5 = collection_map(list(set(listM4[0][1])),fM5)
        #print(listM5)
        listM6 = collection_map(crossJoinByKey(listM5,listS),fM6)
        #print(listM6)
        listM7 = collection_map(crossJoinByKey(listM6, listT),fM7)
        #print(listM7)
        listM8 = collection_map(crossJoinByKey(collection_map(crossJoinByKey(listM7, listM5),fM8),listS),fM9)
        #print(listM8)
        listS = reduceByKey(listS + listM8,fM10)
        #print(listS)
print("--------------------------------------------")
print("list FiN: ",listS)



