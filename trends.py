"""
Created on Dec 05 2021

@author: Seung Won Joeng
"""


# pip install pytrends
# pip install pandas
from pytrends.request import TrendReq
import pandas as pd
import json
import datetime

def search_trend(user_input):
    """ For this version, English searching trends only """
    kw_list = [user_input]

    pytrends = TrendReq(hl='en-US', tz=360)

    pytrends.build_payload(kw_list, cat=0, timeframe='today 1-m')
    df = pytrends.interest_over_time()
    df = df.drop('isPartial', axis=1)

    return df.to_dict()


def dict_to_list(d, user_input):
    d = d.get(user_input)
    result = []
    for k, v in d.items():
        result.append({k.strftime('%Y-%m-%d'): v})
    return result


def response_trends(user_input):
    d = search_trend(user_input)
    lst = dict_to_list(d, user_input)

    response = json.dumps(lst)

    return response

# d = search_trend("McGill University")
#
# print(d)
# print(type(d))
#
# print(dict_to_list(d, "McGill University"))
