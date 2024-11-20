from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import numpy as np

app = Dash(__name__)

np.random.seed(42)
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
data = {
    'Month': months,
    'Revenue': np.random.randint(5000, 15000, len(months)),
    'Customers': np.random.randint(100, 500, len(months))
}
df = pd.DataFrame(data)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Business Analytics</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Poppins', sans-serif;
                margin: 0;
                background-color: #f0f2f6;
            }
            .card {
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                padding: 20px;
                margin: 10px;
            }
            .header {
                background-color: #2c3e50;
                color: white;
                padding: 1rem;
                margin-bottom: 2rem;
            }
            .metric-value {
                font-size: 24px;
                font-weight: 600;
                color: #2c3e50;
            }
            .metric-label {
                font-size: 14px;
                color: #7f8c8d;
                margin-top: 5px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div([
   
    html.Div([
        html.H1('Business Analytics Dashboard', 
                style={'margin': 0, 'textAlign': 'center'})
    ], className='header'),
    
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div(f"${df['Revenue'].sum():,.0f}", 
                            className='metric-value'),
                    html.Div('Total Revenue', className='metric-label')
                ], className='card'),
            ], style={'width': '33%', 'display': 'inline-block'}),
            
            html.Div([
                html.Div([
                    html.Div(f"{df['Customers'].sum():,.0f}", 
                            className='metric-value'),
                    html.Div('Total Customers', className='metric-label')
                ], className='card'),
            ], style={'width': '33%', 'display': 'inline-block'}),
            
            html.Div([
                html.Div([
                    html.Div(f"${df['Revenue'].mean():,.0f}", 
                            className='metric-value'),
                    html.Div('Average Monthly Revenue', className='metric-label')
                ], className='card'),
            ], style={'width': '33%', 'display': 'inline-block'}),
        ], style={'display': 'flex', 'justifyContent': 'space-between'}),
        
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Monthly Revenue Trend', 
                           style={'margin': '0 0 20px 0', 'color': '#2c3e50'}),
                    dcc.Graph(id='revenue-chart')
                ], className='card'),
            ], style={'width': '48%', 'display': 'inline-block'}),
            
            html.Div([
                html.Div([
                    html.H3('Customer Growth', 
                           style={'margin': '0 0 20px 0', 'color': '#2c3e50'}),
                    dcc.Graph(id='customer-chart')
                ], className='card'),
            ], style={'width': '48%', 'display': 'inline-block'}),
        ], style={'display': 'flex', 'justifyContent': 'space-between', 
                  'marginTop': '20px'}),
        
    ], style={'padding': '20px', 'maxWidth': '1200px', 'margin': '0 auto'})
])

@callback(
    Output('revenue-chart', 'figure'),
    Input('revenue-chart', 'id')
)
def update_revenue_chart(_):
    fig = px.bar(df, x='Month', y='Revenue',
                 text=df['Revenue'].apply(lambda x: f'${x:,.0f}'))
    
    fig.update_traces(
        marker_color='#3498db',
        textposition='outside'
    )
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f0f2f6'),
        margin=dict(t=0, l=0, r=0, b=0),
        height=300
    )
    
    return fig

@callback(
    Output('customer-chart', 'figure'),
    Input('customer-chart', 'id')
)
def update_customer_chart(_):
    fig = px.line(df, x='Month', y='Customers',
                  markers=True)
    
    fig.update_traces(
        line_color='#2ecc71',
        marker=dict(size=10)
    )
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f0f2f6'),
        margin=dict(t=0, l=0, r=0, b=0),
        height=300
    )
    
    return fig

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)