import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import base64

df = pd.read_csv('Score By AI.csv').drop(columns='Unnamed: 0')

df3 = pd.read_csv('Company Name.csv').drop(columns='Unnamed: 0')
df = df.round(decimals=2)
df = pd.concat([df.set_index('index'),df3.set_index('unique_id')], axis=1, join='inner').reset_index()
df2 = df.set_index("index")

# for i,r in df.iterrows():
#     print(df.loc[i]['index'])


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

image_filename = 'Logo_TH.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
print(encoded_image )

input_list = []
# for x in ['AZ','FL','GA','IA','ME','MI','NC','NV','OH','PA','TX','WI']:
#     input_list.append(
#         Input(component_id=f'radiolist-{x}', component_property='value')
#     )

table_header = [
    html.Thead(html.Tr([html.Th("MainRisk"), html.Th("First Score") , html.Th("second Score")]))
]

dcc.Store(id='session', storage_type='session',data = "primary")
row1 = html.Tr([html.Td(html.Div("General risk" , id='GenB')) , html.Td(html.Div(id='Gen')), html.Td(html.Div(id='Gen2'))])
row2 = html.Tr([html.Td(html.Div("Credit/Asset" , id='AssB')) , html.Td(html.Div(id='Ass')), html.Td(html.Div(id='Ass2'))])
row3 = html.Tr([html.Td(html.Div("Market"       , id='MarB')) , html.Td(html.Div(id='Mar')), html.Td(html.Div(id='Mar2'))])
row4 = html.Tr([html.Td(html.Div("Liquidity"    , id='LiqB')) , html.Td(html.Div(id='Liq')), html.Td(html.Div(id='Liq2'))])
row5 = html.Tr([html.Td(html.Div("License"      , id='LicB')) , html.Td(html.Div(id='Lic')), html.Td(html.Div(id='Lic2'))])


table_body = [html.Tbody([row1, row2, row3, row4, row5])]

x = [] #DropDown All บลจ
for i,r in df3.iterrows():
     x.append({"label": r['abb'], "value": r['unique_id']},)

# Scatter Plot
df['Total'] = df['rank_AUM']+df['ประเภทการขายกอง']+df['risk_spectrum']+df['AI']+df['invest_country_flag']+df['ratioAI']+df['ratioDI']+df['Sector risk']+df['Total Percent']+df['UnderratePercentR']+df['Comlexity return']+df['Derivative']+df['FX_Ex']+df['Asset']+df['Sensitive']+df['Term to maturity']+df['Nature of liabilities']+df['Last Resort ']+df['Funding strategy to support ']+df['ประวัติการทำความผิด']
fig = px.scatter(df, x="Total", y="Total", color="abb", size= "Total")
#fig = px.scatter(df, x="x", y="y", color="fruit", custom_data=["customdata"])
fig.update_layout(title='Risk Graph ', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(17,72,117,255)', font  ={'color': '#ffffff'})

#Table 2
table_header2 = [
    html.Thead(html.Tr([html.Th("Factor"), html.Th("First Score"), html.Th("Second Score")]))
]
table2_l = []
for i in df2:
    table2_l.append(html.Tr(  [html.Td(i) , html.Td(    df2.loc['C0000000021'][i])   ]))
table_body2 = [html.Tbody(table2_l)]



app.layout = html.Div([
    dbc.Row([
        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),style={'margin-left':'100px','height':'70px'}),
        html.Div(
        [
            dbc.Row(dbc.Col(html.H1("RBA Score DashBoard", style={'textAlign':'left','color':'green','margin-left':'45px'}), width=12)),
        ],
        )],style={'padding':'15px','background-color': '#001542'}),




    dbc.Row(
        [

        dbc.Col(dcc.Graph(id='Scatter', figure=fig,
                          config={'displayModeBar':False}
                          , style={
                                    'color': 'white'
                                  }
                          ), width=8),
        ], no_gutters=True,
        style=
        {'width':'95%', 'height':'400px', 'margin':'15px','padding' : '10px' },justify="center",
#,'background-color': '#114875'
    ),

    dbc.Row([
        dbc.Col([
            html.H5("First", style={'textAlign': 'center','color': 'white'}),
            dbc.Select(
                id="select",
                options=x
                , value='C0000000021'
            )]),
        dbc.Col([
            html.H5("Second", style={'textAlign': 'center','color': 'white'}),
            dbc.Select(
                id="select2",
                options=x + [{"label": "none", "value": "none"}, ]
                , value='none'
            )])
    ]),

    dbc.Row(
        [

        dbc.Col([dbc.Row(
                        dbc.Select(id="MainRiskSelector",
                                options=[{"label": 'General', "value": 'G'},
                                        {"label": 'Market', "value": 'M'},
                                        {"label": 'Credit/Asset', "value": 'A'},
                                        {"label": 'Liq' , "value": 'L'},
                                        {"label": 'License' , "value": 'C'},
                                        {"label": 'All' , "value": 'Z'},]
                                        ,value = 'G'),
                        style={'padding':'15px'}),
                dbc.Row(
                        dbc.Table(id = 'BarTable' , children  = table_header2 + table_body2, bordered=True),
                        )], width=5,style={'padding':'15px'}),

        dbc.Col(dbc.Table(table_header + table_body, bordered=True, id='ScoreTable'), width=5,style={'padding': '15px','margin-top':'65px'}),
        ], no_gutters=True
        ,style={'width':'95%', 'margin':'15px','padding' : 'auto','justify-content':'space-evenly'},
    ),
    dbc.Row(
            dbc.Col(dcc.Graph(id='BarPlot', figure={},config={'displayModeBar': False}),)
           )
],style={'background-color': '#002653'})


