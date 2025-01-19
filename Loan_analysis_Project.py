# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 21:14:44 2024

@author: richi
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

customer_data = pd.read_csv('customer_data.csv',sep=';')
loan_data = pd.read_excel('loandataset.xlsx')

#merge data
merged_data = pd.merge(loan_data,customer_data,left_on='customerid',right_on='id')

#check for null data
merged_data.isnull().sum()
#drop null values
merged_data = merged_data.dropna()
#check for duplicated data
merged_data.duplicated().sum()

#create a function to categorize purpose in a new column purpose category
def categorize_purpose(purpose):
    if purpose in ['credit_card','debt_consolidation']:
        return 'Financial'
    elif purpose in ['educational','small_business']:
        return 'Educational/Business'
    else:
        return 'Other'
    
categorize_purpose('credit_card')

merged_data['purpose_category'] = merged_data['purpose'].apply(categorize_purpose)

#create function to check if theres is high or low risk in new column Risk
def assess_risk(row):
    if row['dti'] > 20 and row['revol.util'] > 60 and row['delinq.2yrs'] > 2 :
        return 'High Risk'
    else :
        return 'Low Risk'
    
merged_data['Risk'] = merged_data.apply(assess_risk,axis =1)

#create funtion to categorize fico scores of individuals
def categorize_fico(row):
    if row['fico'] >= 800 and row['fico'] <=850:
        return 'Excellent'
    elif row['fico'] >= 740 and row['fico'] <=799:
        return 'Very Good'
    elif row['fico'] >= 670 and row['fico'] <=739:
        return 'Good'
    elif row['fico'] >= 580 and row['fico'] <=669:
        return 'Fair'
    elif row['fico'] >= 300 and row['fico'] <=579:
        return 'Poor'
    else : 
        return 'Not eligible'

merged_data['Categorize_fico'] = merged_data.apply(categorize_fico,axis =1)

#identify high inq and public records
def identify_high_inq_derog(row):
    average_inq = merged_data['inq.last.6mths'].mean()
    average_derog = merged_data['pub.rec'].mean()
    
    if row['inq.last.6mths'] > average_inq and row['pub.rec'] > average_derog:
        return True
    else:
        return False

merged_data['High_Inquiries_Public_Records'] = merged_data.apply(identify_high_inq_derog,axis=1)

#classes example
class Person:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def greet(self):
        return f"Hello I am {self.name} and my age is {self.age}"
    def adult(self):
        if self.age > 18:
            return "I'm an adult"
        else:
            return "I'm not an adult"
        
#create an instance
person1 = Person("Richitha",20)
person1.greet()

class DataAnalysis:
    def __init__(self,df,column_name):
        self.df = df
        self.column_name = column_name
    def calc_mean(self):
        return self.df[self.column_name].mean()
    def calc_median(self):
        return self.df[self.column_name].median()
        
data_analysis = DataAnalysis(merged_data, 'fico')
mean_fico = data_analysis.calc_mean()    

#data visualization
#bar plot to show loans distribution by purpose
plt.figure(figsize = (10,6))
sns.countplot(x='purpose',data=merged_data,palette = 'dark')
plt.title('Loan Distribution by purpose')
plt.xlabel('Purpose')
plt.ylabel('no. of loans')
plt.xticks(rotation = 45)
plt.show()

#create a scatterplot dti vs income
plt.figure(figsize = (10,6))
plt.scatter(x='log.annual.inc',y='dti',data=merged_data)
plt.xlabel('Annual Income')
plt.ylabel('Debt by income')
plt.title('DTI vs INCOME')
plt.show()

#histplot of fico scores
plt.figure(figsize = (10,6))
sns.histplot(merged_data['fico'],bins=30,kde=True)
plt.title('Fico scores')

#box plot to determine risk vs interest rate
plt.figure(figsize = (10,6))
sns.boxplot(x='Risk',y='int.rate',data = merged_data)

#subplot
fig, axs = plt.subplots(nrows = 2,ncols = 2)

sns.countplot(x='purpose',data=merged_data,palette = 'dark',ax=axs[0,0])
axs[0,0].set_title('Loan Distribution by purpose')
plt.setp(axs[0,0].xaxis.get_majorticklabels(),rotation=45)

axs[0,1].scatter(x='log.annual.inc',y='dti',data=merged_data)
axs[0,1].set_title('DTI vs INCOME')

sns.histplot(merged_data['fico'],bins=30,kde=True,ax=axs[1,0])
axs[1,0].set_title('Fico scores')

sns.boxplot(x='Risk',y='int.rate',data = merged_data,ax=axs[1,1])
axs[1,1].set_title('Risk vs Income')

plt.tight_layout()
plt.show()