
# %%
import pandas as pd
import plotly.express as px
import numpy as np
import pathlib
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output 
import dash_bootstrap_components as dbc
from app import app

#%%
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
df = pd.read_csv(DATA_PATH.joinpath("1-1.csv")) 

# %%
df['direction'] = np.where(df['src_index']<df['dst_index'], '►►►', '◄◄◄')

# %%

df.loc[(df.src == 'l1cache_1'),'src_index']='1.1'
df.loc[(df.src == 'l1cache_2'),'src_index']='1.2'

df.loc[(df.src == 'l2cache_1'),'src_index']='2.1'
df.loc[(df.src == 'l2cache_1'),'src_index']='2.2'

df.loc[(df.src == 'dc1'),'src_index']='3.1'
df.loc[(df.src == 'dc2'),'src_index']='3.2'


# %%
df.loc[(df.dst == 'l1cache_1'),'dst_index']='1.1'
df.loc[(df.dst == 'l1cache_2'),'dst_index']='1.2'

df.loc[(df.dst == 'l2cache_1'),'dst_index']='2.1'
df.loc[(df.dst == 'l2cache_1'),'dst_index']='2.2'

df.loc[(df.dst == 'dc1'),'dst_index']='3.1'
df.loc[(df.dst == 'dc2'),'dst_index']='3.2'

# %%
df[["src_index", "dst_index"]] = df[["src_index", "dst_index"]].apply(pd.to_numeric)

# %%
df['cycle'] = df['cycle'].astype('int')


# %%
df['cycle'] += df.groupby('cycle').cumcount()*50

###Layout###
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Sequence Diagram")
        ], width=12)
    ]),

    html.Br(),

    html.Div([
        dcc.RadioItems(
                id='radioitem',
                options=[{'label': 'Cycle Range', 'value': 'cyc'},
                         {'label': 'Transaction ID', 'value': 'tranid'}],
                value='tranid',
            ),
    ]),
    html.Div([
        dcc.Input(
            id='tranid_input',
            type='number', 
            value=32,
            placeholder="Enter Tran_ID",

            ),
    ],
    style={"display": "grid", "grid-template-columns": "10% 40% 10%"}
    ),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.RangeSlider(
                2000, 692000, 10000,
                marks=None,
                id='cycle_range',
                value=[2000, 22000],
                tooltip={"placement": "top", "always_visible": True})
        ],id='slider')
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='the_graph', 
                figure={},
                style={'align':'center'},
                loading_state={'is_loading':True,'component_name':'fig'},
                config={
                    'scrollZoom':False,
                    'autosizable':True,
                    # 'fillFrame':True,
                    'modeBarButtonsToRemove':['lasso2d','select2d','zoomOut2d','zoomIn2d']
                },
                # animate=True
            )
        ], width=12,align='center'),
    ]),


])

###Callback###

@app.callback(
    # Output('slider','children')
    Output('the_graph','figure'),
    [Input('cycle_range','value'),
    Input('tranid_input','value'),
    Input('radioitem','value')
    ]
)
def update_graph(cycles_chosen, id_chosen, id_or_cyc):
    if id_or_cyc == 'cyc':
        dff=df[(df['cycle']>=cycles_chosen[0])&(df['cycle']<=cycles_chosen[1])]
    elif id_or_cyc == 'tranid':
        dff= df[df['tran_id']== id_chosen]
    fig1 = px.timeline(
        dff,
        x_end='src_index',
        x_start='dst_index',
        color='event',
        y='cycle',
        text='direction',
        opacity=0.7,
        hover_data={
            'cpuID':True,
            'tran_id':True,
            'hit-miss':True,
            'type-op':True,
            'reqAddr':True,
            'cycle':False,
            'src_index':False,
            'dst_index':False,    
        },
        color_discrete_sequence=["SlateGray","Slateblue",'OrangeRed']
    )
    fig2 =px.timeline(
        dff,
        x_start='src_index',
        x_end='dst_index',
        color='event', 
        y='cycle',
        text='direction',
        opacity=0.7,
        hover_data={
            'cpuID':True,
            'tran_id':True,
            'hit-miss':True,
            'type-op':True,
            'reqAddr':True,
            'cycle':False,
            'src_index':False,
            'dst_index':False,
        },
        color_discrete_sequence=["SlateGray","Slateblue",'OrangeRed']
    )
    
    fig1.update_traces(insidetextanchor="start")
    fig2.update_traces(insidetextanchor="end")
    fig = go.Figure(data = fig1.data + fig2.data) 

    fig.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = [
                0, 
                1,1.1,1.2,
                2,2.1,2.2,
                3,3.1,3.2,
                4
            ],
            ticktext = [
                'cpu0:memory',
                'l1cache_0','l1cache_1','l1cache_2', 
                'l2cache_0','l2cache_1','l2cache_2',
                'dc0','dc1','dc2', 
                'memory0'
            ],
            tickangle=90,
            mirror='ticks',
            side='top',gridcolor='grey', 
            griddash='dash',
            zeroline=True,
            zerolinewidth=0.5, 
            zerolinecolor='grey',
            # rangebreaks = {'bounds':[0,4]} 
        ),
        yaxis=dict(
            title_text="cycle",
            dtick=1,
            # ticklen=0.0001,
            showgrid = True,
            automargin = True,
            autorange="reversed",
            type = "category",
            # tickson ='boundaries',
            categoryorder = 'array',
            categoryarray = dff['cycle'].values
        ),
        autosize=False,
        # width=1000,
        height=700,
        template='plotly_white',
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
        barmode='group',
        # bargap=0.01,
        # bargroupgap=1
    )
    return fig
# %%
# if __name__ == '__main__':
#     app.run_server(debug=True)