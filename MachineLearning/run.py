import MachineLearning
import csv


def read_data(csv_path):
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


if __name__ == '__main__':

    csv_path = r'../data/bilibili_data.csv'

    data = read_data(csv_path)

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