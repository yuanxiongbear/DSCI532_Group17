import dash
import dash_html_components as html
import dash_core_components as dcc
from data_manager import DataManager

# retrieve data
data = DataManager().get_data()
table = data[['Ranking', 'Name', 'Nationality', 'Age', 'Value', 'Overall']]
table = table.sort_values('Overall', ascending=False)[:10]

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
                value='True',
                options=[{'label': 'Descending', 'value': 'False'},
                         {'label': 'Ascending', 'value': 'True'}]
            ),
            html.Br(),
            html.Div(['Nationality:']),
            dcc.Dropdown(
                id='filter-natn-widget',
                value='',
                options=[{'label': val, 'value': val} for val in data['Nationality'].unique()]
            ),
            html.Br(),
            html.Div(['Club:']),
            dcc.Dropdown(
                id='filter-club-widget',
                value='',
                options=[{'label': val, 'value': val} for val in data['Club'].dropna().unique()]
            ),
            html.Br(),
            html.Div(['Continent:']),
            dcc.Dropdown(
                id='filter-conti-widget',
                value='',
                options=[{'label': val, 'value': val} for val in data['Continent'].unique()
            
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
    Input('attribute-widget', 'value'),
    Input('filter-natn-widget', 'value'),
    Input('filter-club-widget', 'value'),
    Input('filter-conti-widget', 'value'))
def update_table(v1, v2, v3, v4, v5):
    return None

  
def plot_altair(by = 'Overall', ascending = False , show_n = 10):
    
        
    df_nation = df.groupby('Nationality').agg({by:'mean'}).reset_index()
    df_nation= df_nation.sort_values(by,ascending= ascending)[:show_n]
    nation_chart = alt.Chart(df_nation).mark_bar().encode(alt.X('Nationality', sort='-y'), alt.Y(by))
    
    
    df_nation = df.groupby('Club').agg({by:'mean'}).reset_index()
    df_nation= df_nation.sort_values(by,ascending= ascending)[:show_n]
    club_chart = alt.Chart(df_nation).mark_bar().encode(alt.X('Club', sort='-y'), alt.Y(by))
    return club_chart&nation_chart

if __name__ == '__main__':
    app.run_server(debug=True)
