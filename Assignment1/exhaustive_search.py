def exhaustive(data):
    maxItemLength = max([len(each) for each in data])
    allItems = []
    for i in data:
        for j in i:
            if not j in allItems:
                allItems.append(j)
    dic = {}
    for i in range(maxItemLength):
        nr = i + 1
        for each in combinations(allItems, nr)[0]:
            each = tuple(each)
            if not each in dic.keys():
                dic[each] = 1
            else:
                dic[each] += 1
    return dic


def combinations(L, k):
    n = len(L)
    result = []
    for i in range(n - k + 1):
        if k > 1:
            newL = L[i + 1:]
            Comb, _ = combinations(newL, k - 1)
            for item in Comb:
                item.insert(0, L[i])
                result.append(item)
        else:
            result.append([L[i]])
    return result, len(result)
