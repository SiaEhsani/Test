# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc


# Define the navbar structure
def Navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Sequence Diagram", href="/seq_diagram")),
                dbc.NavItem(dbc.NavLink("Topology", href="/topology")),
                # dbc.NavItem(dbc.NavLink("Test", href="/test"))
            ] ,
            brand="Lorem Ipsum",
            brand_href="/seq_diagram",
            color="dark",
            dark=True,
        ), 
    ])

    return layout
