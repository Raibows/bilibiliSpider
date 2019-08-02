import sys
sys.path.append('..')
sys.path.append('.')
import MachineLearning
import csv


def bilibili_read_data(csv_path):
    input_data = []
    input_exp = []
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        flag = 1
        for line in reader:
            if flag > 1000:
                break
            if flag % 102 == 1 or flag % 102 == 2:
                flag += 1
                continue
            line = [float(item) for item in line]
            flag += 1
            data = line[2:8]
            input_exp.append(line[-2])
            input_data.append(data)
    return input_data, input_exp

def divide_data(input_data, input_exp):
    import random
    test_data = []
    test_exp = []
    for i in range(1):
        x = random.randint(0, len(input_data))
        test_data.append(input_data[x])
        test_exp.append(input_exp[x])
        del input_data[x]
        del input_exp[x]
    train_data = input_data
    train_exp = input_exp
    return {
        'train_vecs' : train_data,
        'train_exps' : train_exp,
        'test_vecs' : test_data,
        'test_exps' : test_exp,
    }



def bilibili_train():
    csv_path = r'../data/bilibili_data.csv'

    data = bilibili_read_data(csv_path)

    data = divide_data(data[0], data[1])

    variables = ['danmu', 'reply', 'favorite', 'coin', 'share', 'like']

    print(len(data.get('train_vecs')))
    print(len(data.get('train_exps')))

    train_vecs = data.get('train_vecs')
    train_exps = data.get('train_exps')

    MachineLearning.normalize_median(train_vecs, train_exps)

    model = MachineLearning.perceptron(
        variables=variables,
        train_vecs=train_vecs,
        train_exps=train_exps
    )

    model.train(
        train_iter_num=10000,
        rate=0.01
    )


def wine_train():
    csv_path = r'winequality-red.csv'
    input_vecs = []
    input_exps = []
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        for line in reader:
            # print(line)
            temp = [eval(_i) for _i in line]
            line = temp
            input_vecs.append(line[0:-1])
            # print(input_vecs)
            # import os
            # os._exit(-1)
            input_exps.append(line[-1])

    features = ['fixed acidity', 'volatile acidity', 'citric acid',
                'residual sugar', 'chlorides', 'free sulfur dioxide',
                'total sulfur dioxide', 'density', 'pH', 'sulphates',
                'alcohol', ]
    variables = [0.0 for _ in features]
    MachineLearning.normalize_median(input_vecs, input_exps)

    model = MachineLearning.perceptron(
        variables=variables,
        train_vecs=input_vecs,
        train_exps=input_exps
    )

    model.train(
        train_iter_num=10000,
        rate=0.0001
    )










if __name__ == '__main__':

    bilibili_train()


