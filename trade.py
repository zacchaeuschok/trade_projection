# from turtle import end_fill
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

class Trade:

    def __init__(self, name, direction, amount, leverage, entry, begin, end):
        #stock attributes 
        self.name = name
        self.direction = direction
        self.amount = amount
        self.leverage = leverage
        self.entry = entry

        #stock data 
        data = {'Name' : self.name, 'Direction' : self.direction, 'Amount' : self.amount, 'Leverage' : self.leverage, 
                'Entry' : self.entry}
        self.table = pd.DataFrame(data = data, index = ["Name"])

        #price range
        self.price_line = np.linspace(begin, end, 101)

        #profit
        self.returns = self.direction * (self.leverage * self.amount * self.price_line / 
                        self.entry - self.leverage * self.amount)

    # def projection(self):
    #     st.title("🐧 Kowalski analaysis")
    #     mask = self.profit() >= 0
    #     self.fig = go.Figure(go.Scatter(x = self.price_line[mask], y = self.returns[mask], mode = 'lines', 
    #                        fill = 'tozeroy', fillcolor = 'rgba(0, 255, 0, 0.1)', name = 'profit'))
    #     self.fig.add_trace(go.Scatter(x = self.price_line[~mask], y = self.returns[~mask], 
    #                         mode = 'lines', fill = 'tozeroy', fillcolor= 'rgba(255, 0, 0, 0.1)', name = 'loss'))
    #     self.fig.update_layout(title='<b>Trade performance</b>', title_x=0.5, 
    #               yaxis_zeroline=False, xaxis_zeroline=False, xaxis = {'title':'price'}, yaxis = {'title':'P/L'})

    #     return self.fig
    
class Portfolio:

    def __init__(self, trade, begin, end):
        self.table = st.dataframe(trade.table)
        self.list = [trade]
        self.profit = trade.returns
        self.price_line = np.linspace(begin, end, 101)

    def addTrade(self, trade):
        self.table.add_rows(trade.table)
        self.profit += trade.returns

    def projection(self):
        mask = self.profit >= 0
        self.fig = go.Figure(go.Scatter(x = self.price_line[mask], y = self.profit[mask], mode = 'lines', 
                         fill = 'tozeroy', fillcolor = 'rgba(0, 255, 0, 0.1)', name = 'profit'))
        self.fig.add_trace(go.Scatter(x = self.price_line[~mask], y = self.profit[~mask], 
                             mode = 'lines', fill = 'tozeroy', fillcolor= 'rgba(255, 0, 0, 0.1)', name = 'loss'))
        self.fig.update_layout(title='<b>Trade performance</b>', title_x=0.5, 
                   yaxis_zeroline=False, xaxis_zeroline=False, xaxis = {'title':'price'}, yaxis = {'title':'P/L'})
        return self.fig
    
        
def newTrade():
    with st.form(key='Form1', clear_on_submit=True):      
        with st.sidebar:
            # inserting variable controllers
            name = st.text_input('Stock Ticker')
            direction = st.selectbox('Direction', ("Short", "Long")) 
            leverage = st.selectbox('Leverage', (1, 2, 5))
            amount = st.number_input("Amount")
            entry_price = st.number_input("Entry price")
            st.form_submit_button(label = 'Submit')
            return Trade(name, -1 if direction == "Short" else 1, amount, leverage, entry_price, begin, end)  


with st.sidebar:
    st.header("Welcome to Marymount Trading")
    st.radio("View", ['New trade', 'Portfolio'])
    price_range = st.slider("Range", 0, 1000, value = (25, 75))
    begin = price_range[0]
    end = price_range[1]

trade = newTrade()
myPortfolio = Portfolio(trade, begin, end)
st.plotly_chart(myPortfolio.projection())





