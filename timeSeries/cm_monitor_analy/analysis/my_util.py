# -*- coding: utf-8 -*-

def split_train_test(data,train_percent):
    test_index = int(len(data)*train_percent)
    train = data[:test_index]
    test = data[test_index:]
    return train,test