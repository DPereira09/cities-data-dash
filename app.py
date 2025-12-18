import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Initialize the Dash app
app = Dash(__name__)
server = app.server  # Expose the server for deployment

# Load and prepare data
URL = "https://raw.githubusercontent.com/plotly/datasets/refs/heads/master/2014_us_cities.csv"
cities_df = pd.read_csv(URL)
cities_df.sort_values(by='pop', ascending=False, inplace=True)

# Helper function to filter data based on checkbox selection
def filter_by_checkboxes(option):
    """
    Filter cities dataframe based on checkbox option.
    
    Args:
        option (str): The checkbox value ('top5', 'bottom5', 'top10', 'largest10', 'smallest10')
    
    Returns:
        tuple: (filtered_dataframe, chart_type, title, color)
    """
    filters = {
        'top5': {
            'data': cities_df.head(5),
            'type': 'bar',
            'title': 'Top 5 Most Populous US Cities (2014)',
            'color': '#3498db'
        },
        'bottom5': {
            'data': cities_df.tail(5),
            'type': 'bar',
            'title': 'Bottom 5 Least Populous US Cities (2014)',
            'color': '#e74c3c'
        },
        'top10': {
            'data': cities_df.head(10),
            'type': 'bar',
            'title': 'Top 10 Most Populous US Cities (2014)',
            'color': '#2ecc71'
        },
        'largest10': {
            'data': cities_df.head(10),
            'type': 'map',
            'title': 'Largest 10 US Cities by Population (2014) - Geographic View',
            'color': None
        },
        'smallest10': {
            'data': cities_df.tail(10),
            'type': 'map',
            'title': 'Smallest 10 US Cities by Population (2014) - Geographic View',
            'color': None
        }
    }
    
    filter_config = filters.get(option)
    if filter_config:
        return (
            filter_config['data'],
            filter_config['type'],
            filter_config['title'],
            filter_config['color']
        )
    return None, None, None, None

# Helper function to create bar chart
def create_bar_chart(df, title, color):
    """Create a bar chart figure."""
    fig = px.bar(
        df, 
        x='name', 
        y='pop',
        title=title,
        labels={'name': 'City', 'pop': 'Population'},
        color_discrete_sequence=[color]
    )
    fig.update_layout(
        xaxis_title="City Name",
        yaxis_title="Population",
        title_x=0.5,
        title_font_size=20,
        showlegend=False,
        hovermode='x'
    )
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Population: %{y:,}<extra></extra>'
    )
    return fig

# Helper function to create geo map
def create_geo_map(df, title):
    """Create a scatter geo map figure."""
    fig = px.scatter_geo(
        df,
        lat="lat",
        lon="lon",
        size='pop',
        scope='usa',
        color='name',
        hover_name='name',
        hover_data={'pop': ':,', 'lat': False, 'lon': False, 'name': False},
        title=title
    )
    fig.update_layout(
        title_x=0.5,
        title_font_size=20,
        geo=dict(
            bgcolor='rgba(0,0,0,0)',
            lakecolor='#4E91D2',
        ),
        height=600
    )
    return fig

# App layout
app.layout = html.Div([
    html.H1("US Cities Population Dashboard (2014)", 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
    
    html.Div([
        html.Label("Select Display Options:", 
                   style={'fontSize': 18, 'fontWeight': 'bold', 'marginBottom': 10}),
        dcc.Checklist(
            id='display-checklist',
            options=[
                {'label': ' Show top five cities by population', 'value': 'top5'},
                {'label': ' Show bottom five cities by population', 'value': 'bottom5'},
                {'label': ' Show top 10 cities by population', 'value': 'top10'},
                {'label': ' Show largest 10 cities (map)', 'value': 'largest10'},
                {'label': ' Show smallest 10 cities (map)', 'value': 'smallest10'}
            ],
            value=['top5'],  # Default selection
            style={'fontSize': 16},
            labelStyle={'display': 'block', 'marginBottom': 10}
        )
    ], style={
        'marginBottom': 30, 
        'padding': '20px',
        'backgroundColor': '#f8f9fa',
        'borderRadius': '10px',
        'maxWidth': '500px',
        'margin': '0 auto 30px auto'
    }),
    
    html.Div(id='charts-container', style={'padding': '20px'})
    
], style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'})

# Callback to update the charts based on checklist selection
@app.callback(
    Output('charts-container', 'children'),
    Input('display-checklist', 'value')
)
def update_charts(selected_options):
    """Update displayed charts based on checkbox selections."""
    charts = []
    
    if not selected_options:
        return html.Div("Please select at least one option above.", 
                       style={'textAlign': 'center', 'fontSize': 18, 'color': '#7f8c8d'})
    
    # Iterate through selected options and create appropriate charts
    for option in selected_options:
        df, chart_type, title, color = filter_by_checkboxes(option)
        
        if df is not None:
            if chart_type == 'bar':
                fig = create_bar_chart(df, title, color)
            elif chart_type == 'map':
                fig = create_geo_map(df, title)
            else:
                continue
            
            charts.append(dcc.Graph(figure=fig, style={'marginBottom': 30}))
    
    return charts

if __name__ == '__main__':
    app.run_server(debug=True)