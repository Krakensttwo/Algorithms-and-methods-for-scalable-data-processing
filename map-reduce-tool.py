import sys

def load_txt(fname):
    list2 = []
    with open(fname,'r') as f:
        lines = f.readlines()
        for line in lines:
            list2.append(line[:-1])
        return list2
    
def flatten(listA):
    

def collection_map(listA):
    listB = []
    for line in listA:
        listB.append(line.split())
    return listB


list1 = load_txt(sys.argv[1])
print(list1)
list2 = collection_map(list1)
print(list2)