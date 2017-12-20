import pandas as pd

def parser(time_data):
    return pd.datetime.strptime('2017-'+time_data,'%Y-%d-%m %H:%M:%S')

def read_wisetone(file_name):
    file_name = '../data/'+file_name
    data = pd.read_csv(file_name,header=0,index_col=0, parse_dates=[0], date_parser=parser)
    data = data.rename(columns={'cpu process':'top_cpu','memory process':'top_mem'})
    data['top_cpu'] = data['top_cpu'].str.partition('/')[0]
    data['top_mem'] = data['top_mem'].str.partition('/')[0]
    return data

def read_aws(file_name):
    file_name = '../data/'+file_name
    return pd.Series.from_csv(file_name,header=0)