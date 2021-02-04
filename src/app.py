# authors: Yuanzhe Marco Ma, Sicheng Sun, Guanshu Tao, Yuan Xiong
# date: 2021-01-23
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output
from data_manager import DataManager
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go

# retrieve data
data = DataManager().get_data()

# land-on page graphics
table = DataManager().make_table(data)
chart_natn, chart_club = DataManager().plot_altair(data)
ranking_histo = DataManager().plot_histo(data)


# prepare data for map
def prepare_map():
    df_country = data.groupby(['Nationality']).sum().reset_index()
    code_df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')
    df_country_code = df_country.merge(code_df, left_on='Nationality', right_on='COUNTRY', how='left')

    return(df_country_code)


# app layout
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = 'Fifa Star Board'
app.layout = dbc.Container([
    html.H1('FIFA STAR BOARD', style={'width': '100', 'height': '20', 'textAlign': 'center'}),
    html.Br(),
    
    dbc.Row([
        dbc.Col([
            
            html.H4(['Select Attributes:']), 
            dcc.Dropdown(
                id='attribute-widget',
                value=['Name', 'Nationality', 'Age', 'Value(€)', 'Overall'],
                options=[{'label': col, 'value': col} for col in data.columns],
                multi=True
            ),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.Div(['Rank By:']),
                    dcc.Dropdown(
                        id='rankby-widget',
                        value='Overall',
                        options=[{'label': col, 'value': col} for col in data.columns]
                    ),
                ]),
                dbc.Col([
                    html.Div(['Order:']),
                    dcc.Dropdown(
                        id='order-widget',
                        value='True',
                        options=[{'label': 'Descending', 'value': 'False'},
                                 {'label': 'Ascending', 'value': 'True'}]
                    ),
                ]),
                dbc.Col([
                    html.Div(['Continent:']),
                    dcc.Dropdown(
                        id='filter-cont-widget',
                        value='',
                        options=[{'label': val, 'value': val} for val in data['Continent'].unique()]
                    ),
                ]),
                dbc.Col([
                    html.Div(['Club:']),
                    dcc.Dropdown(
                        id='filter-club-widget',
                        value='',
                        options=[{'label': val, 'value': val} for val in data['Club'].dropna().unique()]
                    ),
                ])
            ]),
            html.Br(),
            dbc.Tabs([
                dbc.Tab([
                    html.Br(),
                    dbc.Row([
                        dcc.Slider(id='slider_update', vertical=True, verticalHeight=400, 
                                   tooltip=dict(always_visible=True, placement='left'), min=1, max=986,
                                   step=1, value=1),
                        html.Br(),
                        html.Div([dash_table.DataTable(
                            id='table',
                            columns=[{"name": i, "id": i} for i in table.columns],
                            data=table.to_dict('records'),
                            style_cell={'width': 120}
                        )])
                    ])
                ], label='Table', style={'height': '70vh', 'width': '100vh'}),
                dbc.Tab(
                    dcc.Graph(id="map-graph"),
                    label='Map'
                )
            ]),
            
            html.Iframe(
                id='rank-histogram',
                style={'border-width': '0', 'width': '100%', 'height': '500px'},
                srcDoc=ranking_histo.to_html()
            )
        ]),
        dbc.Col([
            html.Div(
                id='placebolder-right',
                style={'height': '10vh'}
            ),
            dbc.Tabs([
                dbc.Tab(
                    html.Iframe(
                        id='natn-chart',
                        srcDoc=chart_natn.to_html(),
                        style={'border-width': '0', 'width': '150%', 'height': '700px'}
                    ),
                    label='By Nationality'
                ),
                dbc.Tab(
                    html.Iframe(
                        id='club-chart',
                        srcDoc=chart_club.to_html(),
                        style={'border-width': '0', 'width': '150%', 'height': '700px'}
                    ),
                    label='By Club'
                )
            ])
        ], md=3)
    ])
])


# updates table from all 5 dropdowns
@app.callback(
    Output('table', 'data'),
    Output('table', 'columns'),
    Input('rankby-widget', 'value'),
    Input('order-widget', 'value'),
    Input('attribute-widget', 'value'),
    Input('filter-cont-widget', 'value'),
    Input('filter-club-widget', 'value'), 
    Input('slider_update', 'value'))
def update_table(by, order, cols, filter_cont, filter_club, slider_update):
    table = DataManager().update_table(data, by, order == 'True',
                                       cols, filter_cont, filter_club, slider_update)
    columns = [{"name": i, "id": i} for i in table.columns]

    return table.to_dict('records'), columns


# updates charts with Rank-by selection
# updates only when selected col is numeric
@app.callback(
    Output('natn-chart', 'srcDoc'),
    Output('club-chart', 'srcDoc'),
    Output('rank-histogram', 'srcDoc'),
    Input('rankby-widget', 'value'))
def update_charts(by):
    global chart_natn, chart_club
    global ranking_histo
    if not (np.issubdtype(data[by], int) or
            np.issubdtype(data[by], float)):
        return chart_natn, chart_club, ranking_histo
    else:
        chart_natn, chart_club = DataManager().plot_altair(data, by=by)
        ranking_histo = DataManager().plot_histo(data, by=by)
        return (chart_natn.to_html(), chart_club.to_html(), 
                ranking_histo.to_html())



@app.callback(
    dash.dependencies.Output("map-graph", "figure"),
    [dash.dependencies.Input("rankby-widget", "value")]
)
def update_figure(selected):
    #dff = prepare_confirmed_data()

    dff = prepare_map()
    dff['hover_text'] = dff["Nationality"] + ": " + dff[selected].apply(str)
    trace = go.Choropleth(locations=dff['CODE'],z=np.log(dff[selected]),
                          text=dff['hover_text'],
                          hoverinfo="text",
                          marker_line_color='white',
                          autocolorscale=False,
                          reversescale=True,
                          colorscale="RdBu",marker={'line': {'color': 'rgb(180,180,180)','width': 0.5}},
                          colorbar={"thickness": 10,"len": 0.3,"x": 0.9,"y": 0.7,
                                    'title': {"text": 'sum of attribute', "side": "bottom"},
                                    'tickvals': [ 2, 10],
                                    'ticktext': ['100', '100,000']}) 
    return {"data": [trace],
            "layout": go.Layout(height=600, width = 800, margin=dict(l=0, r=0, t=0, b=0), geo={'showframe': False,'showcoastlines': False,
                                                                      'projection': {'type': "natural earth"}})}

if __name__ == '__main__':
    app.run_server(debug=True)