# must have Dash version 1.16.0 or higher
@app.callback(
    Output("Gen","children"),
    Output("Ass","children"),
    Output("Mar","children"),
    Output("Liq","children"),
    Output("Lic","children"),
    Output("Gen2","children"),
    Output("Ass2","children"),
    Output("Mar2","children"),
    Output("Liq2","children"),
    Output("Lic2","children"),
    [Input(component_id="select",  component_property="value"),Input(component_id="select2",  component_property="value")]
)
def SeachMainRisk(n,m):
    print(n)
    token_a = df2.loc[n]['rank_AUM']+df2.loc[n]['ประเภทการขายกอง']+df2.loc[n]['risk_spectrum']+df2.loc[n]['AI']+df2.loc[n]['invest_country_flag']+df2.loc[n]['ratioAI']+df2.loc[n]['ratioDI']
    token_b = df2.loc[n]['Sector risk']+df2.loc[n]['Total Percent']+df2.loc[n]['UnderratePercentR']
    token_c = df2.loc[n]['Comlexity return']+df2.loc[n]['Derivative']+df2.loc[n]['FX_Ex']+df2.loc[n]['Asset']+df2.loc[n]['Sensitive']+df2.loc[n]['Term to maturity']
    token_d = df2.loc[n]['Nature of liabilities']+df2.loc[n]['Last Resort ']+df2.loc[n]['Funding strategy to support ']
    token_e = df2.loc[n]['ประวัติการทำความผิด']

    token_a2 = 0 if m == 'none' else df2.loc[m]['rank_AUM'] + df2.loc[m]['ประเภทการขายกอง'] + df2.loc[m]['risk_spectrum'] + df2.loc[m]['AI'] + df2.loc[m]['invest_country_flag'] + df2.loc[m]['ratioAI'] + df2.loc[m]['ratioDI']
    token_b2 = 0 if m == 'none' else df2.loc[m]['Sector risk'] + df2.loc[m]['Total Percent'] + df2.loc[m]['UnderratePercentR']
    token_c2 = 0 if m == 'none' else df2.loc[m]['Comlexity return'] + df2.loc[m]['Derivative'] + df2.loc[m]['FX_Ex'] + df2.loc[m]['Asset'] + df2.loc[m]['Sensitive'] + df2.loc[m]['Term to maturity']
    token_d2 = 0 if m == 'none' else df2.loc[m]['Nature of liabilities'] + df2.loc[m]['Last Resort '] + df2.loc[m]['Funding strategy to support ']
    token_e2 = 0 if m == 'none' else df2.loc[m]['ประวัติการทำความผิด']
    return token_a,token_b,token_c,token_d,token_e,token_a2,token_b2,token_c2,token_d2,token_e2

