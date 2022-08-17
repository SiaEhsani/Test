# Import necessary libraries 
from dash import html, dcc
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app

# Connect to your app pages
from pages import  topology, seq_diagram

# Connect the navbar to the index
from components import navbar

# define the navbar
nav = navbar.Navbar()

# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav, 
    html.Div(id='page-content', children=[]), 
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/topology':
        return topology.layout
    if pathname == '/seq_diagram':
        return seq_diagram.layout
    else:
        return seq_diagram.layout


if __name__ == '__main__':
    app.run_server(debug=True)
