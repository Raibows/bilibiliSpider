import os
import ToolBox



def universal_activator(predict, expect):
    '''
    activator for fitting data
    :param predict:
    :param expect:
    :return:
    '''
    if expect == 0:
        base = 1e-10
        if abs(predict) < base:
            return 1
        else:
            ratio = predict / base
    else:
        ratio = predict / expect
    return ratio


class perceptron():
    def __init__(
            self,
            variables,
            train_vecs,
            train_exps,
            activator=None,
            test_vecs=None,
            test_exps=None,
    ):
        '''
        Strongly recommend that you normalize the data, or it might overflow
        if your data is too large
        :param variables:
        :param activator: fitting function/drive function
        :param train_exps: train data of expectations
        :param train_vecs: train data of input xi
        :param test_vecs: test data of input xi
        :param test_exps: test data of expectations
        '''

        self.__variable_num = len(variables)
        self.__variable = variables
        if activator == None:
            self.__activator = universal_activator
        else:
            self.__activator = activator
        self.__weights = [0.0 for _ in variables] #weights init
        self.__bias = 0.0 #offset init
        self.__train_vecs = train_vecs
        self.__train_exps = train_exps
        if test_vecs == None or test_exps == None:
            self.__test_vecs = self.__train_vecs
            self.__test_exps = self.__train_exps
        else:
            self.__test_vecs = test_vecs
            self.__test_exps = test_exps

        self.__variance_result = [] #for recording training result
        self.__latest_variance = None
    def __check(self):
        flag = False
        train_vecs_len = len(self.__train_vecs[0])
        test_vecs_len = len(self.__test_vecs[0])
        if not (self.__variable_num == train_vecs_len == test_vecs_len):
            print('ERROR data length doesn\'t match variables!')
            flag = True
        train_vecs_len = len(self.__train_vecs)
        train_exps_len = len(self.__train_exps)
        test_vecs_len = len(self.__test_vecs)
        test_exps_len = len(self.__test_exps)
        if train_vecs_len != train_exps_len:
            print('ERROR train data length doesn\'t match !')
            flag = True
        if test_vecs_len != test_exps_len:
            print('ERROR test data length doesn\'t match !')
            flag = True
        if flag:
            os._exit(-1)

    def __repr__(self):
        info = f'predict weights: \n{self.__weights} \nbias: {self.__bias}' \
            f'\nvariance: {self.__latest_variance}'
        return info

    def __predict(self, input_vec, input_exp):
        zipped = zip(input_vec, self.__weights) #[(xi, wi)]
        multi_result = [item[0] * item[1] for item in zipped]
        sum_result = sum(multi_result) #sum xi * wi
        return self.__activator(sum_result, input_exp)

    @ToolBox.tool_count_time
    def train(self, train_iter_num=1000, rate=0.01, stop_variance=1e-5):
        '''
        :param train_iter_num: max train iteration num
        :param rate: train rate, the smaller the rate, the more accurate the
        predict weights, and the slower the training
        :param stop_variance: stop variance flag, if training result less than
        stop variance flag, the training will end immediately
        :return:
        '''
        self.__check()
        for i in range(train_iter_num):
            self.__bias = 0
            self.__one_iteration(rate)
            self.__get_variance()
            self.__bias /= len(self.__train_exps)
            log = f'train {i+1} \n{self}'
            print(log)
            self.__variance_result.append(self.__latest_variance)
            if self.__latest_variance < stop_variance:
                print(f'\n\ntrain {i+1} done ! \n{self}')
                print('done')
                return
            if self.__judge_stop_training():
                print("CAN'T FIT THIS DATA \nNO NEED FOR TRAINING ANYMORE")
                return


    def __judge_stop_training(self):
        '''
        judge whether to stop the training
        because sometimes the loss is too large to train
        there is no necessary for training anymore
        :return:
        '''
        if len(self.__variance_result) > 10:
            del self.__variance_result[0]
        latest_variance = self.__variance_result[-1]
        if self.__variance_result.count(latest_variance) > 4:
            return True #need to stop the training
        else:
            return False

    def __one_iteration(self, rate):
        zipped = zip(self.__train_vecs, self.__train_exps) #[(input_vec, expectation)]
        #train sample is (x1,x2...., expectation)
        for sample in zipped:
            output = self.__predict(sample[0], sample[1])
            self.__update_weights(sample[0], sample[1], output, rate)


    def __update_weights(self, input_vec, expectation, output, rate):
        delta = expectation * (1 - output)
        zipped = zip(input_vec, self.__weights)
        new_weights = []
        for item in zipped:
            new_weight = rate * delta * item[0] + item[1] #w_i = w_i-1 + delta_w
            new_weights.append(new_weight)
        self.__weights = new_weights
        self.__bias += delta

    def __get_variance(self):
        predict_res = []
        for item in self.__test_vecs:
            temp = zip(item, self.__weights)
            res = [_[0] * _[1] for _ in temp]
            res = sum(res)
            predict_res.append(res)
        zipped = zip(predict_res, self.__test_exps)
        variance = 0.0
        for item in zipped:
            variance += (item[0] - item[1]) ** 2

        self.__latest_variance = variance / len(predict_res)




















if __name__ == '__main__':

    import MachineLearning

    variables = [0.3, 1, 2.1, 0.66, 0.841, 0.247, 1.6, 7.1]
    example = MachineLearning.fake_data(variables=variables, data_size=1000, error_data_ratio=0.01, precision=17)
    data = example.get_test_data()

    test_vecs = data.get('test_vecs')
    test_exps = data.get('test_exps')

    # NormalizeModule.normalize_min_max(test_vecs, test_exps)
    MachineLearning.normalize_median(test_vecs, test_exps)

    model = perceptron(
        activator=universal_activator,
        variables=example.get_variables(),
        train_vecs=test_vecs,
        train_exps=test_exps,
    )


    model.train(
        train_iter_num=10000,
        rate=1,
        stop_variance=1e-10
    )
    print(example)

'''
DATA100:
10000:   variance     cost     stop
after:   9.5e-8       19.21s   10000
before:  9.3e-8       17.79s   10000

30000:   variance     cost     stop
after:   9.3e-8       53.83s   27142
before:  8.7e-8       48.39s   27298


DATA1000:
10000:   variance     cost     stop
after:   1.0e-7       42.63s   2451
before:  1.2e-7       38.42s   2034

'''