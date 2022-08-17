from dash import html, dcc, dash,Input,Output,dash_table,no_update
import dash_bootstrap_components as dbc
from dash import Dash, dash_table
import pathlib
import pandas as pd
from app import app
import plotly.express as px 
import plotly.graph_objects as go
import xarray as xr
import pooch


# df = px.data.gapminder()

# dff = df[df.year == 2007]

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
dff = pd.read_csv(DATA_PATH.joinpath("Topology.csv")) 
columns = ["a", "b", "c", "d"]
# dff["id"] = dff.index

table=dash_table.DataTable(
            id="table",
            columns=[{"name": c, "id": c} for c in columns],
            data=dff.to_dict("records"),
            style_header = {'display': 'none'},
            style_data={ 'border': '10px solid white' },
            style_cell={'textAlign': 'center','backgroundColor': 'rgb(50, 50, 50)', 'color': 'white',},
            # style_table={'height': '100px'}
        )

####LAYOUT####
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.H4("Choose a Cell"),
        table
        ],
            width = 4
        ),
        dbc.Col(
            dcc.Graph(id='graph',figure={}),
            # html.Div(id='tbl_out')
        ), 
        # dbc.Row(
        #     dcc.Graph(id='graph'),
        # )
    ])
])

@app.callback(
    Output('graph', 'figure'),
    Input('table', 'active_cell'))
# def update_graphs(active_cell):
#     if active_cell == {'row': 0, 'column': 0, 'column_id': 'a'} :
#         return str(active_cell) 

# @app.callback(
#   Output('graph', 'children'),
#   Input('table', 'active_cell')
# )
# def noupdate(active_cell):
#     if active_cell is None:
#         return no_update
def update_graphs(active_cell):
    #%%
    ############# 1ST ROW #################
    if active_cell == {'row': 0, 'column': 0, 'column_id': 'a'}:
        data_canada = px.data.gapminder().query("country == 'Canada'")
        fig = px.bar(data_canada, x='year', y='pop')

    if active_cell == {'row': 0, 'column': 1, 'column_id': 'b'}:
        fig = go.Figure(data =
            go.Contour(
                z=[[10, 10.625, 12.5, 15.625, 20],
                [5.625, 6.25, 8.125, 11.25, 15.625],
                [2.5, 3.125, 5., 8.125, 12.5],
                [0.625, 1.25, 3.125, 6.25, 10.625],
                [0, 0.625, 2.5, 5.625, 10]]
            ))
    if active_cell == {'row': 0, 'column': 2, 'column_id': 'c'}:
        airtemps = xr.tutorial.open_dataset('air_temperature').air.sel(lon=250.0)
        fig = px.imshow(airtemps.T, color_continuous_scale='RdBu_r', origin='lower')

    # if active_cell == {'row': 0, 'column': 3, 'column_id': 'd'}:

    # else:
    #     fig = go.Figure() 

    return fig

#     if active_cell == {'row': 0, 'column': 0, 'column_id': 'a'}:
#         data_canada = px.data.gapminder().query("country == 'Canada'")
#         fig = px.bar(data_canada, x='year', y='pop')
#     return fig

#     if active_cell == {'row': 0, 'column': 0, 'column_id': 'a'}:
#         data_canada = px.data.gapminder().query("country == 'Canada'")
#         fig = px.bar(data_canada, x='year', y='pop')
#     return fig

# #%%
#     ############# 2ND ROW #################
#     if active_cell == {'row': 0, 'column': 0, 'column_id': 'a'}:
#         data_canada = px.data.gapminder().query("country == 'Canada'")
#         fig = px.bar(data_canada, x='year', y='pop')
#     return fig

#     if active_cell == {'row': 0, 'column': 0, 'column_id': 'a'}:
#         data_canada = px.data.gapminder().query("country == 'Canada'")
#         fig = px.bar(data_canada, x='year', y='pop')
#     return fig
    
    