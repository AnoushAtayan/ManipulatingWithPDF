
import csv
import pandas as pd
import re


reader = pd.read_csv(r'C:\Users\Anoush Atayan\Downloads\tabula-OC_Carlyle Global Market Strategies CLO 2016-4.csv', nrows=14)
list = []
for row in reader:
    list.append(row)

print list
new_list = []

for i in list[1:]:
    if str(i).startswith('Sub'):
        new_list.append('SUB')
    else:
        namesRegex = re.search(r'Class +(\w+(-\w+)?)( +Notes)', i)
        new_list.append(namesRegex.group(1).replace('-', ''))


print new_list


















