# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 22:02:38 2024

@author: richi
"""

import pandas as pd
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

#load the files
pizza_sales_df = pd.read_excel('pizza_sales.xlsx')
pizza_category_df = pd.read_csv('pizza_category.csv')
pizza_size_df = pd.read_csv('pizza_size.csv')

#a brief statistical summary
pizza_sales_df.describe()
pizza_category_df.describe()
pizza_size_df.describe()

#first and last 10 rows
pizza_sales_df.head(10)
pizza_sales_df.tail(10)

#summary data structure 
pizza_sales_df.info()
#count null values
pizza_sales_df.isnull().sum()

#check duplicated values
pizza_sales_df.duplicated().sum()

#select a column
pizza_sales_df['quantity']

#select row
pizza_sales_df.loc[3]
#select 2 rows with index label 3 and 5
pizza_sales_df.loc[[3,5]]
#select rows between 3 and 5 and specific columns
columns = pizza_sales_df.loc[3:5,['quantity','unit_price']]

#truncate dataframe before index 3
truncated_before = pizza_sales_df.truncate(before = 3)

#basic filtering
filtered_rows = pizza_sales_df[pizza_sales_df['unit_price'] > 20]

#filtering on data
pizza_sales_df['order_date'] = pizza_sales_df['order_date'].dt.date

date_target = datetime.strptime('2015-12-15', '%Y-%m-%d').date()
filtered_rows_by_date = pizza_sales_df[pizza_sales_df['order_date'] > date_target]

#and & condition
bbq_chicken_rows = pizza_sales_df[(pizza_sales_df['unit_price'] > 15) & (pizza_sales_df['pizza_name'] == 'The Barbecue Chicken Pizza')]
#or | condition
bbq_chicken_rows_or = pizza_sales_df[(pizza_sales_df['unit_price'] > 20) | (pizza_sales_df['pizza_name'] == 'The Barbecue Chicken Pizza')]
#specific range
unit_price_range = pizza_sales_df[(pizza_sales_df['unit_price'] > 15) & (pizza_sales_df['unit_price'] <= 20)]

#drop null values
pizza_sales_df_null_dropped = pizza_sales_df.dropna()
pizza_sales_df_null_dropped.isnull().sum()

#replace null with value
date_fill_na = datetime.strptime('2000-01-01', '%Y-%m-%d').date()
fill_na_values = pizza_sales_df.fillna(date_fill_na)

#remove a row
remove_row = pizza_sales_df.drop(2,axis = 0)

#delete 5,7,9 rows
remove_row_5_7_9 = pizza_sales_df.drop([5,7,9],axis = 0)

#delete a column by column name
filtered_unit_price = pizza_sales_df.drop('unit_price',axis=1)

#delete multiple columns
filtered_columns = pizza_sales_df.drop(['unit_price','order_id'],axis=1)

#sorting dataframe
sorted_data = pizza_sales_df.sort_values('total_price')

sorted_data= pizza_sales_df.sort_values('total_price',ascending=False)
sorted_data= pizza_sales_df.sort_values(['pizza_category_id','total_price'],ascending=[False,True])

#group pizza size id and get the count 
grouped_pizza_sales_by_size = pizza_sales_df.groupby(['pizza_size_id']).count()
#group pizza size id and sum the total price 
grouped_pizza_sales_by_size_sum = pizza_sales_df.groupby(['pizza_size_id'])['total_price'].sum()
#group pizza size id and sum the total price and quantity
grouped_pizza_sales_by_size_sum_quantity_total_price = pizza_sales_df.groupby(['pizza_size_id'])[['total_price','quantity']].sum()

goruped_agg = pizza_sales_df.groupby(['pizza_size_id']).agg({'total_price' : 'sum', 'quantity' : 'mean'})

#merge,join,concatenate

merge_df = pd.merge(pizza_sales_df,pizza_size_df,on='pizza_size_id')

merge_df = pd.merge(pizza_category_df,merge_df,on='pizza_category_id')

#concatenate 2 dataframes - vertically appending rows to a df
another_pizza_sales_df = pd.read_excel('another_pizza_sales.xlsx')
concatenated_df = pd.concat([pizza_sales_df,another_pizza_sales_df])

#concatenate horizontally - columns
pizza_sales_voucher_df = pd.read_excel('pizza_Sales_voucher.xlsx')
concatenate_horizontally = pd.concat([pizza_sales_df,pizza_sales_voucher_df],axis=1)

#convert to lower case
pizza_sales_df['pizza_ingredients'] = pizza_sales_df['pizza_ingredients'].str.lower()
#convert to upper case
pizza_sales_df['pizza_ingredients'] = pizza_sales_df['pizza_ingredients'].str.upper()
#convert to title case
pizza_sales_df['pizza_ingredients'] = pizza_sales_df['pizza_ingredients'].str.title()

#replacing text
pizza_sales_df_replaced = pizza_sales_df['pizza_ingredients'].str.replace('Feta Cheese','Mozarella')

#removing white space
pizza_sales_df['pizza_name'] = pizza_sales_df['pizza_name'].str.strip()

#create a box plot
sns.boxplot(x='category',y='total_price',data=merge_df)
plt.xlabel('Pizza Category')
plt.ylabel('Total Sales')