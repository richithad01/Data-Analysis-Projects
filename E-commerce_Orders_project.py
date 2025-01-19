# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 20:50:54 2024
   
@author: richi
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Set the current working directory
os.chdir(r"C:\Users\richi\Desktop\spyder\E-commerce Orders Project")

#Check current working directory
print(os.getcwd())

# =============================================================================
# Loading Files
# =============================================================================

# load orders,payments and customers data
orders_data = pd.read_excel(r'C:/Users/richi/Desktop/spyder/E-commerce Orders Project/orders.xlsx')
payments_data = pd.read_excel('order_payment.xlsx')
customers_data = pd.read_excel('customers.xlsx')

# =============================================================================
# Describing the data
# =============================================================================

orders_data.info()
payments_data.info()
customers_data.info()

# =============================================================================
# Handling Missing Values
# =============================================================================

orders_data.isnull().sum()
payments_data.isnull().sum()
customers_data.isnull().sum()

#fill null values with default value
orders_data2 = orders_data.fillna('N/A')
orders_data2.isnull().sum()

#drop rows with missing values in payments data
payments_data = payments_data.dropna()
payments_data.isnull().sum()

# =============================================================================
# Removing Duplicate Data
# =============================================================================

#check for duplicated data
orders_data.duplicated().sum() 

#remove duplicated data
orders_data = orders_data.drop_duplicates()

payments_data.duplicated().sum()
payments_data = payments_data.drop_duplicates()

# =============================================================================
# Filtering the data
# =============================================================================

#select subset of orders data where the order status is invoiced
invoiced_orders_data = orders_data[orders_data['order_status'] == 'invoiced']
invoiced_orders_data = invoiced_orders_data.reset_index(drop = True)

#select subset of orders data where the payment type is credit card and has a payment value greater than 1000
credit_card_payment = payments_data[(payments_data['payment_type'] == 'credit_card') & (payments_data['payment_value'] > 1000)]
credit_card_payment = credit_card_payment.reset_index(drop = True)

#select subset of customers data where the customer state is SP
customer_data_state = customers_data[customers_data['customer_state'] == 'SP']
customer_data_state = customer_data_state.reset_index(drop = True)

# =============================================================================
# Merge and Join differences
# =============================================================================

#merge orders data with payments data on order id column
merged_data = pd.merge(orders_data,payments_data,on = 'order_id')
#join merged data with customers data on customer id column
joined_data = pd.merge(merged_data,customers_data,on = 'customer_id')

# =============================================================================
# Creating Data Visualizations
# =============================================================================

joined_data.info()

#create a field of month_year from order_purchase_timestamp
joined_data['month_year'] = joined_data['order_purchase_timestamp'].dt.to_period('M')
joined_data['week_year'] = joined_data['order_purchase_timestamp'].dt.to_period('W')
joined_data['year'] = joined_data['order_purchase_timestamp'].dt.to_period('Y')


grouped_data = joined_data.groupby('month_year')['payment_value'].sum()
grouped_data = grouped_data.reset_index()
grouped_data.info()

grouped_data['month_year'] = grouped_data['month_year'].astype(str)

#Creating a plot
plt.plot(grouped_data['month_year'],grouped_data['payment_value'],color='red',marker=0)
plt.ticklabel_format(useOffset=False,style ='plain',axis='y')
plt.xlabel('Month and Year')
plt.ylabel('Payment value')
plt.xticks(rotation = 90,fontsize=8)
plt.yticks(fontsize=8)

#Creating scatterplot using matplotlib.pyplot
scatter_df = joined_data.groupby('customer_unique_id').agg({'payment_value':'sum','payment_installments' : 'sum' })

plt.scatter(scatter_df['payment_value'],scatter_df['payment_installments'])
plt.xlabel('Payment Value')
plt.ylabel('Payment Installments')
plt.title('Payment Value vs Payment Installments by Customer')
plt.show()

#using seaborn
sns.set_theme(style='darkgrid')
sns.scatterplot(data = scatter_df,x = 'payment_value' , y = 'payment_installments')

#creating a bar chart

bar_chart_df = joined_data.groupby(['payment_type','month_year'])['payment_value'].sum()
bar_chart_df = bar_chart_df.reset_index()
pivot_data = bar_chart_df.pivot(index='month_year',columns='payment_type',values = 'payment_value')

pivot_data.plot(kind='bar',stacked=True)
plt.xlabel('Month of Payment')
plt.ylabel('Payment Value')
plt.title('Payment per payment type by month')

#creating a box plot

payment_values = joined_data['payment_value']
payment_types = joined_data['payment_type']

#creating a separate box plot per payment type
plt.boxplot([payment_values[payment_types == 'credit_card'],
            payment_values[payment_types == 'boleto'],
            payment_values[payment_types == 'voucher'],
            payment_values[payment_types == 'debit_card']],
            labels = ['credit_Card','Boleto','Voucher','debit_Card'])
plt.xlabel('Payment type')
plt.ylabel('Payment value')
plt.title('Box plot payment value ranges by Payment Type')
plt.show()

#creating subplots(3 in one)

fig,(ax1,ax2,ax3) = plt.subplots(3,1,figsize=(10,10))

#a box plot
ax1.boxplot([payment_values[payment_types == 'credit_card'],
            payment_values[payment_types == 'boleto'],
            payment_values[payment_types == 'voucher'],
            payment_values[payment_types == 'debit_card']],
            labels = ['credit_Card','Boleto','Voucher','debit_Card'])
ax1.set_xlabel('Payment type')
ax1.set_ylabel('Payment value')
ax1.set_title('Box plot payment value ranges by Payment Type')

#a stacked bar chart
pivot_data.plot(kind='bar',stacked=True,ax=ax2)
ax2.set_xlabel('Month of Payment')
ax2.set_ylabel('Payment Value')
ax2.set_title('Payment per payment type by month')

#a scatter plot
ax3.scatter(scatter_df['payment_value'],scatter_df['payment_installments'])
ax3.set_xlabel('Payment Value')
ax3.set_ylabel('Payment Installments')
ax3.set_title('Payment Value vs Payment Installments by Customer')

fig.tight_layout()