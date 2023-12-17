import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo

#Class to create Graph object
class Graph():
    def __init__(self, name, df):
        self.name = name
        self.df = df
        self.process()  #Calculates Current Price, Difference and converts to datetime 

    def process(self):
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp']) #Converts timestamp to datetime type
        self.DELTA = round((self.df['open'][0] - self.df['open'][1]) / self.df['open'][0] * 100 , 3)    #Calculates difference between today and yesterday 
        self.price = self.df['open'][0] #Current Price
    
    def line(self):
        '''Create line graph and saves it as a html file in assets folder'''
        self.line = px.line(data_frame=self.df, 
                            x=self.df['timestamp'], 
                            y=self.df['open'], 
                            labels={'x':'', 'y':''}, 
                            title=f'{self.name}: {self.DELTA}%   Current Price: {self.df["open"][0]}', 
                            hover_data=['volume'], 
                            template="plotly_dark")
        pyo.plot(self.line, filename=rf'templates/{self.name}line.html')

    def candle(self):
        '''Create candlestick and saves it as a html file in assets folder'''
        self.candle = go.Figure(data=[go.Candlestick(
            x=self.df['timestamp'],
            open=self.df['open'],
            high=self.df['high'],
            low=self.df['low'],
            close=self.df['close'])])
        pyo.plot(self.candle, filename=rf'templates/{self.name}candle.html')
