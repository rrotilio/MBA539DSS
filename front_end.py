
import pandas as pd
import numpy as np
import modules as mod


var_str = str(input("Enter filename (including file extension): "))

mod.scrub(var_str)
var_str_no_ext = var_str[:-4]

print("Choose an operation\n1. Expense totals dy department\n2. Expenses by month for each department")
var_int = int(input("Choice: "))

if var_int == 1:
	mod.dept_pivot(var_str_no_ext+'_output.csv')
elif var_int == 2:
	mod.month_pivot(var_str_no_ext+'_output.csv')
else:
	print('Please Choose 1 or 2"')
