import dash
from dash.dependencies import Output, Input, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random

import plotly.graph_objs as go
from collections import deque
import pandas
import csv
import flask
import dash
import dash_daq as daq


X = deque(maxlen=500)
Y = deque(maxlen=500)

# colnames = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
# stock_data = pandas.read_csv('SP500.csv', names=colnames)
# global count
# count = 0
# dates = stock_data.Date.tolist()
# stock_value = stock_data.Close.tolist()
vals = []
with open('SP500.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    count = 0
    for row in readCSV:
        if count is 0:
            count += 1
        else:
            vals.append(float(row[4].replace(',', '')))
# train_size = int(len(vals) * 0.85)
filter(None, vals)
train_size = int(len(vals) * 0.92)
test_size = len(vals) - train_size
vals = vals[train_size:len(vals)]
vals_display = vals
vals.reverse()
start = False
X.append(1)
portfolio_val = 10000
stocks_owned = portfolio_val / vals[len(vals) - 1]
Y.append(vals.pop())
# print(vals[0])
own_stocks = True
buttonDisable = False
resDisplay = 'none'
app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.Div([
            html.H1('S&P 500 Stock Trading'),
            html.H3('by Isaac Sutor', id='author-info'),
        ], id="top-bar",),
        html.Div([
            html.Div(
                html.Button('Click To Start', id='button', disabled=buttonDisable),
                id="start-btn",
            ),
            html.Div([
                html.Button(
                    "Buy",
                    id="Buy",
                    disabled=buttonDisable,
                    n_clicks=0,
                    # style={"margin": "0px 7px 7px 10px", "textAlign": "center"},
                ),
                html.Button(
                    "Sell",
                    id="Sell",
                    disabled=buttonDisable,
                    n_clicks=0,
                    # style={"margin": "0px 7px 7px 10px", "textAlign": "center"},
                ),
                html.Button(
                    "Void",
                    id="void",
                    n_clicks=0,
                    style={"display": "none"},
                )
                ],
                id="buy-sell-btn",
            ),
            html.Div(id='live-update-text'),
        ], id="side-bar",),
        html.Div(id='resPage'),

        html.Div([
            html.H1("YOU LOST."),
            ],
            id='results-page-lose',
            style={"display": resDisplay}),

        html.Div([
            html.H1("YOU WON YOU ROCK")
            ],
            id='results-page-win',
            style={"display": resDisplay}
            ),
        html.Div(
        [
            dcc.Graph(id='live-graph', animate=True),
            dcc.Interval(
                id='graph-update',
                # interval=1 * 50
            ),
            html.Div(
                children=[
                    dcc.Location(id="bottom_tab", refresh=False),
                    # dcc.Link("Open positions", id="open_positions", href="/"),
                    # dcc.Link("Closed positions", id="closed_positions", href="/closed"),
                    # html.Div(
                    # dcc.Dropdown(id="closable_orders", placeholder="Close order"),
                    # style={"width": "15%"},
                    # id="close_orders_div",
                    # ),
                    html.Div(
                        children=[html.Table(id="orders_table")],
                        className="row",
                        style={"padding": "3", "textAlign": "center"},
                        id="bottom_content",
                    ),
                ],
                id="bottom_panel",
                className="row",
                style={
                    "overflowY": "auto",
                    "margin": "9px 5px 0px 5px",
                    "padding": "5",
                    "height": "21%",
                    "backgroundColor": "#1a2d46",
                },
            ),
            html.Div([
                html.P("Adjust Play Speed"),
                daq.Slider(
                    id='my-daq-slider',
                    marks={i: '{}'.format(10 ** i) for i in range(2)},
                    max=1,
                    value=1,
                    step=0.01,
                    updatemode="drag",
                    # value=100
                ),
                html.Div()
            ], id='slider-output')
        ], id="graph-panel",),
        ]
)


@app.callback(Output('live-graph', 'figure'),
              [
                  Input('button', 'n_clicks'),
                  Input('Buy', 'n_clicks'),
                  Input('Sell', 'n_clicks'),
              ],
              events=[Event('graph-update', 'interval')],
              )
def update_graph_scatter(btn_click, buy_click, sell_click):
    if btn_click is None:
        btn_click = 0
    if btn_click != 0:
        # It was triggered by a click on the button 1
        X.append(X[-1] + 1)
        global start
        start = True
        # Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))
        # X.append(dates.pop())
        # Y.append(stock_value.pop())
        global vals
        if len(vals) != 0:
            Y.append(vals.pop())
            print(len(vals))
        if len(vals) is 0:
            # endGraph()
            # runResults()
            # endIntervals()
            start = False

        data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            # mode= 'lines+markers'
            mode='lines',
            line={
                'color': '#EF553B',
                'width': 2
            },
        )

        return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X) + 10]),
                                                    yaxis=dict(range=[min(Y) - 20, max(Y) + 20]), )}


@app.callback(Output('live-update-text', 'children'),
              [Input('Buy', 'n_clicks'),
               Input('Sell', 'n_clicks'), ],
              events=[Event('graph-update', 'interval')],)
