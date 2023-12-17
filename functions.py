import os
from dotenv import load_dotenv
import requests
import pandas as pd
from Graph import Graph

load_dotenv()

ALPHAVANTAGE_API_ENDPOINT = "https://www.alphavantage.co/query?"
NEWSAPI_ENDPOINT = 'https://newsapi.org/v2/everything?'

def fetch_data(stock):
    '''GET request to alphavantage API to download csv and save it in assets'''
    parameters_daily = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': stock,
    'outputsize': 'compact',
    'apikey': os.getenv('ALPHAVANTAGE_APIKEY'),
    'datatype': 'csv'
}
    response = requests.get(url=ALPHAVANTAGE_API_ENDPOINT, params=parameters_daily)
    if response.status_code == 200:
        daily_data = response.text
        with open(rf'static/assets/csv/{stock}.csv', mode='w') as file:
            file.write(daily_data)

def fetch_news(stock):
    '''GET request to newsAPI to fetch news articles and append them to list ARTICLES as json objects'''
    news_params = {
        'apiKey': os.getenv('NEWSAPI_KEY'),
        'q': stock,
        'sortBy': 'relevancy',
        'language': 'en'
    }
    news_response = requests.get(NEWSAPI_ENDPOINT, params=news_params)
    news = news_response.json()
    if news_response.status_code == 200 and news['totalResults'] != 0:
       return news['articles'][0]

def create_obj(stock):
    '''Reads the csv files and creates Graph object then appends to list GRAPHS'''
    df = pd.read_csv(rf'static/assets/csv/{stock}.csv')
    graph = Graph(df=df, name=stock)
    return graph
