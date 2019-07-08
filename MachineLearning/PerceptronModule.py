import time
import os
import csv

logging_path = 'logging.txt'

def tool_get_current_time():
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return current_time

def tool_log_info(level='info', message='NOTHING'):
    '''
    :param level: info or error
    :param message:
    :return:
    '''
    line = level + '  ' + message + '  ' + tool_get_current_time()
    with open(logging_path, 'a+', encoding='utf-8', newline='') as file:
        file.write(line+'\n')









class video():
    def __init__(self):
        self.y_points = 0
        self.x1_view = 0
        self.x2_danmu = 0
        self.x3_reply = 0
        self.x4_favorite = 0
        self.x5_coin = 0
        self.x6_share = 0
        self.x7_like = 0
        self.rank = 0
        self.avid = 0



class perceptron():
    def __init__(self, variable, activator, test_vecs, test_expectations):
        self.variable_num = len(variable)
        self.variable = variable
        self.activator = activator
        self.weights = [0.0 for _ in variable] #weights init
        self.bias = 0.0 #offset init
        self.test_vecs = test_vecs
        self.test_expectations = test_expectations

    def __repr__(self):
        info = f'weights:{self.weights} \n bias:{self.bias}'
        return info

    def predict(self, input_variable_vector, expectation):
        zipped = zip(input_variable_vector, self.weights) #[(xi, wi)]
        multi_result = [item[0] * item[1] for item in zipped]
        # print('kkk', multi_result[0])
        sum_result = sum(multi_result) #sum xi * wi
        return self.activator(sum_result, expectation)

    def train(self, input_vecs, expectation_vecs, train_iternum, rate):
        for i in range(train_iternum):
            self._one_iteration(input_vecs, expectation_vecs, rate)
            variance = self._get_variance()
            log = f'train {i} \n {self} \n variance {variance}'
            # log = f'train {i} \n {self} \n variance'
            print(log)
            tool_log_info(level='info', message=log)
            if variance < 1e-10:
                print('done !')
                # tool_log_info(level='info', message='done')
                break


    def _one_iteration(self, input_vecs, expectation_vecs, rate):
        zipped = zip(input_vecs, expectation_vecs) #[(input_vec, expectation)]
        #train sample is (x1,x2...., expectation)
        for sample in zipped:
            # print(sample)
            # os._exit(-1)
            output = self.predict(sample[0], sample[1])
            self._update_weights(sample[0], output, sample[1], rate)


    def _update_weights(self, input_vec, output, expectation, rate):
        delta = expectation * (1 - output)
        zipped = zip(input_vec, self.weights)
        new_weights = []
        for item in zipped:
            new_weight = rate * delta * item[0] + item[1]
            if new_weight < 0.0:
                new_weight = -new_weight
            new_weights.append(new_weight)
        self.weights = new_weights
        self.bias += delta * rate

    def _get_variance(self):
        predict_res = []
        for item in self.test_vecs:
            temp = zip(item, self.weights)
            res = [_[0] * _[1] for _ in temp]
            res = sum(res)
            predict_res.append(res)
        zipped = zip(predict_res, self.test_expectations)
        variance = 0.0
        # print(predict_res)
        for item in zipped:
            # print(variance)
            variance += (item[0] - item[1]) ** 2

        return variance / len(predict_res)





def activator(predict_value, expect_value):
    # print(predict_value, expect_value)
    # os._exit(-1)
    x = predict_value / expect_value
    # print(x)
    if x <= 2 and x >= 0.5:
        return 1
    else:
        return x







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
            # print(data)
            # print(line)
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
        'train_data' : train_data,
        'train_exp' : train_exp,
        'test_data' : test_data,
        'test_exp' : test_exp,
    }



csv_path = r'bilibili_data.csv'

data = read_data(csv_path)

data = divide_data(data[0], data[1])

variable = ['danmu', 'reply', 'favorite', 'coin', 'share', 'like']

print(len(data.get('train_data')))

print('hhhhhhhhhhhhh')
print(len(data.get('train_exp')))

print(len(data.get('test_exp')))
# print(input_exp)
# print(input_data)
model = perceptron(
    variable=variable,
    activator=activator,
    test_vecs=data.get('train_data'),
    test_expectations=data.get('train_exp')
)

model.train(
    input_vecs=data.get('train_data'),
    expectation_vecs=data.get('train_exp'),
    train_iternum=10000000000000000,
    rate=0.0000000000000001
)














# input_vecs = [[1, 1, 1], [1, 2, 3], [2, 1, 4], [2, 3, 2], [3, 3, 4], [2, 1, 5], [4, 2, 1]]
# expectations = [0.3 * item[0] + 0.6 * item[1] + 0.7 * item[2] for item in input_vecs] #f(x1, x2) = x1 + 2 * x2
# variable = ['x1', 'x2', 'x3']
# print(expectations)
# test = [[0, 0, 0], [3, 1, 4], [3, 2, 8]]
# exp = [0.3 * item[0] + 0.6 * item[1] + 0.7 * item[2] for item in input_vecs]
#
# test = perceptron(variable, activator, input_vecs, exp)
# test.train(input_vecs, expectations, 30000, 0.01)

# weights = [1.19535, 1.783925]
# bias = 0.934325

# zipped = zip(input_vecs, expectations)
#
# for item, expect in zipped:
#     res = item[0] * weights[0] + item[1] * weights[1]
#     print(f'predict:{res}  expect:{expect}')


# 1179615
# 1539536
# 6700
# 3090
# 151159
# 158637
# 6252
# 153169