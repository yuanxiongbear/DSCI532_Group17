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

### charts ###
def make_chart(df, group_col):
    df = (data.groupby(group_col).sum()['Value']
         ).sort_values(ascending=False)[:10].reset_index()

    chart = alt.Chart(df).mark_bar().encode(
            x = alt.X(group_col, sort='-y'),
            y = alt.Y('Value', title='Player Value')
    ).properties(
        width=200,
        height=150
    )
    return chart
    
chart_top = make_chart(data, 'Nationality')
chart_bot = make_chart(data, 'Club')


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# app layout
app.layout = dbc.Container([
    html.H1('FIFA Star Board'), 
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div(['Rank By:']),
            dcc.Dropdown(
                id='sortby-widget',
                value='Overall',
                options=[{'label': col, 'value': col} for col in data.columns]
            ), 
            html.Br(),
            html.Div(['Order:']),
            dcc.Dropdown(
                id='order-widget',
                value='False',
                options=[{'label': 'Descending', 'value': 'False'},
                         {'label': 'Ascending', 'value': 'True'}]
            )
        ], md=3),
        dbc.Col([
            html.H4(['Select Attributes:']),
            dcc.Dropdown(
                id='attribute-widget',
                value=['Name', 'Nationality', 'Age', 'Value', 'Overall'],
                options=[{'label': col, 'value': col} for col in data.columns],
                multi=True
            ),
            html.Iframe(
                id='table',
                srcDoc=table.to_html(index=False),
                style={'border-width': '0', 'width': '100%', 'height': '400px'}
            ),
        ]),
        dbc.Col([
            html.Iframe(
                id='bycountry-chart',
                srcDoc=chart_top.to_html(),
                style={'border-width': '0', 'width': '150%', 'height': '300px'}
            ),
            html.Iframe(
                id='byclub-chart',
                srcDoc=chart_bot.to_html(),
                style={'border-width': '0', 'width': '150%', 'height': '300px'}
            ),
        ], md=3)
    ])
])

@app.callback(
    Output('table', 'srcDoc'),
    Input('sortby-widget', 'value'),
    Input('order-widget', 'value'),
    Input('attribute-widget', 'value'))
def update_table(by, order, cols):
    table = DataManager().update_table(data, by, order=='True', cols)
    return table.to_html(index=False)






if __name__ == '__main__':
    app.run_server(debug=True)
