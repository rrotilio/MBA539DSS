
import pandas as pd
import numpy as np

labels = ['date', 'trans#', 'description', 'debit', 'credit', 'cumulative', 'blank1', 'blank2', 'department', 'blank3','product_line']

scrub = ['Ledger account','AR/AP Account Info','Sample,LLC','Period']

scrub2 = ['Opening balance', 'Closing']

trans = pd.read_csv("sample.csv", engine='python',header=None,names=labels,usecols=['date', 'trans#', 'description', 'debit', 'credit', 'department',],skiprows=[0,1,2],skipfooter=3)
#first three rows and last three rows are always the same and can be removed.  Column data is always the same including blanks


trans['gl'] = np.nan
trans['gl_desc'] = np.nan
trans['amount'] = np.nan
trans['debit2'] = np.nan


trans.loc[trans['date'] == 'Ledger account', 'gl'] = trans['trans#']
trans.loc[trans['date'] == 'Ledger account', 'gl_desc'] = trans['description']
trans.gl.fillna(method='ffill',inplace=True)
trans.gl_desc.fillna(method='ffill',inplace=True)
trans.date = pd.to_datetime(trans.date,errors='ignore')
trans.gl = pd.to_numeric (trans.gl,errors='ignore')
trans.debit2 = trans.debit.astype(np.float64,errors='ignore')
trans.credit = pd.to_numeric (trans.credit,errors='ignore')
trans = trans[~trans['date'].isin(scrub)]  #want to drop all non datetimes (or NaT values if I used 'coerce'), but I can't figure out
trans = trans[~trans['description'].isin(scrub2)] #potential for valid data to be dropped? not likely, but Murphy's Law
print(type(trans['debit2'].iloc[0]))
print(trans['debit2'].iloc[0])
print(type(trans['credit'].iloc[7]))
print(trans['credit'].iloc[7])
print(type(trans['date'].iloc[7]))
print(trans['date'].iloc[7])
#trans['amount'] = trans.debit - trans.credit
#print(trans.amount)
trans.to_csv('sample2.csv')