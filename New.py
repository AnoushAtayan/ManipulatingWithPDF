# -*- coding: utf-8 -*-

import csv
import re


#open csv file created by tabula

csv_file=open(r'C:\Users\Anoush Atayan\Downloads\tabula-OC_Carlyle Global Market Strategies CLO 2016-4.csv', 'rb')
reader = csv.reader(csv_file)

#extracting all table fields to nested list from csv file

list_of_fields = []

for row in reader:
    if row[0] == '':
        break
    else:
        list_of_fields.append(row)


print list_of_fields

#all fields in the first column

column_1 = [row[i] for row in list_of_fields for i in range(1)]

#create list of tranches' names

list_of_names=[]

for i in list_of_fields[0][1:]:
    if str(i).startswith('Sub'):
        list_of_names.append('SUB')
    else:
        namesRegex = re.search(r'Class +(\w+(-\w+)?)( +Notes)', i)
        list_of_names.append(namesRegex.group(1).replace('-', ''))



print list_of_names

#create list of tranches' currencies

list_of_currencies=(len(list_of_names))*['USD']

print list_of_currencies

#create list of tranches' Fixing to deal currencies

list_of_fxrate = (len(list_of_names))*['1']

print list_of_fxrate

# create list of tranches' types

list_of_types = (len(list_of_names))*['Standard']


# create list of tranches' coupon frequencies

list_of_cfreq = (len(list_of_names))*['Quarterly']

# create list of tranches' deferral statuses

list_of_deferral=[]

index_of_deferral = [i for i, item in enumerate(column_1) if re.search(r'.*Def', item)]


for i in list_of_fields[index_of_deferral[0]][1:]:
    if i == 'No':
        list_of_deferral.append('NO')
    elif i == 'Yes':
        list_of_deferral.append('PIK')
    else:
        list_of_deferral.append('N/A')
print list_of_deferral



# create list of tranches' original amounts

list_of_balances = []

index_of_balances = [i for i, item in enumerate(column_1) if re.search(r'\w*(Amount)|(Principal)\w*', item)]


for i in list_of_fields[index_of_balances[0]][1:]:
    balance = re.search(r'\w*(((\d{3}(.)?)|(\d{2}(.)?)|(\d(.)?))+)\w*', i)

    list_of_balances.append(balance.group())


print list_of_balances


# create list of tranches' Moody's ratings

rating_Moodys = []

index_Moodys = [i for i, item in enumerate(column_1) if re.search(r'\w*Mood', item)]
if len(index_Moodys)==0:
    rating_Fitch = (len(list_of_names)*[''])
else:
    for i in list_of_fields[index_Moodys[0]][1:]:
        if i == 'N/A':
            rating_Moodys.append('')
        else:
            moodys = re.search(r'[^\u0000-\u007F]+(\w+)', i)
            rating_Moodys.append(moodys.group(1))

print rating_Moodys

# create list of tranches' S&P ratings

rating_SP = []

index_SP = [i for i, item in enumerate(column_1) if re.search(r'\w*S&P', item)]

if len(index_SP)==0:
    rating_SP = (len(list_of_names)*[''])
else:
    for i in list_of_fields[index_SP[0]][1:]:
        if i == 'N/A':
            rating_SP.append('')
        else:
            sp = re.search(r'[^\u0000-\u007F]+(\w+)', i)
            rating_SP.append(sp.group(1))

print rating_SP



# create list of tranches' Fitch ratings

rating_Fitch = []

index_Fitch =  [i for i, item in enumerate(column_1) if re.search(r'\w*Fitch', item)]

if len(index_Fitch)==0:
    rating_Fitch = (len(list_of_names)*[''])
else:
    for i in list_of_fields[index_Fitch[0]][1:]:
        if i == 'N/A':
            rating_Fitch.append('')
        else:
            fitch = re.search(r'[^\u0000-\u007F]+(\w+)', i)
            rating_Fitch.append(fitch.group(1))


print rating_Fitch


# create list of tranches' coupon types

list_of_coupon_type = []

index_ctype1 = [i for i, item, in enumerate(column_1) if re.search(r'\w*(Type)', item)]


for i in list_of_fields[index_ctype1[0]][1:]:
    if re.search(r'.*Float', i):
        list_of_coupon_type.append('floating')
    elif re.search(r'.*Fixed', i):
        list_of_coupon_type.append('fixed')
    else:
        list_of_coupon_type.append('variable')
print list_of_coupon_type


# create list of tranches' Spreads and coupons
list_of_spreads = []
list_of_coupons = []

index_spread = [i for i, item, in enumerate(column_1) if re.search(r'\w*(Rate)', item)]
print index_spread
for i in list_of_fields[index_spread[0]][1:]:
    spread = re.search(r'.*LIBOR.*(\d+\.\d+)', i)

    if spread is not None:
        list_of_spreads.append(spread.group(1))
    else:
        list_of_spreads.append('')


for i in list_of_fields[index_spread[0]][1:]:
    coupon = re.search(r'^\d+\.\d+', i)
    if coupon is not None:
        list_of_coupons.append(coupon.group())
    else:
        list_of_coupons.append('')






print list_of_spreads
print list_of_coupons
