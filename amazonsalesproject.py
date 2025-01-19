# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 22:02:46 2024
@author: richi
"""
import pandas as pd

sales_data = pd.read_excel("sales_data.xlsx")


# =====================================================================
# Exploring the data 
# =====================================================================

sales_data.columns
sales_data.info()
sales_data.describe()


sales_data.isnull()

sales_data.isnull().sum()

sales_data_dropped = sales_data.dropna()

sales_data_cleaned = sales_data.dropna(subset = ['Amount'])

sales_data_cleaned.isnull().sum()

high_amount_data = sales_data[sales_data['Amount'] > 1000]

filtered_data = sales_data[(sales_data['Category'] == "Top") & (sales_data['Qty'] == 3)]

total_saled_by_category = sales_data.groupby('Category')['Amount'].sum()

avg_sales = sales_data.groupby(['Category','Status'])['Amount'].mean()

total_sales = sales_data.groupby(['Category','Fulfilment'],as_index=False)['Amount'].sum()


total_sales.to_excel('sales total.xlsx',index=False)
