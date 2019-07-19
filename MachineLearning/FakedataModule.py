import random
import ToolBox
import math


def universal_data_convert(temp:float):
    '''
    randomly change the value of temp
    for generating error data
    :param temp:
    :return:
    '''
    temp *= (random.uniform(1, 2) - 1) ** random.uniform(1, 2)
    temp += random.uniform(-1, 1)
    if temp >= 0:
        temp = temp ** random.uniform(1, 2)
    else:
        temp = (-temp) ** random.uniform(1, 2)
    return temp

class fake_data():
    def __init__(self, variables=None, data_size=1000, error_data_ratio=0, precision=17):
        '''
        :param variables: list, the expected weights of variables
        :param data_size: int, the num of data you want to generate
        :param test_vecs: list, generated variables
        :param test_exps: list, generated expectations for test_vecs
        :param error_data_ratio [0,1], error data ratio of all data
        '''
        if variables == None:
            self.__variables = [0.1, 0.3, 1.2, 2.8, 0.5, 9.1]
        else:
            self.__variables = variables
        self.__data_size = data_size
        self.__test_vecs = []
        self.__test_exps = []
        self.__error_data_size = int(error_data_ratio * self.__data_size)
        self.__error_data = []
        self.__precision = precision

    def __generate_test_data(self):
        for i in range(self.__data_size):
            temp = []
            sum = 0
            for variable in self.__variables:
                x = random.uniform(1, 2) - 1
                temp.append(x)
                sum += variable * x
                if self.__precision != 17:
                    temp = [round(_i, self.__precision) for _i in temp]
                    sum = round(sum, self.__precision)
            if temp in self.__test_vecs:
                i -= 1
            else:
                self.__test_vecs.append(temp)
                self.__test_exps.append(sum)
                # print(i)
        for i in range(self.__error_data_size):
            error_index = random.randint(0, self.__error_data_size)
            if error_index in self.__error_data:
                i -= 1
            else:
                self.__error_data.append(error_index)
                temp = self.__test_exps[error_index]
                temp = universal_data_convert(temp)
                self.__test_exps[error_index] = temp


    def get_test_data(self):
        '''
        :return: dict, (test_vecs, test_exps)
        '''
        self.__generate_test_data()
        return {
            'test_vecs': self.__test_vecs,
            'test_exps': self.__test_exps
        }

    def get_variables(self):
        '''
        :return: __variables, a list filled with expected weights
        '''
        return self.__variables

    def __repr__(self):
        info = f"""
        all_data_size: {self.__data_size}
        data_precision: {self.__precision}
        error_data_size: {self.__error_data_size}
        error_data_ratio: {self.__error_data_size / self.__data_size}
        variables_num: {len(self.__variables)}
        variables_weights: {self.__variables}
        """
        return info


def fakedata_generate(weights:list, num_max:int=10, precision=17):
    '''
    this is a generator function
    :param weights: like [0.1, 0.8, -3.2, 9]
    :param num_max: the num of fake data you want to generate
    :return: a tuple, (vec, exp)
    '''
    num = 0
    vec_num = len(weights)
    while num < num_max:
        vec = [random.uniform(1, 2)-1 for _i in weights]
        exp = sum([weights[_i] * vec[_i] for _i in range(vec_num)])
        if precision != 17:
            vec = [round(item, precision) for item in vec]
            exp = round(exp, precision)
        yield vec, exp
        num += 1


@ToolBox.tool_count_time
def get_test_data_pro(weights:list, num_max:int=1000, error_ratio=0.0, precision=17):
    '''
    this is high performance version for getting test data with numba.jit
    decorator
    :return:
    '''
    vecs = []
    exps = []
    vec_num = len(weights)
    error_data_num = int(error_ratio * num_max)
    for _i in range(num_max):
        temp = []
        exp = 0.0
        for _vec in range(vec_num):
            x = random.uniform(1, 2) - 1
            x = round(x, precision)
            temp.append(x)
        if temp not in vecs:
            # print('hhh')
            if _i < error_data_num:
                for _j, _vec in enumerate(temp):
                    exp += _vec * weights[_j] * random.uniform(0.001, 1000)
                exp = universal_data_convert(exp)
            else:
                for _j, _vec in enumerate(temp):
                    exp += _vec * weights[_j]
            exp = round(exp, precision)
            vecs.append(temp)
            exps.append(exp)
        else:
            _i -= 1

    return vecs, exps




if __name__ == '__main__':
    test_weights = [1.2, 2.1, 3.66, 4.48, -1.05, 0.994, 2.768, 12.66]
    # fake_data_generator = fakedata_generate(test_weights, 10, 3)
    # for item in fake_data_generator:
    #     print(item)
    # fake = fake_data(test_weights)
    # test_data = fake.get_test_data()

    x = get_test_data_pro(test_weights, num_max=10, precision=6, error_ratio=0.1)
    print(x)
