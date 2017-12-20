# -*- coding: utf-8 -*-
 
from sklearn import preprocessing

# 添加‘norm’列
def norm_df(df,col):
    scaler = preprocessing.MinMaxScaler()
    df['norm'] = scaler.fit_transform(df[col].values.reshape(-1,1))
    return scaler,df

def norm_ts(ts):
    scaler = preprocessing.MinMaxScaler()
    result_ts = scaler.fit_transform(ts.values.reshape(-1,1))
    return sclaer,result_ts

def recovery_df(df,col,scaler):
    return scaler.inverse_transform(df[col].values.reshape(-1,1))

def recovery_ts(ts,scaler):
    return scaler.inverse_transform(ts.values.reshape(-1,1))

