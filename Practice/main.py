import csv
from itertools import islice

import numpy as np
from deepforest import CascadeForestClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.preprocessing import OneHotEncoder


def main():
    # Author
    authorDict = {}
    with open('E:\\nju-dmcdo-final-mining-practice-track1\\resources\\Author.csv', 'r', encoding='utf-8') as f:
        rows = csv.reader(f)
        for row in islice(rows, 1, None):
            if row[0] not in authorDict.keys():
                authorDict[row[0]] = [row[1:]]
            else:
                authorDict[row[0]].append(row[1:])

    # Conference
    conferenceDict = {}
    with open('E:\\nju-dmcdo-final-mining-practice-track1\\resources\\Conference.csv', 'r', encoding='utf-8') as f:
        rows = csv.reader(f)
        for row in islice(rows, 1, None):
            conferenceDict[row[0]] = [row[1:]]

    # Journal
    journalDict = {}
    with open('E:\\nju-dmcdo-final-mining-practice-track1\\resources\\Journal.csv', 'r', encoding='utf-8') as f:
        rows = csv.reader(f)
        for row in islice(rows, 1, None):
            journalDict[row[0]] = [row[1:]]

    # Paper
    paperDict = {}
    with open('E:\\nju-dmcdo-final-mining-practice-track1\\resources\\Paper.csv', 'r', encoding='utf-8') as f:
        rows = csv.reader(f)
        for row in islice(rows, 1, None):
            paperDict[row[0]] = [row[1:]]

    # PaperAuthor
    paperAuthorDict = {}
    with open('E:\\nju-dmcdo-final-mining-practice-track1\\resources\\PaperAuthor.csv', 'r', encoding='utf-8') as f:
        rows = csv.reader(f)
        for row in islice(rows, 1, None):
            if row[0] not in paperAuthorDict.keys():
                paperAuthorDict[row[0]] = [row[2:]]
            else:
                paperAuthorDict[row[0]].append(row[2:])

    # train
    trainDict = {}
    with open('E:\\nju-dmcdo-final-mining-practice-track1\\resources\\train.csv', 'r', encoding='utf-8') as f:
        rows = csv.reader(f)
        for row in islice(rows, 1, None):
            trainDict[row[0]] = [row[1:]]

    train_x = []
    train_y = []
    for key in trainDict.keys():
        confirmedList = trainDict[key][0][0].split()
        deletedList = trainDict[key][0][1].split()
        for item in confirmedList:
            # addList = []
            addList = [key, item]
            flag = 0
            for author in paperAuthorDict[item]:
                for a in authorDict[key]:
                    if a[0] == author[0]:
                        addList.append(1)
                        flag = 1
                        break
                if flag == 1:
                    break
            if flag == 0:
                addList.append(0)
            flag = 0
            for author in paperAuthorDict[item]:
                for a in authorDict[key]:
                    if a[1] != "" and a[1] == author[1]:
                        addList.append(1)
                        flag = 1
                        break
                if flag == 1:
                    break
            if flag == 0:
                addList.append(0)
            train_x.append(addList)
            train_y.append(1)

        for item in deletedList:
            # addList = []
            addList = [key, item]
            flag = 0
            for author in paperAuthorDict[item]:
                for a in authorDict[key]:
                    if a[0] == author[0]:
                        addList.append(1)
                        flag = 1
                        break
                if flag == 1:
                    break
            if flag == 0:
                addList.append(0)
            flag = 0
            for author in paperAuthorDict[item]:
                for a in authorDict[key]:
                    if a[1] != "" and a[1] == author[1]:
                        addList.append(1)
                        flag = 1
                        break
                if flag == 1:
                    break
            if flag == 0:
                addList.append(0)
            train_x.append(addList)
            train_y.append(0)

    train_x = np.array(train_x)
    train_y = np.array(train_y)


    # test
    test_x = []
    with open('E:\\nju-dmcdo-final-mining-practice-track1\\test.csv', 'r', encoding='utf-8') as f:
        rows = csv.reader(f)
        for row in islice(rows, 1, None):
            test_x.append(row[1:])

    for i in range(0, len(test_x)):
        flag = 0
        for author in paperAuthorDict[test_x[i][1]]:
            for a in authorDict[test_x[i][0]]:
                if a[0] == author[0]:
                    test_x[i].append(1)
                    flag = 1
                    break
            if flag == 1:
                break
        if flag == 0:
            test_x[i].append(0)

        flag = 0
        for author in paperAuthorDict[test_x[i][1]]:
            for a in authorDict[test_x[i][0]]:
                if a[1] != "" and a[1] == author[1]:
                    test_x[i].append(1)
                    flag = 1
                    break
            if flag == 1:
                break
        if flag == 0:
            test_x[i].append(0)
        # test_x[i] = test_x[i][2:]

    test_x = np.array(test_x)

    encoder = OneHotEncoder()
    encoder.fit(np.append(train_x, test_x, axis=0))
    train_x = encoder.transform(train_x)

    model = XGBClassifier(
        n_estimators=5000
    )
    '''
    model = RandomForestClassifier(
        n_estimators=100
    )
    model = GradientBoostingClassifier(
        n_estimators=5000
    )
    model = CascadeForestClassifier(
        n_estimators=5
    )
    '''

    model.fit(train_x, train_y)
    pred_train_y = model.predict(train_x)
    predictions = [round(value) for value in pred_train_y]
    train_acc = np.mean(train_y == predictions)
    print(train_acc)

    test_x = encoder.transform(test_x)
    test_y = model.predict(test_x)
    predictions = [round(value) for value in test_y]
    with open('E:\\nju-dmcdo-final-mining-practice-track1\\submission.csv', 'w', encoding='utf-8', newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["Id", "Expected"])
        for i in range(0, len(predictions)):
            csv_writer.writerow([i, predictions[i]])



if __name__ == "__main__":
    main()
