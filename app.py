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
                {'label': ' Show top 10 cities by population', 'value': 'top10'}
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
    charts = []
    
    if not selected_options:
        return html.Div("Please select at least one option above.", 
                       style={'textAlign': 'center', 'fontSize': 18, 'color': '#7f8c8d'})
    
    # Show top 5 cities
    if 'top5' in selected_options:
        top_5_df = cities_df.head(5)
        fig_top5 = px.bar(
            top_5_df, 
            x='name', 
            y='pop',
            title="Top 5 Most Populous US Cities (2014)",
            labels={'name': 'City', 'pop': 'Population'},
            color_discrete_sequence=['#3498db']
        )
        fig_top5.update_layout(
            xaxis_title="City Name",
            yaxis_title="Population",
            title_x=0.5,
            title_font_size=20,
            showlegend=False,
            hovermode='x'
        )
        fig_top5.update_traces(
            hovertemplate='<b>%{x}</b><br>Population: %{y:,}<extra></extra>'
        )
        charts.append(dcc.Graph(figure=fig_top5, style={'marginBottom': 30}))
    
    # Show bottom 5 cities
    if 'bottom5' in selected_options:
        bottom_5_df = cities_df.tail(5)
        fig_bottom5 = px.bar(
            bottom_5_df, 
            x='name', 
            y='pop',
            title="Bottom 5 Least Populous US Cities (2014)",
            labels={'name': 'City', 'pop': 'Population'},
            color_discrete_sequence=['#e74c3c']
        )
        fig_bottom5.update_layout(
            xaxis_title="City Name",
            yaxis_title="Population",
            title_x=0.5,
            title_font_size=20,
            showlegend=False,
            hovermode='x'
        )
        fig_bottom5.update_traces(
            hovertemplate='<b>%{x}</b><br>Population: %{y:,}<extra></extra>'
        )
        charts.append(dcc.Graph(figure=fig_bottom5, style={'marginBottom': 30}))
    
    # Show top 10 cities
    if 'top10' in selected_options:
        top_10_df = cities_df.head(10)
        fig_top10 = px.bar(
            top_10_df, 
            x='name', 
            y='pop',
            title="Top 10 Most Populous US Cities (2014)",
            labels={'name': 'City', 'pop': 'Population'},
            color_discrete_sequence=['#2ecc71']
        )
        fig_top10.update_layout(
            xaxis_title="City Name",
            yaxis_title="Population",
            title_x=0.5,
            title_font_size=20,
            showlegend=False,
            hovermode='x'
        )
        fig_top10.update_traces(
            hovertemplate='<b>%{x}</b><br>Population: %{y:,}<extra></extra>'
        )
        charts.append(dcc.Graph(figure=fig_top10, style={'marginBottom': 30}))
    
    return charts

if __name__ == '__main__':
    app.run_server(debug=True)