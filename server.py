alphavantage_apiendpoint = "https://www.alphavantage.co/query?"
alphavantage_apikey = "KE7MBHHWS14Q5O95"

newsAPI_endpoint = 'https://newsapi.org/v2/everything?'
newsAPI_key = 'e566609b3a074d10891c172ccbcdcd62'

STOCKS = ['GOOGL', 'TSLA']
GRAPHS = [] #for storing all objects 
ARTICLES = []

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo  


class AddForm(FlaskForm):
    stock = StringField(label='name', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class Graph():
    def __init__(self, name, df):
        self.name = name
        self.df = df
        self.process()  #Calculates Current Price, Difference and converts to datetime 
        self.create_color() #sets self.color to green or red depending on DELTA 
    
    def process(self):
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp']) #Converts timestamp to datetime type
        self.DELTA = round((self.df['open'][0] - self.df['open'][1]) / self.df['open'][0] * 100 , 3)    #Calculates difference between today and yesterday 
        self.price = self.df['open'][0] #Current Price

    def create_color(self):
        if self.DELTA >= 0 :
            self.color = 'green'
        else:
            self.color = 'red'
    
    def line(self):
        self.line = px.line(data_frame=self.df, x=self.df['timestamp'], y=self.df['open'], labels={'x':'', 'y':'USD'}, title=f'{self.name}: {self.DELTA}%   Current Price:${self.df["open"][0]}', hover_data=['volume'], template="plotly_dark")
        pyo.plot(self.line, filename=rf'templates\{self.name}line.html')

    def candle(self):
        self.candle = go.Figure(data=[go.Candlestick(x=self.df['timestamp'],open=self.df['open'],high=self.df['high'],low=self.df['low'],close=self.df['close'])])
        pyo.plot(self.candle, filename=rf'templates\{self.name}candle.html')

        
def fetch_data(stock):
    parameters_daily = {
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol': stock,
    'outputsize': 'compact',
    'apikey': alphavantage_apikey,
    'datatype': 'csv'
}
    data_daily = requests.get(url=alphavantage_apiendpoint, params=parameters_daily).text
    with open(rf'static\assets\csv\{stock}.csv', mode='w') as file:
        file.write(data_daily)

def create_obj(stock):
    df = pd.read_csv(rf'static\assets\csv\{stock}.csv')
    graph = Graph(df=df, name=stock)
    GRAPHS.append(graph)

def fetch_news(stock):
    news_params = {
        'apiKey': newsAPI_key,
        'q': stock,
        'sortBy': 'relevancy',
        'language': 'en'
    }
    news = requests.get(newsAPI_endpoint, params=news_params).json()
    ARTICLES.append(news)

def initialize():
    for stock in STOCKS:
        #fetch_data(stock)
        create_obj(stock)
        fetch_news(stock)

def singular_initialize(stock):
    fetch_data(stock)
    create_obj(stock)
    fetch_news(stock)

initialize()

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = '1j123h21ndu1jd19iackoac93328mcwnejd'

@app.route('/')
def home():
    return render_template('index.html', all_graphs = GRAPHS, all_articles=ARTICLES)

@app.route('/line/<name>')    
def line(name):
    for graph in GRAPHS:
        if graph.name == name:
            graph.line()
            return render_template(f'{graph.name}line.html')

@app.route('/candle/<name>')    
def candle(name):
    for graph in GRAPHS:
        if graph.name == name:
            graph.candle()
            return render_template(f'{graph.name}candle.html')
        
@app.route('/add', methods=['POST', 'GET'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        singular_initialize(form.stock.data)
        return redirect(url_for('home'))
    return render_template('add.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
