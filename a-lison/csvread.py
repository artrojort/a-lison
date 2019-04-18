#Compilador A-LISON 
#Main
#Arturo Rojas Ortiz
#Eduardo Mancilla de la Cruz

import csv
import pandas as pd




colNames = []

data = pd.read_csv('C:/Users/Arturo/Desktop/csvtest.csv', sep=',', header=0)
colNames = data.values[0]
print(colNames)
print(colNames.size)
print(data)
print(data[["Name"]])
lis = data[["Name"]]

#Get max value from column
print(data['Age'].max())

#Drop column
data = data.drop(columns="Age")

#Add column
data['Age'] = [1, 1, 53, 1, 1, 1, 1, 1, 1, 53, 1, 1, 1, 1, 2]
print(data)

#Find in column
print(data.loc[data['Age'] == 53])

data.to_csv (r'C:/Users/Arturo/Desktop/csvtest2.csv', index = None, header=True) #Don't forget to add '.csv' at the end of the path