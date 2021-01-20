import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from data_manager import DataManager
import altair as alt
import dash_bootstrap_components as dbc

# retrieve data
data = DataManager().get_data()


table = DataManager().make_table(data)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# app layout
app.layout = dbc.Container([
    html.H1('FIFA Star Board'), 
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='sortby-widget',
                value='Overall',
                options=[{'label': col, 'value': col} for col in data.columns]
            ), 
            html.Br(),
            dcc.Dropdown(
                id='order-widget',
                value='True',
                options=[{'label': 'Descending', 'value': 'False'},
                         {'label': 'Ascending', 'value': 'True'}]
            )
        ], md=3),
        dbc.Col([
            html.Iframe(
                id='table',
                srcDoc=table.to_html(index=False),
                style={'border-width': '0', 'width': '100%', 'height': '400px'}
            ),
        ]),
        dbc.Col([
            html.Div(['Right section'],
            style={"border":"2px black solid"})
        ], md=3)
    ])
])

@app.callback(
    Output('table', 'srcDoc'),
    Input('sortby-widget', 'value'),
    Input('order-widget', 'value'))
def update_table(by, order):
    table = DataManager().update_table(data, by, order=='True')
    return table.to_html(index=False)


if __name__ == '__main__':
    app.run_server(debug=True)
