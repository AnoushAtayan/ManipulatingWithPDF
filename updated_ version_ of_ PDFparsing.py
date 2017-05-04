# -*- coding: utf-8 -*-

import re
import numpy as np
import pandas as pd
import os

os.chdir('C:\Users\Anoush Atayan\Desktop')


def rename_indices(text):
    namesRegex = re.search(r'Class +(\w+(-\w+)?) +Notes', text)
    if 'Sub'in text:
        return 'SUB'
    elif 'Inc' in text:
        return 'INC'
    elif'Preference' in text:
        return 'PS'
    elif namesRegex:
        return namesRegex.group(1).replace('-', '')
    else:
        print 'Unexpected column name {}'.format(i)
        return 'NA'

def rename_columns(text):
    col_map = {'Def' : 'Interest deferral', 'Amount' or 'Principal' : 'Original amount', 'Mood' : 'Initial ratings (M)', \
            'S&P' : 'Initial ratings (SNP)', 'Fitch':'Initial ratings (F)', 'Type' : 'Coupon type', 'Rate' : 'spread_coupon', \
             'Pari' : 'Ranking' }

    for k, v in col_map.items():
        if k in text:
            return v
    return 'NONE'


def set_rankings(text):
    rankings = []
    initial = True
    for i, j in enumerate(text):
        if initial:
            rankings.append(1)
            initial = False
        elif j == 'None' or text[i-1] == 'None':
            rankings.append(rankings[-1]+1)
        elif text[i-1] != 'None':
            rankings.append(rankings[-1])
    return rankings

def set_deferral(text):
    deferrals = []
    for i, j in enumerate(text):
        if j == 'No':
            deferrals.append('NO')
        elif j == 'Yes':
            deferrals.append('PIK')
        else: deferrals.append('N/A')
    return deferrals



def set_couponType(text):
    couponType = []

    for i, j in enumerate(text):
        if re.search(r'.*Float', j):
            couponType.append('floating')
        elif re.search(r'.*Fixed', j):
            couponType.append('fixed')
        else:
            couponType.append('variable')
    return couponType


def set_spread_coupon(text):

    spread_coupon = []

    for i, j in enumerate(text):
        if str(j)=='nan':
            spread_coupon.append('')
        else:
            parsed_number_list = re.findall(r'[^A-Za-z+ %]+', j)
            if len(parsed_number_list) != 1:
                raise IOError('Cannot parse number {}'.format(j))
            parse_number = parsed_number_list[0]
            spread_coupon.append(parse_number)
    return spread_coupon

def set_missing_rating(text):
    ratings = ['Initial ratings (M)', 'Initial ratings (SNP)', 'Initial ratings (F)']
    for i in ratings:
        if i not in text:
            df[i] = ''


if __name__ == '__main__':

    df = pd.read_csv('input.csv')


    for column in df:
        if "Unnamed" in column:
            df.drop(column, axis=1, inplace=True)

    s = df.ix[:, 0]
    df = df.set_index(s)

    for n, i in enumerate(df.index.tolist()):
        if str(i) == 'nan':
            break

    df = df.iloc[:n, :]

    df = df.T

    df = df.drop(df.index[0])

    df.index = df.index.map(rename_indices)

    df = df.applymap(lambda x: x.replace('\r', ' ').replace('$', '').replace('(sf)', '').replace('sf', '').strip('\xe2\x80\x9c\xe2\x80\x9d') if type(x) == str else x)




    df.columns = df.columns.map(rename_columns)

    df = df[[i for i in df.columns if i != 'NONE']]

    df['Ranking'] = set_rankings(df['Ranking'])

    df['Tranche type'] = 'Standard'

    df['Interest deferral'] = set_deferral(df['Interest deferral'])

    df['Fixing to deal currency'] = '1'

    df['Currency'] = 'USD'

    df['Coupon type'] = set_couponType(df['Coupon type'])

    df['Current Coupon'] = ''

    df['spread_coupon'] = set_spread_coupon(df['spread_coupon'])

    df['Coupon'] = ''
    df['Spread'] = ''

    df['Spread'].mask(df['Coupon type'] == 'floating', df['spread_coupon'], inplace=True)
    df['Coupon'].mask(df['Coupon type'] == 'fixed', df['spread_coupon'], inplace=True)
    set_missing_rating(df.columns)

    df['Name'] = df.index

    df['Coupon frequency'] = 'Quarterly'

    header = ['Ranking', 'Tranche type', 'Interest deferral', 'Fixing to deal currency', 'Name', 'Currency', 'Original amount', 'Initial ratings (M)',\
              'Initial ratings (SNP)', 'Initial ratings (F)', 'Coupon type', 'Spread', 'Coupon', 'Current Coupon', 'Coupon frequency' ]

    df.to_csv('output.csv', columns=header, index=False, na_rep='')






























