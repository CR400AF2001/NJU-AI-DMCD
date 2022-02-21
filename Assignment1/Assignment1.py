import datetime

import pandas as pd
import numpy as np

import apriori
import fp_growth
import exhaustive_search


min_supp = 0.05
min_conf = 0.05


def do_apriori(data):
    print("apriori")
    start = datetime.datetime.now()
    items, rules = apriori.runApriori(data_iter=data, minSupport=min_supp, minConfidence=min_conf)
    end = datetime.datetime.now()
    print("total time: " + str((end - start).total_seconds()) + "s")
    print("num of frequent itemsets: " + str(len(items)))
    for item in items:
        print(str(item))
    print("num of frequent rules: " + str(len(rules)))
    for rule in rules:
        print(str(rule))


def do_fp_growth(data):
    print("fp_growth")
    minSupport = min_supp * len(data)
    start = datetime.datetime.now()
    items = list(fp_growth.find_frequent_itemsets(transactions=data, minimum_support=minSupport))
    end = datetime.datetime.now()
    print("total time: " + str((end - start).total_seconds()) + "s")
    print("num of frequent itemsets: " + str(len(items)))
    for item in items:
        print(str(item))


def do_exhaustive_search(data):
    print("exhaustive_search")
    minSupport = min_supp * len(data)
    start = datetime.datetime.now()
    dic = dict(exhaustive_search.exhaustive(data=data))
    num = 0
    for each in list(filter(lambda x: dic[x] > minSupport, dic.keys())):
        print(each, dic[each])
        num += 1
    print("num of frequent itemsets: " + str(num))
    end = datetime.datetime.now()
    print("total time: " + str((end - start).total_seconds()) + "s")


if __name__ == "__main__":
    data = pd.read_csv("dataset/GroceryStore/Groceries.csv")
    data = np.array(data)
    data_array = []
    for item in data:
        row_array = str(item[1])[1:-1].split(',')
        data_array.append(row_array)
    do_apriori(data_array)
    do_fp_growth(data_array)
    # do_exhaustive_search(data_array)

    for i in range(0, 9):
        with open('dataset/UNIX_usage/USER' + str(i) + '/sanitized_all.981115184025', 'r') as f:
            with open('dataset/UNIX_usage/USER' + str(i) + '/data.csv', 'w') as g:
                lines = f.readlines()
                begin = False
                for l in lines:
                    t = l.strip('\n')
                    if t == "**SOF**":
                        begin = True
                        continue
                    elif t == "**EOF**":
                        if begin:
                            continue
                        g.write('\n')
                    else:
                        if begin:
                            g.write(t)
                            begin = False
                        else:
                            g.write(',')
                            g.write(t)

    data_array = []
    for i in range(0, 9):
        with open('dataset/UNIX_usage/USER' + str(i) + '/data.csv', 'r') as f:
            lines = f.readlines()
            for l in lines:
                row_array = str(l.strip('\n')).split(',')
                real_array = []
                start = True
                temp = ''
                dic = {}
                for item in row_array:
                    if start:
                        temp = item
                        start = False
                    else:
                        if len(item) < 1:
                            continue
                        if 'a' <= item[0] <= 'z':
                            if temp in dic.keys():
                                continue
                            dic[temp] = 1
                            real_array.append(temp)
                            temp = item
                        else:
                            temp = temp + ' ' + item
                real_array.append(temp)
                data_array.append(real_array)

    do_apriori(data_array)
    do_fp_growth(data_array)
    # do_exhaustive_search(data_array)