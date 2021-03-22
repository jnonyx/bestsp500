import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf
import chart_studio
username = 'jnonyx'
api_key = 'VOp5YDDGckKiTc985CRP'
chart_studio.tools.set_credentials_file(username = username, api_key=api_key)
# Web scraping of S&P 500 data
#

def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df

df = load_data()
sector = df.groupby('GICS Sector')

#start_date = input("Enter Start Date in the yyyy-mm-dd format: ")
start_date = '2019-03-13'
print("Start Date is " + start_date)

end_date = '2019-08-13'
#end_date = input("Enter End Date in the yyyy-mm-dd format: ")
print("End Date is " + end_date)


stocks = df.Symbol.tolist()
data = yf.download(stocks, start = start_date, end= end_date)

# Keep only
closed_data = data['Close']
# Transpose from long to wide
close_data = closed_data.transpose()
# For now, just remove the latest day
close_data = close_data.iloc[:, :-1]
# Calc Growth from first to last day
close_data["Growth"] = close_data.iloc[:,-1]/close_data.iloc[:,1]-1
# Sort by Growth
close_data.sort_values(by='Growth', inplace = True, ascending=False)
close_data
# Figure out why there are NaNs
# Try graphing top 5
top5 = close_data.iloc[:5,:-1]
top5t = top5.transpose()
top5t
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
title = 'Top 5 Growth Stocks'
labels = top5t.columns.tolist()
x_data = top5t.index.tolist()
y_data = np.array([top5t.iloc[:,0], top5t.iloc[:,1], top5t.iloc[:,2], top5t.iloc[:,3], top5t.iloc[:,4]])
ranks = ['1) ','2) ','3) ','4) ','5) ']
fig = go.Figure()

for i in range(0, 5):
    fig.add_trace(go.Scatter(x=x_data, y=y_data[i], mode='lines', name=labels[i]
    ))


annotations = []

# Adding labels
for y_trace, label, rank in zip(y_data, labels,ranks):
    # labeling the left_side of the plot
    annotations.append(dict(xref='paper', x=0.1, y=y_trace[0],
                                  xanchor='right', yanchor='middle',
                                  text= ' ${}'.format(round(y_trace[0]),2),
                                  font=dict(family='Arial',
                                            size=16),
                                  showarrow=False))
    # labeling the right_side of the plot
    annotations.append(dict(xref='paper', x=0.9, y=y_trace[-1],
                                  xanchor='left', yanchor='middle',
                                  text=rank + label + ' ${}'.format(round(y_trace[-1]),2),
                                  font=dict(family='Arial',
                                            size=16),
                                  showarrow=False))
# Title
annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                              xanchor='center', yanchor='bottom',
                              text='Best Growth S&P 500 Stocks',
                              font=dict(family='Arial',
                                        size=30,
                                        color='rgb(37,37,37)'),
                              showarrow=False))

fig.update_layout(annotations=annotations)

fig.show()

#fig = go.Figure()
#fig = make_subplots(rows=5, cols=1)
#fig.add_trace(go.Scatter(x=x_data, y=y_data[0], mode='lines', name=labels[0]), row=1, col=1)
#fig.add_trace(go.Scatter(x=x_data, y=y_data[1], mode='lines', name=labels[1]), row=2, col=1)
#fig.add_trace(go.Scatter(x=x_data, y=y_data[2], mode='lines', name=labels[2]), row=3, col=1)
#fig.add_trace(go.Scatter(x=x_data, y=y_data[3], mode='lines', name=labels[3]), row=4, col=1)
#fig.add_trace(go.Scatter(x=x_data, y=y_data[4], mode='lines', name=labels[4]), row=5, col=1)

#fig.update_layout(height=1600, width=700)
#fig.show()

test = fig

