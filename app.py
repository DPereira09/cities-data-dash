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

# Get top 5 and bottom 5 cities
top_5_df = cities_df.head(5)
bottom_5_df = cities_df.tail(5)

# App layout
app.layout = html.Div([
    html.H1("US Cities Population Dashboard (2014)", 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
    
    html.Div([
        html.Label("Select Dataset:", 
                   style={'fontSize': 18, 'fontWeight': 'bold', 'marginRight': 10}),
        dcc.Dropdown(
            id='dataset-dropdown',
            options=[
                {'label': 'Top 5 Most Populous Cities', 'value': 'top'},
                {'label': 'Bottom 5 Least Populous Cities', 'value': 'bottom'}
            ],
            value='top',
            style={'width': '400px'}
        )
    ], style={'marginBottom': 30, 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
    
    html.Div([
        dcc.Graph(id='population-chart')
    ], style={'padding': '20px'})
], style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'})

# Callback to update the chart based on dropdown selection
@app.callback(
    Output('population-chart', 'figure'),
    Input('dataset-dropdown', 'value')
)
def update_chart(selected_dataset):
    if selected_dataset == 'top':
        df = top_5_df
        title = "Top 5 Most Populous US Cities (2014)"
        color = '#3498db'
    else:
        df = bottom_5_df
        title = "Bottom 5 Least Populous US Cities (2014)"
        color = '#e74c3c'
    
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

if __name__ == '__main__':
    app.run_server(debug=True)