@app.callback(
    Output("BarTable","children"),
    [Input(component_id="MainRiskSelector", component_property="value"),Input(component_id="select", component_property="value"),Input(component_id="select2", component_property="value")]
)
def UpdatefactorGen(a,b,c):
    GenList = ['rank_AUM', 'ประเภทการขายกอง', 'risk_spectrum', 'AI', 'invest_country_flag', 'ratioAI', 'ratioDI']
    AssList = ['Sector risk', 'Total Percent', 'UnderratePercentR']
    MarList = ['Comlexity return', 'Derivative', 'FX_Ex', 'Asset', 'Sensitive', 'Term to maturity']
    LiqList = ['Nature of liabilities', 'Last Resort ', 'Funding strategy to support ']
    LicList = ['ประวัติการทำความผิด']
    x = GenList if a == 'G' else AssList if a == 'A' else MarList if a == 'M' else LiqList if a == 'L' else LicList if a == 'C' else GenList + AssList + MarList + LiqList
    if c == 'none':
        header = [html.Thead(html.Tr([html.Th("Factor"), html.Th("First Score"),html.Th("Second"), ]))]
        Tlist = []
        for i in x:
            Tlist.append(html.Tr([html.Td(i), html.Td(df2.loc[b][i]), html.Td(0.00)]))
        # Tlist = html.Tbody([Tlist])
    else :
        header = [html.Thead(html.Tr([html.Th("Factor"), html.Th("First Score"),html.Th("Second"), ]))]
        Tlist = []
        for i in x:
            Tlist.append(html.Tr([html.Td(i), html.Td(df2.loc[b][i]), html.Td(df2.loc[c][i])]))
        # Tlist = html.Tbody([Tlist])
    return header + Tlist

@app.callback(
    Output(component_id='BarPlot', component_property='figure'), [Input(component_id="MainRiskSelector", component_property="value"),Input(component_id="select", component_property="value"),Input(component_id="select2", component_property="value")]
)
def Bar(a,b,c):
    GenList = ['rank_AUM', 'ประเภทการขายกอง', 'risk_spectrum', 'AI', 'invest_country_flag','ratioAI','ratioDI']
    AssList = ['Sector risk', 'Total Percent','UnderratePercentR']
    MarList = ['Comlexity return', 'Derivative', 'FX_Ex','Asset','Sensitive','Term to maturity']
    LiqList = ['Nature of liabilities', 'Last Resort ', 'Funding strategy to support ']
    LicList = ['ประวัติการทำความผิด']
    x = GenList if a == 'G' else AssList if a == 'A' else MarList if a == 'M' else LiqList if a == 'L' else LicList if a== 'C' else GenList + AssList + MarList + LiqList
    xlist = []
    ylist = []
    xlist2 = []
    ylist2 = []
    for i in x:
        xlist.append(i)
        ylist.append(df2.loc[b][i])
        if c != 'none':
            xlist2.append(i)
            ylist2.append(df2.loc[c][i])
    if c != 'none':
        fig = go.Figure(data=[go.Bar(name='Company1', x=xlist, y=ylist, marker_color='indianred'),
                              go.Bar(name='Company2', x=xlist2, y=ylist2, marker_color='red')])
    else :
        print(xlist)
        print(ylist)
        fig = go.Figure(data=[go.Bar(name='Company1', x=xlist, y=ylist, marker_color='indianred')])
    # Customize aspect
    # fig.update_layout(title_text='  ')
    fig.update_layout(title='Compare 2 Compamy Bar Graph ', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)