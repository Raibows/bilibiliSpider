'''
liner normalize
'''
import numpy as np

def normalize_min_max(input_vecs:list, input_exps:list):
    vec_num = len(input_vecs[0])
    for i in range(vec_num):
        std = np.std(input_vecs[i], ddof=1) #unbiased variance n-1
        mean = np.mean(input_vecs[i])
        for j in range(len(input_vecs)):
            input_vecs[j][i] = (input_vecs[j][i] - mean) / std

    std = np.std(input_exps, ddof=1)
    mean = np.mean(input_exps)
    for i in range(len(input_exps)):
        input_exps[i] = (input_exps[i] - mean) / std




if __name__ == '__main__':
    test_vecs = [[1,10], [10,3]]
    test_exps = [1, 10]

    normalize_min_max(test_vecs, test_exps)
    print(test_vecs)
    print(test_exps)