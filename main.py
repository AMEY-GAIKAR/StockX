from dotenv import load_dotenv
import os
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from functions import fetch_data, fetch_news, create_obj 
from AddForm import AddForm

load_dotenv()
#Constants & Variables
STOCKS = ['AAPL', 'MSFT', 'HDFCBANK.BSE']    #Inital Stocks to display
GRAPHS = []    #for storing all objects 
ARTICLES = []    #for storing articles
LEN = len(ARTICLES) 

def initialize():
    '''Downloads csv, creates Graph object and fetches news articles for all items in list STOCKS'''
    for stock in STOCKS:
        fetch_data(stock)
        GRAPHS.append(create_obj(stock))
        ARTICLES.append(fetch_news(stock))
        global LEN
        LEN = len(ARTICLES)

def singular_initialize(stock):
    '''Downloads csv, creates Graph object and fetches news articles for the passed argument'''
    fetch_data(stock)
    GRAPHS.append(create_obj(stock))
    ARTICLES.append(fetch_news(stock))

initialize()    

app = Flask(__name__)    #Initiate Flask server
Bootstrap(app)    #Add Bootstrap to server
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/')
def home():
    return render_template('index.html', all_graphs = GRAPHS, all_articles=ARTICLES, len=LEN)

@app.route('/line/<name>')    
def line(name):
    for graph in GRAPHS:
        if graph.name == name:
            graph.line()
            return redirect(url_for('home'))

@app.route('/candle/<name>')    
def candle(name):
    for graph in GRAPHS:
        if graph.name == name:
            graph.candle()
            return redirect(url_for('home'))
        
@app.route('/add', methods=['POST', 'GET'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        singular_initialize(form.stock.data)
        return redirect(url_for('home'))
    return render_template('add.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
