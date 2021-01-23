import dash
import dash_html_components as html
import dash_core_components as dcc
from data_manager import DataManager

# retrieve data
data = DataManager().get_data()
table = data[['Ranking', 'Name', 'Nationality', 'Age', 'Value', 'Overall']]
table = table.sort_values('Overall', ascending=False)[:10]

app = dash.Dash(__name__)

# app layout
app.layout = html.Div([
    html.Center(
        html.H1('FIFA Star Board')
    ),
    html.Iframe(
        srcDoc=table.to_html(index=False),
        style={'border-width': '0', 'width': '50%', 'height': '400px'}
    )
])


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
