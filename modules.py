
import pandas as pd
import numpy as np


def scrub(str1):
	labels = ['date', 'trans#', 'description', 'debit', 'credit', 'cumulative', 'blank1', 'blank2', 'department', 'blank3','product_line']
	scrub = ['Ledger account','AR/AP Account Info','Sample,LLC','Period']
	scrub2 = ['Opening balance', 'Closing']
	trans = pd.read_csv(str1, engine='python',header=None,names=labels,usecols=['date', 'trans#', 'description', 'debit', 'credit', 'department',],skiprows=[0,1,2],skipfooter=3)
	trans['gl'] = np.nan
	trans['gl_desc'] = np.nan
	trans['amount'] = np.nan
	trans.loc[trans['date'] == 'Ledger account', 'gl'] = trans['trans#']
	trans.loc[trans['date'] == 'Ledger account', 'gl_desc'] = trans['description']
	trans.gl.fillna(method='ffill',inplace=True)
	trans.gl_desc.fillna(method='ffill',inplace=True)
	trans.date = trans.date.apply(pd.to_datetime, errors='coerce')
	trans.gl = pd.to_numeric (trans.gl,errors='coerce')
	trans.debit = trans.debit.str.replace(',', '')
	trans.credit = trans.credit.str.replace(',', '')
	trans.debit = trans.debit.apply(pd.to_numeric, errors='coerce')
	trans.credit = trans.credit.apply(pd.to_numeric, errors='coerce')
	trans.amount = trans.debit - trans.credit
	trans.drop(['debit', 'credit'], axis=1, inplace=True)
	trans = trans[~trans['date'].isnull()]  
	trans = trans[~trans['description'].isin(scrub2)] 
	newstring = str1[:-4]
	trans.to_csv(newstring+'_output.csv')
	data = pd.read_csv(newstring+'_output.csv')


def dept_pivot(str1):
	data = pd.read_csv(str1)
	pd.options.display.float_format = '${:,.2f}'.format
	print(data.pivot_table(index='gl_desc', columns='department', values='amount', fill_value=0))


def month_pivot(str1):
	data = pd.read_csv(str1)
	pd.options.display.float_format = '${:,.2f}'.format
	data.date=pd.to_datetime(data.date)
	data.date=data.date.dt.strftime('%Y-%m')
	data_dept = data.groupby(by='department')
	for department, department_df in data_dept:
		print(department)
		print(department_df.pivot_table(index='gl_desc', columns='date', values='amount', fill_value=0))


