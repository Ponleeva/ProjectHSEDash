
from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objs as go
import numpy as np

from dash.dependencies import Input, Output, State
import pandas_datareader.data as web # requires v0.6.0 or later
from datetime import datetime
import pandas as pd
#from yahooquery import Ticker
import yfinance as yf
from datetime import timedelta
import dash_auth

#password
USERNAME_PASSWORD_PAIRS=[['username', 'password'], ['K', 'N']]
app = Dash(__name__)
dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)
server = app.server
nsdq = pd.read_csv('NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace=True)
options = []
for tic in nsdq.index:
    mydict={}
    mydict['label']= nsdq.loc[tic]['Name']+ ' '+tic
    mydict['value']= tic
    options.append(mydict)

'''
app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.H3('Enter stock symbol:'),
    dcc.Input(id='my_stock_picker',
                value='TSLA'
              ),
    dcc.Graph(id='my_graph',
              figure={'data':[
                  {'x':[1,2], 'y':[3,1]}
              ], 'layout':{'title':'Default title'}}
              )

])
'''
app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.Div([html.H3('Enter stock symbol:', style={'paddingRight':'30px'}),
        dcc.Dropdown(
            id='my_ticker_symbol',
            options=options,
            value = ['TSLA'],
            multi=True
        )], style={'display':'inline-block', 'verticalAlign':'top','width':'40%'}),
    html.Div([html.H3('Select start and end dates:'),
        dcc.DatePickerRange(
            id='my_date_picker',
            initial_visible_month=datetime.today(),
            min_date_allowed=datetime(2015, 1, 1),
            max_date_allowed=datetime.today(),
            #start date would be 1 day before today
            start_date=datetime.today()-timedelta(days=1),
            end_date=datetime.today()
        )
    ], style={'display':'inline-block'}),
    html.Div([
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit',
            style={'fontSize':24, 'marginLeft':'30px'}
        ),
    ], style={'display':'inline-block'}),
    dcc.Graph(
        id='my_graph',
        figure={
            'data': [
                {'x': [1,2], 'y': [3,1]}
            ], 'layout':{'title':'Default title'}}
    )
])
'''
@app.callback(Output('my_graph','figure'),
              [Input('my_stock_picker','value'),
                Input('my_date_picker','start_date'),
                Input('my_date_picker','end_date')
            ])
'''
@app.callback(
    Output('my_graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('my_ticker_symbol', 'value'),
    State('my_date_picker', 'start_date'),
    State('my_date_picker', 'end_date')
     ])
#def update_graph(stock_ticker):
    #fig = {'data':[{'x':[1,2], 'y':[3,1]}],
          # 'layout':{'title': stock_ticker}
           #}
    #return fig

def update_graph(n_clicks,  stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    traces = []
    for tic in stock_ticker:
        data = yf.download(tic, start, end)
        traces.append({'x': data.index, 'y': data['Close'], 'name': tic})
    fig = {
        'data': traces,
        'layout': {'title': stock_ticker}
    }
    return fig

if __name__=='__main__':
    app.run(debug=True)


