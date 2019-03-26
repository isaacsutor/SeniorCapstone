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

X = deque(maxlen=2000)
Y = deque(maxlen=2000)

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
train_size = int(len(vals) * 0.7)
test_size = len(vals) - train_size
vals = vals[train_size:len(vals)]
vals_display = vals
vals.reverse()
X.append(1)
portfolio_val = 10000
stocks_owned = portfolio_val / vals[len(vals) - 1]
Y.append(vals.pop())
# print(vals[0])
own_stocks = True
app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.H3('S&P 500 Stock Trading'),
        html.Div(html.Button('Click To Start', id='button')),
        html.Button(
            "Buy",
            id="Buy",
            n_clicks=0,
            style={"margin": "0px 7px 7px 10px", "textAlign": "center"},
        ),
        html.Button(
            "Sell",
            id="Sell",
            n_clicks=0,
            style={"margin": "0px 7px 7px 10px", "textAlign": "center"},
        ),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1 * 100
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
        )
    ]
)


@app.callback(Output('live-graph', 'figure'),
              [
                  Input('button', 'n_clicks'),
                  Input('Buy', 'n_clicks'),
                  Input('Sell', 'n_clicks')
              ],
              events=[Event('graph-update', 'interval')],
              )
def update_graph_scatter(btn_click, buy_click, sell_click):
    if btn_click is None:
        btn_click = 0
    if buy_click is None:
        buy_click = 0
    if sell_click is None:
        sell_click = 0
    global stocks_owned
    global portfolio_val
    global own_stocks
    global vals
    # print(vals[len(vals)-1])
    if sell_click is 1:
        if own_stocks is True:
            portfolio_val = stocks_owned * vals[len(vals) - 1]
            stocks_owned = 0
            own_stocks = False
            print("stocks sold")

    if buy_click is 1:
        if own_stocks is False:
            stocks_owned = portfolio_val / vals[len(vals) - 1]
            print("Stocks Bought: ", portfolio_val)
            own_stocks = True

    if own_stocks:
        portfolio_val = stocks_owned * vals[len(vals) - 1]
        print("Value changing:", portfolio_val, " Stocked owned: ", stocks_owned, "At Value:", vals[len(vals) - 1])
    else:
        print("Value Stagnant:", portfolio_val)
        print(stocks_owned)
        # print(0)

    if btn_click != 0:
        # It was triggered by a click on the button 1
        X.append(X[-1] + 1)
        # Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))
        # X.append(dates.pop())
        # Y.append(stock_value.pop())
        Y.append(vals.pop())
        data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            # mode= 'lines+markers'
            mode='lines'
        )
        return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X) + 10]),
                                                    yaxis=dict(range=[min(Y) - 20, max(Y) + 20]), )}


@app.callback(Output('live-update-text', 'children'),
              [Input('Buy', 'n_clicks'),
                Input('Sell', 'n_clicks'),],
              events=[Event('graph-update', 'interval')],)
def update_score():
    style = {'padding': '5px', 'fontSize': '16px'}
    # global stocks_owned
    # global portfolio_val
    return [
        html.Span('Portfolio Value: {0:.2f}'.format(portfolio_val), style=style),
        html.Span('Stocks Owned: {0:.2f}'.format(stocks_owned), style=style),
        html.Span('Starting Value: {0:0.2f}'.format(10000), style=style)
    ]


@app.callback(Output('Buy', 'n_clicks'),
              events=[Event('graph-update', 'interval')], )
def update():
    return 0


@app.callback(Output('Sell', 'n_clicks'),
              events=[Event('graph-update', 'interval')], )
def update():
    return 0




if __name__ == '__main__':
    app.run_server(debug=True)
