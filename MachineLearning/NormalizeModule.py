'''
liner normalize
'''
import numpy as np

def normalize_median(input_vecs:list, input_exps:list):
    vec_num = len(input_vecs[0])
    vecs_median = np.median(input_vecs)
    exps_median = np.median(input_exps)
    median = vecs_median if vecs_median > exps_median else exps_median
    for vec in input_vecs:
        for i in range(vec_num):
            vec[i] /= median

    for i in range (len(input_exps)):
        input_exps[i] /= median




if __name__ == '__main__':
    test_vecs = [[1,10], [10,3], [12, 9]]
    test_exps = [1, 10]

    normalize_median(test_vecs, test_exps)
    print(test_vecs)
    print(test_exps)