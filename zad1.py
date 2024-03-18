import sys
from collections import defaultdict

def flatten(list_of_lists):
    flattened_list = [item for sublist in list_of_lists for item in sublist]
    return flattened_list

def colection_map(lista, f):
    return list(map(f, lista))

def flatmap(lista, f):
    return flatten(colection_map(lista,f))

def load_txt(fname):
    list2 = []
    with open(fname,'r') as f:
        lines = f.readlines()
        for line in lines:
            list2.append(line[:-1])
        return list2

def reduceByKey(pairs, f):
    reduced_dict = defaultdict(list)
    for key, value in pairs:
        reduced_dict[key].append(value)
    reduced_pairs = [(key, f(values)) for key, values in reduced_dict.items()]
    
    return reduced_pairs

list1 = load_txt(sys.argv[1])
print(list1)

f = lambda x: x.split()
word_to_pair_lambda = lambda word: (word, 1)
sum_values_lambda = lambda values: sum(values)

result = colection_map(list1, f)
print(result)
result1 = flatmap(list1, f)
print(result1)
result2 = colection_map(result1, word_to_pair_lambda)
print(result2)
reduced_pairs = reduceByKey(result2, sum_values_lambda)
print(reduced_pairs)