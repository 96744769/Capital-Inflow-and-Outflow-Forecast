import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression、
def create_feat_byday(df,feat,days=45):
    feat_df = pd.DataFrame()
    for i in range(1,days+1):
        feat_df['%s_before_%s_day'%(feat,i)] = df[feat].shift(i)
    feat_df.index = df.index
    return feat_df,feat_df.columns.tolist()
def create_label_byday(df,feat,days=30):
    label_df = pd.DataFrame()
    for i in range(1,days+1):
        label_df['%s_label_%s_day'%(feat,i)] = df[feat].shift(-i)
    label_df.index = df.index
    return label_df,label_df.columns.tolist()
data_bt = pd.read_csv("../input/user_balance_table.csv")
target_tpm = "total_purchase_amt"
target_tra = "total_redeem_amt"
agg_tpm_sum = {target_tpm:'sum'}
agg_tra_sum = {target_tra:'sum'}
rd_tpm = data_bt.groupby('report_date').agg(agg_tpm_sum)
rd_tra = data_bt.groupby('report_date').agg(agg_tra_sum)
rd_tpm_feat,rd_tpm_feat_col = create_feat_byday(rd_tpm,'total_purchase_amt')
rd_tpm_label,rd_tpm_label_col = create_label_byday(rd_tpm,'total_purchase_amt')
rd_tra_feat,rd_tra_feat_col = create_feat_byday(rd_tra,'total_redeem_amt')
rd_tra_label,rd_tra_label_col = create_label_byday(rd_tra,'total_redeem_amt')
windows_day = [1,3,5,7,14,21,27,34,45]#构建不同的时间窗口1天，3天，5天，45天 45天往前推一天 求均值 16个特征
winddows_feat = pd.DataFrame()#创建空的时间窗口的特征dataframe
for window in windows_day:
    winddows_feat['tra_%sday_gap_mean'%(window)] = rd_tra_feat.iloc[:,:window].mean(axis=1)
    winddows_feat['tpm_%sday_gap_mean'%(window)] = rd_tpm_feat.iloc[:,:window].mean(axis=1)
tpm_pre = []
tra_pre = []
for col in rd_tra_label_col:#对未来30天的赎回数据一一进行遍历，建模，并进行预测
    train_conditon = (rd_tra_feat['total_redeem_amt_before_45_day'].notnull()) & (rd_tra_label[col].notnull()) & (~rd_tpm_feat.index.isin(["20140831"]))
    test_conditon = rd_tpm_feat.index.isin(["20140831"])
    winddows_feat_train = winddows_feat[train_conditon]
    winddows_feat_test = winddows_feat[test_conditon]
    winddows_feat_label = rd_tra_label[col][train_conditon]
    model_linear = LinearRegression()
    model_linear.fit(winddows_feat_train.values,winddows_feat_label.values)
    test_pre = model_linear.predict(winddows_feat_test)
    tra_pre.append(test_pre[0])
for col in rd_tpm_label_col:
    train_conditon = (rd_tpm_feat['total_purchase_amt_before_45_day'].notnull()) & (rd_tpm_label[col].notnull()) & (~rd_tpm_feat.index.isin(["20140831"]))
    test_conditon = rd_tpm_feat.index.isin(["20140831"])
    winddows_feat_train = winddows_feat[train_conditon]
    winddows_feat_test = winddows_feat[test_conditon]
    winddows_feat_label = rd_tpm_label[col][train_conditon]
    model_linear = LinearRegression()
    model_linear.fit(winddows_feat_train.values,winddows_feat_label.values)
    test_pre = model_linear.predict(winddows_feat_test)
    tpm_pre.append(test_pre[0]) 
sub = pd.DataFrame()#创建时间这一列，20140901至20140930
sub['date'] = pd.date_range(start='20140901',periods=30)
sub['tpm'] = tpm_pre
sub['tra'] = tra_pre
sub['date'] = sub['date'].astype(str)
sub['date'] = sub['date'].map(lambda x:x[:10].replace("-",""))
sub.to_csv("../code/190330/tc_comp_predict_table.csv",index=False,header=False)
'done'