def update_score(buy_click, sell_click):
    style = {'padding': '5px', 'fontSize': '16px'}
    global start
    if start:
        if buy_click is None:
            buy_click = 0
        if sell_click is None:
            sell_click = 0
        global stocks_owned
        global portfolio_val
        global own_stocks
        global vals_display
        print("vals", len(vals_display))
        # print(vals[len(vals)-1])
        if len(vals_display) != 0:
            if sell_click is 1:
                if own_stocks is True:
                    portfolio_val = stocks_owned * vals_display[len(vals_display) - 1]
                    stocks_owned = 0
                    own_stocks = False
                    print("stocks sold")

            if buy_click is 1:
                if own_stocks is False:
                    stocks_owned = portfolio_val / vals_display[len(vals_display) - 1]
                    print("Stocks Bought: ", portfolio_val)
                    own_stocks = True

            if own_stocks:
                portfolio_val = stocks_owned * vals_display[len(vals_display) - 1]
            vals_display.pop()
            # print("Value changing:", portfolio_val, " Stocked owned: ", stocks_owned, "At Value:", vals_display[len(vals_display) - 1])
        # else:
            # print("Value Stagnant:", portfolio_val)
            # print(stocks_owned)
            # print(0)
        else:
            # endGraph()

            # endIntervals()
            start = False
            # runResults()
    return [
        html.P('Portfolio Value: {0:.2f}'.format(portfolio_val), style=style),
        html.P('Stocks Owned: {0:.2f}'.format(stocks_owned), style=style),
        html.P('Starting Value: {0:0.2f}'.format(10000), style=style)
    ]


# @app.callback(Output('res', 'children'), )
# def runResults():
    # style = {'padding': '5px', 'fontSize': '16px'}
    # return [
        # html.H3('If you had held your stocks the whole way through, your end portfolio value would be: $30485.87'),
        # html.Span('Portfolio Value: {0:.2f}'.format(portfolio_val), style=style),
    # ]


@app.callback(Output('graph-update', 'interval'),
             [Input('my-daq-slider', 'value'), ],)
             # events=[Event('graph-update', 'interval')],)
def update_interval(value):
    # shutdown also needs to be added
    # print(value)
    val = pow(10, 4-value)/2
    if val is not 0:
        return val
    else:
        return 0.1


# @app.callback(Output('graph-update', 'interval'), )
# def endIntervals():
    # return 0


# @app.callback(Output('graph-update', 'interval'),)
@app.callback(Output('resPage', 'children'),
              [Input('Sell', 'n_clicks'), ],
              events=[Event('graph-update', 'interval')],)
def endGraph(n_clicks):
    if n_clicks is 1000000:
        n_clicks = 0
    # global buttonDisable
    # buttonDisable = True
    # global resDisplay
    # resDisplay = 'inline-block'
    # return 0
    # if win
    global vals
    if len(vals) is 0:
        if portfolio_val < 16484.1:
            # style = {'padding': '5px', 'fontSize': '16px'}
            if portfolio_val < 13615.78:
                return [
                    html.H3('Buy-and-Hold is the best strategy - Warren Buffet'),
                    html.P('You should have taken that advise because'),
                    html.H3('YOU LOST'),
                    html.P('If you had held your stocks the whole way through, '
                           'your end portfolio value would be: $16484.10'),
                    html.P('Our Neural Net managed to complete the same time period with 82.6% accuracy.'),
                    html.P('This returns a resulting portfolio of $13615.78'),
                    html.P('Because you traded, you lost to both the market and our Neural Net'),
                    html.P('Your actual end portfolio was: ${0:.2f}'.format(portfolio_val)),
                ]
            else:
                return [
                    html.H3('Buy-and-Hold is the best strategy - Warren Buffet'),
                    html.P('You should have taken that advise because'),
                    html.H3('YOU LOST'),
                    html.P('If you had held your stocks the whole way through, '
                           'your end portfolio value would be: $16484.10'),
                    html.P('Our Neural Net managed to complete the same time period with 82.6% accuracy.'),
                    html.P('This returns a resulting portfolio of $13615.78'),
                    html.P('Because you traded, you lost to the market, '
                           'but beat our Neural Net with an end portfolio of: ${0:.2f}'.format(portfolio_val)),
                ]
        elif portfolio_val > 16484.1:
            if portfolio_val > 13615.78:
                return [
                    # html.H3('Buy-and-Hold is the best strategy - Warren Buffet'),
                    html.P('Color me impressed because'),
                    html.H3('YOU BEAT THE MARKET'),
                    html.P('If you had held your stocks the whole way through, '
                           'your end portfolio value would be: $16484.10'),
                    html.P('Our Neural Net managed to complete the same time period with 82.6% accuracy.'),
                    html.P('This returns a resulting portfolio of $13615.78'),
                    html.P('Because you traded, you beat the market (and our Neural Net)'
                           ' with an end portfolio of: ${0:.2f}'.format(portfolio_val)),
                ]
            else:
                return [
                    # html.H3('Buy-and-Hold is the best strategy - Warren Buffet'),
                    html.P('Color me impressed because'),
                    html.H3('YOU BEAT THE MARKET'),
                    html.P('If you had held your stocks the whole way through, '
                           'your end portfolio value would be: $16484.10'),
                    html.P('Our Neural Net managed to complete the same time period with 82.6% accuracy.'),
                    html.P('This returns a resulting portfolio of $13615.78'),
                    html.P('Because you traded, you beat the market (but not our Neural Net)'
                           ' with an end portfolio of: ${0:.2f}'.format(portfolio_val)),
                ]
    else:
        return []


# @app.callback(Output('button', 'disabled'))
# def buttonsOff():
    # return True


@app.callback(Output('Buy', 'n_clicks'),
              events=[Event('graph-update', 'interval')], )
def update():
    return 0


@app.callback(Output('Sell', 'n_clicks'),
              events=[Event('graph-update', 'interval')], )
def update():
    return 0


# @app.callback(Output('results-page-win'))
# def pageWin():
    # return 0


# @app.callaback(Output('results-page-lose'))
# def pageLose():
    # return 0

if __name__ == '__main__':
    app.run_server(debug=True)
