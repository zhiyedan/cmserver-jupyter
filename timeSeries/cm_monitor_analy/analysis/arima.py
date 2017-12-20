# -*- coding: utf-8 -*-

from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.stattools import adfuller
import statsmodels.tsa.stattools as stools

from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
import pyflux as pf
from sklearn.metrics import mean_squared_error

# 平稳性检测
def test_stationarity(timeseries,autolag='AIC'):
    dftest = adfuller(timeseries, autolag=autolag)
    return dftest[1]

# 白噪声检测
def test_stochastic(ts):
    p_value = acorr_ljungbox(ts, lags=1)[1]
    return p_value

# 寻找最佳差分阶数
def best_diff(df,col='norm',maxdiff=8):
    pvalues = {}
    for i in range(maxdiff+1):
        temp = df.copy()
        if i == 0:
            temp['diff'] = temp[col]
        else:
            temp['diff'] = temp[col].diff(i)
            temp = temp.drop(temp.iloc[:i].index)
        p_value = test_stationarity(temp['diff'])
        pvalues[i] = p_value
    for i in range(maxdiff + 1):
        if pvalues[i] < 0.01:
            break
    return i,pvalues

# 增加diff列
def add_diff_col(df,col,diff_num):
    col_name = 'diff' + str(diff_num)
    if diff_num == 0:
        df[col_name] = df[col].apply(lambda x: float(x))
    else:
        df[col_name] = df[col].apply(lambda x: float(x)).diff(diff_num)
        
    # 备份
    bck_df = df[df[col_name].isnull()==True]
    # 去掉空值
    df.dropna(inplace=True)
    return df,col_name,bck_df

# 还原diff数据
def recovery_diff(ts,diffn,begin_value):
    r_diff = ts.copy()
    if diffn != 0:
        r_diff[0] = r_diff[0] + begin_value
        r_diff = r_diff.cumsum()
    return r_diff


# 寻找最佳p/q值
def best_pq(ts,max_ar=7,max_ma=7):
    order = stools.arma_order_select_ic(ts,max_ar=max_ar,max_ma=max_ma,ic=['aic', 'bic', 'hqic'])
    return order

