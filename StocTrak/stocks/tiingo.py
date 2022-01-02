import requests
import json
from datetime import date, datetime
from dateutil import relativedelta
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

headers={
    'Content-Type':'application/json',
    'Authorization':'Token a9a02a5796f522860ffa8ccd15880da64fe170e2'
}

frequency="monthly"

todays_date = date.today()
five_years_back_date = todays_date - relativedelta(years=5)
three_years_back_date = todays_date - relativedelta(years=3)
one_year_back_date = todays_date - relativedelta(years=1)
nine_months_back_date = todays_date - relativedelta(months=9)
six_months_back_date = todays_date - relativedelta(months=6)
three_months_back_date = todays_date - relativedelta(months=3)
one_month_back_date = todays_date - relativedelta(months=1)
one_week_back_date = todays_date - relativedelta(weeks=1)
three_days_back_date = todays_date - relativedelta(days=3)

def get_meta_data(ticker):
    url = "https://api.tiingo.com/tiingo/daily/{}".format(ticker)
    response=requests.get(url,headers=headers)
    return response.json()

def get_price_data(ticker):
    url = "https://api.tiingo.com/tiingo/daily/{}/prices".format(ticker)
    response = requests.get(url,headers=headers)
    return response.json()[0]

def get_five_years_hist_price_data(ticker):
    url = "https://api.tiingo.com/tiingo/daily/{}/prices?startDate={}&endDate={}&format=json&resampleFreq={}".format(ticker,five_years_back_date,todays_date,frequency)
    response = requests.get(url, headers=headers)
    prices=pd.DataFrame(response.json())
    return response.json()
