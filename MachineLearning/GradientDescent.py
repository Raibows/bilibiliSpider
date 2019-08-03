import numpy as np
from Config import repr_base_class


def read_wine():
    path = 'winequality-white.csv'
    import csv
    vecs = []
    exps = []
    with open(path, 'r') as file:
        reader = csv.reader(file, delimiter=';')
        for line in reader:
            line = [eval(_i) for _i in line]
            vecs.append(line[0:-1])
            exps.append(line[-1])
    # print(vecs, exps)
    return vecs, exps


def normalize(X, y):
    X = np.array(X)
    y = np.array(y)
    y = y.reshape((len(y), 1))
    X_shape = X.shape
    for j in range(0, X_shape[1]):
        _mean = np.mean(X[:, j])
        _max = np.max(X[:, j])
        _min = np.min(X[:, j])
        #         print('hhhh', X[:, j])
        #         print(_mean, _max, _min)
        X[:, j] -= _mean
        X[:, j] /= (_max - _min)
    #         print('jjjj', X[:, j])
    _mean = np.mean(y)
    _max = np.max(y)
    _min = np.min(y)
    y = y.astype('float64')
    y[0, :] -= _mean
    y[0, :] /= (_max - _min)
    X = X.tolist()
    y = y.ravel().tolist()
    return X, y




class gradient_descent(repr_base_class):
    def __init__(self, variables:list, input_vecs:list, input_exps:list,
                 learning_step=0.01, max_iterations=1000, constant=False):
        self.__variables = variables
        self.__variable_num = len(variables)
        self.__vecs = np.array(input_vecs)
        self.__exps = np.array(input_exps).reshape((len(input_exps), 1))
        self.__normalize()
        if constant:
            self.__variable_num += 1
            self.__insert_constant()
        self.__theta = np.array([0 for _ in range(self.__variable_num)])
        self.__theta = self.__theta.reshape((1, self.__variable_num))
        if len(input_vecs) != len(input_exps):
            raise IndexError('input_vecs and input_exps length don\'t match!')
        self.__data_size = len(input_vecs)
        self.__alpha = learning_step
        self.__max_iterations = max_iterations
        self.__latest_cost_record = []


    def __get_cost(self, X:np.array, y:np.array):
        '''
        compute the cost
        :param X:
        :param y:
        :return:
        '''
        inner = np.power((X.dot(self.__theta.T) - y), 2)
        _sum = np.sum(inner) / 2 / len(X)
        return _sum

    def __judge_stop(self, cost):
        self.__latest_cost_record.append(cost)
        if len(self.__latest_cost_record) > 10:
            self.__latest_cost_record.pop(0)
        if self.__latest_cost_record.count(cost) > 4:
            return True
        return False


    def __insert_constant(self):
        ones = np.ones((self.__vecs.shape[0], 1))
        self.__vecs = np.insert(self.__vecs, 0, values=ones.T, axis=1)


    def __batch_gradient_descent(self, X, y):
        temp = np.array(np.zeros((self.__theta.shape)))
        parameters = int(self.__theta.shape[1])
        cost = np.zeros(self.__max_iterations)
        # print(X.shape, self.__theta.shape, y.shape)
        for _i in range(self.__max_iterations):
            error = (X.dot(self.__theta.T)) - y
            # print(parameters)
            for _j in range(parameters):
                # print(error)
                term = error * X[:, _j]
                # print(self.__theta[0, 2])
                # import os
                # os._exit(-1)
                temp[0, _j] = self.__theta[0, _j] - ((self.__alpha / len(X)) * np.sum(term))
            self.__theta = temp
            # print(temp)
            cost[_i] = self.__get_cost(X, y)
            info = f'iteration {_i}, cost_function {cost[_i]} \npredict weights{self.__theta}\n'
            print(info)
            if self.__judge_stop(float(cost[_i])):
                print('NO NEED FOR TRAINING ANYMORE')
                break

    def __normalize(self):
        X = self.__vecs
        y = self.__exps
        X_shape = X.shape
        for j in range(0, X_shape[1]):
            _mean = np.mean(X[:, j])
            _max = np.max(X[:, j])
            _min = np.min(X[:, j])
            #         print('hhhh', X[:, j])
            #         print(_mean, _max, _min)
            X[:, j] -= _mean
            X[:, j] /= (_max - _min)
        #         print('jjjj', X[:, j])
        mean_ = np.mean(y)
        max_ = np.max(y)
        min_ = np.min(y)
        y = y.astype('float64')
        y[0, :] -= mean_
        y[0, :] /= (max_ - min_)
        self.__vecs = X
        self.__exps = y

    def start_train(self):
        # self.__repr__()
        self.__batch_gradient_descent(self.__vecs, self.__exps)

    def get_predict_weight(self):
        return self.__theta.ravel().tolist()





if __name__ == '__main__':
    wine_vecs, wine_exps = read_wine()
    temp = [0 for _ in range(11)]
    # from MachineLearning import fake_data
    # variables = [0.5, 0.8, 2.3, 1.6, 8, 3.47, 5.8]
    # fake = fake_data(variables, data_size=1000, precision=3)
    # data = fake.get_test_data()
    test = gradient_descent(
        temp,
        wine_vecs,
        wine_exps,
        learning_step=0.00001,
        max_iterations=1000,
        constant=True
    )
    test.start_train()

    # weight = test.get_predict_weight()
    #
    # test_vecs = data.get('test_vecs')
    # test_exps = data.get('test_exps')

    # for _i in range(len(test_vecs)):
    #     temp = zip(test_vecs[_i], weight[1:])
    #     predict = sum([item[0] * item[1] for item in temp]) + weight[0]
    #
    #     print(f'true {test_exps[_i]}, predict {predict}')

    # from MachineLearning import perceptron
    # wine_vecs, wine_exps = normalize(wine_vecs, wine_exps)
    # test = perceptron(
    #     variables=temp,
    #     train_vecs=wine_vecs,
    #     train_exps=wine_exps,
    # )
    # test.train(
    #     train_iter_num=1000,
    #     rate=0.001
    # )


