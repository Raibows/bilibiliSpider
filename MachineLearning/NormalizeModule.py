'''
normalize the data
'''

def normalize(input_vecs, input_exps):
    vec_num = len(input_vecs[0])
    for i in range(vec_num):
        def func(item):
            return item[i]
        temp_max = max(input_vecs, key=func)
        # print(temp_max[i])
        for vec in input_vecs:
            vec[i] /= temp_max[i]

    exp_max = max(input_exps)
    for i in range(len(input_exps)):
        input_exps[i] /= exp_max




if __name__ == '__main__':
    test_vecs = [[1,10], [10,3]]
    test_exps = [1, 10]

    normalize(test_vecs, test_exps)

    print(test_vecs, test_exps)