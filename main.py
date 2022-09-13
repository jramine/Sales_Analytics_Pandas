import  pandas as pd
import os
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter


path ='./SalesAnalysis/Sales_Data'
new_path = '/Final_Sales.csv'
#concatenating files into Final_Sales.csv
def concactenating_files(path,new_path):
    files = [file for file in os.listdir(path)]
    all_months_data = pd.DataFrame()
    for file in files:
     df = pd.read_csv(path+'/' +file)
    all_months_data = pd.concat([all_months_data,df])

    all_months_data.to_csv(path +new_path)
concactenating_files(path,new_path)


all_data = pd.read_csv("./SalesAnalysis/Output/all_data.csv")


#Cleaning Up The Data
    #Drop Rows Of NAN
def drop_NAN(data):
    datas = data.dropna(how='all')
    return datas
all_data = drop_NAN(all_data)
    #Find 'Or' And Delete It
def delete_Or(data,Column : str,n):
    data= data[data[Column].str[0:n]!='Or']
    return data
all_data=delete_Or(all_data,'Order Date',2)
#all_data = all_data[all_data['Order Date'].str[0:2] !='Or']

    #Convert Columns To The Correct Type
all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered']) #make int
all_data['Price Each'] = pd.to_numeric(all_data['Price Each']) #Make float

#Augment data with additional columns
    #Add Month column

all_data['Month'] = pd.to_numeric(all_data['Order Date'].str[0:2])

    #Add a sales Columns
all_data['Sales']=all_data['Quantity Ordered'] * all_data['Price Each']

    #Add A City Column
def get_City(Address):
    return Address.split(',')[1]
def get_State(Address):
    return Address.split(',')[2].split(' ')[1]
all_data['City']= all_data['Purchase Address'].apply(lambda  x: f"{get_City(x)} ({get_State(x)})")

#what was the best month for sales ?how much was earned that month

def best_month_sales(Month_Column,sales_Column):
    results = all_data.groupby(Month_Column).sum()
    months = range(1,13)
    plt.bar(months,results[sales_Column])
    plt.xlabel('Sales in USA ($)')
    plt.ylabel('Month number')
    plt.show()
best_month_sales('Month','Sales')


#What City Has The Highest Number Of Sales
def city_with_heighest_sales(city_Column,sales_Column):
    results = all_data.groupby(city_Column).sum()
    cities = [city for city,df in all_data.groupby(city_Column)]
    plt.bar(cities,results[sales_Column])
    plt.xticks(cities,rotation='vertical',size=4)
    plt.xlabel('Sales in USA ($)')
    plt.ylabel('City name')
    plt.show()
city_with_heighest_sales('City','Sales')

#What Time Should W e Display Advertisements To Maximize LikeHood Of Customer's Buying product
all_data['Order Date']= pd.to_datetime(all_data['Order Date'])
all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute']= all_data['Order Date'].dt.minute
def Traffic_Buying_Hour(Hour_column):
    hours = [hour for hour , df in all_data.groupby(Hour_column)]
    plt.plot(hours,all_data.groupby([Hour_column]).count())
    plt.xticks(hours)
    plt.grid()
    plt.show()
Traffic_Buying_Hour('Hour')

#What Products Are Most Often Sold Together ?
df = all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped']=df.groupby('Order ID')['Product'].transform(lambda x:','.join(x))
df = df[['Order ID','Grouped']].drop_duplicates()

count = Counter()
for row in df['Grouped']:
    row_list= row.split(',')
    count.update(Counter(combinations(row_list,2)))

"""for key,value in count.most_common(10):
    print(key,value)"""
#What Product Sold The Most ?Why Do You Think It Sold The Most?
product_Group = all_data.groupby('Product')
quantity_Ordered = product_Group.sum()['Quantity Ordered']
products = [product for product,df in product_Group]
plt.bar(products,quantity_Ordered)
plt.xticks(products,rotation='vertical',size =8)
plt.ylabel('Quantity Ordered')
plt.show()

prices = all_data.groupby('Product').mean()['Price Each']
print(prices)



