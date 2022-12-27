import dash
from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import pandas as pd
import plotly.express as px

## --format number
def human_format(num):
  num = float('{:.3g}'.format(num))
  magnitude = 0
  while abs(num) >= 1000:
    magnitude += 1
    num /= 1000.0
  return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

app = dash.Dash(
    external_stylesheets=[dbc.themes.LUX],
    name = 'Covid-19 Dashboard'
)

app.title = 'Covid-19 Dashboard Analytics'

## ---Import dataset
covid=pd.read_csv('covid.csv')

## --List All Countries
country_list = list(covid['Country/Region'].unique())
country_list.append('All Countries')
country_list.sort()

## ---Navbar
navbar = dbc.NavbarSimple([

    ## --Select Country
    dbc.Col([
        dbc.DropdownMenu(
            dcc.Dropdown(
                id='choose_country',
                options=country_list,
                value='All Countries',
                style={'width':'180%',}, 
            ), label='Select Country/Region', size="sm",
        ),
    ], width=7,),

    ## --Date Range
    dbc.Col([
        dbc.DropdownMenu( 
            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=covid['ObservationDate'].min(),
                max_date_allowed=covid['ObservationDate'].max(),
                start_date=covid['ObservationDate'].min(),
                end_date=covid['ObservationDate'].max(),
            ), label='Select Date Range', size="sm",
        ),
    ], width=5,)
     
], brand="Covid-19 Dashboard Analytics",
brand_href="#",
color="#5c6b73",
dark=True,
)

## --- DASHBOARD LAYOUT

## --LAYOUT
app.layout = html.Div([
    navbar,
    
    ## --Component Main Page--

    html.Div([

        ## --Row1
        dbc.Row([

            ##Col1
            dbc.Col([
                dbc.Card(id='card_confirmed', color='#ffc300'),
            ], width=4),

            ##Col2
            dbc.Col([
                dbc.Card(id='card_death', color='#cc444b'),
            ], width=4),

            ##Col3
            dbc.Col([
                dbc.Card(id='card_recovered', color='#73ba9b'),
            ], width=4),  
        ], style={'backgroundColor':'white', 'paddingTop':'30px', 'paddingRight':'15px', 'paddingLeft':'15px', 'paddingBottom':'30px'}),

        ## --Row2
        dbc.Row([
            html.H2('Analysis by Cases'),
            dbc.Tabs([
                ## ---TAB 1: confirmed
                dbc.Tab([
                    dbc.Row([
                        dbc.Col(
                            dcc.Graph(
                                id='mapconfirmed',
                            ), width=6
                        ),

                        dbc.Col(
                            dcc.Graph(
                                id='lineconfirmed',
                            ), width=6
                        ),
                    ]),
                ], 
                label='Confirmed',
                active_tab_style={"textTransform": "uppercase"},
                active_label_style={"color": "#ffc300"}), 

                ## --TAB 2 : deaths
                dbc.Tab([
                    dbc.Row([
                        dbc.Col(
                            dcc.Graph(
                                id='mapdeaths',
                            ), width=6
                        ),

                        dbc.Col(
                            dcc.Graph(
                                id='linedeaths',
                            ), width=6
                        ),
                    ]),
                ], 
                label='Death',
                active_tab_style={"textTransform": "uppercase"},
                active_label_style={"color": "#cc444b"}),
                    
                ## --TAB 3 : recovered
                dbc.Tab([
                    dbc.Row([
                        dbc.Col(
                            dcc.Graph(
                                id='maprecovered',
                            ), width=6
                        ),

                        dbc.Col(
                            dcc.Graph(
                                id='linerecovered',
                            ), width=6
                        ),
                    ]),
                ], 
                label='Recovered',
                active_tab_style={"textTransform": "uppercase"},
                active_label_style={"color": "#008B8B"}),
            ]),
        ], style={'backgroundColor':'white'}),

        html.Hr(),

        ## --Row3 REFERENCE
        dbc.Row([
            html.H3('Reference'),
            ## --- col data csv
            dbc.Col([
                dash_table.DataTable(covid.to_dict('records'),[{"name": x, "id": x} for x in covid.columns], id='table', page_size=10),
            ], width=8),
            
            ## --- card info reference
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.P('About this data: Daily level information on the number of Covid 2019 affected cases across the globe.'),
                        html.P(['Data Source: ', html.A("Covid 19 Dataset", href='https://www.kaggle.com/code/nulldata/covid-19-impact-interactive-dashboard-updated/data', target="_blank"),]),
                    ]),
                ]),
            ], width=4),
        ], style={'backgroundColor':'white', 'paddingTop' : '15px'}),
        html.Br(),

    ], style={
        'backgroundColor':'#bfc0c0',
        'paddingRight':'30px',
        'paddingLeft':'30px',
        'paddingBottom':'30x',
        'paddingTop':'30px',
    })
])

## Callback Card Confirmed
@app.callback(
    Output(component_id='card_confirmed', component_property='children'),
    Input(component_id='choose_country', component_property='value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
)

def update_plot1(country_name, start_date, end_date):
    if country_name == 'All Countries' :
        covid_world = covid
    else: 
        covid_world = covid[covid['Country/Region'] == country_name]
    
    covid_world = covid_world[(covid_world['ObservationDate']>=start_date) & (covid_world['ObservationDate']<=end_date)]

    total_confirmed = [
        dbc.CardHeader(f'Total Confirmed Cases in {country_name}', className='text-center', style={'color':'black'}),
        dbc.CardBody([
            html.H1(human_format(covid_world['Confirmed'].sum()),
            className='text-center',)
        ]), 
    ]

    return total_confirmed

## Callback Card Death
@app.callback(
    Output(component_id='card_death', component_property='children'),
    Input(component_id='choose_country', component_property='value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
)

def update_plot2(country_name, start_date, end_date):
    if country_name == 'All Countries' :
        covid_world = covid
    else: 
        covid_world = covid[covid['Country/Region'] == country_name]
    
    covid_world = covid_world[(covid_world['ObservationDate']>=start_date) & (covid_world['ObservationDate']<=end_date)]

    total_death = [
        dbc.CardHeader(f'Total Death Cases in {country_name}', className='text-center', style={'color':'black'}),
        dbc.CardBody([
            html.H1(human_format(covid_world['Deaths'].sum()),
            className='text-center')
        ]),
    ]

    return total_death

## Callback Card Recovered
@app.callback(
    Output(component_id='card_recovered', component_property='children'),
    Input(component_id='choose_country', component_property='value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
)

def update_plot3(country_name, start_date, end_date):
    if country_name == 'All Countries' :
        covid_world = covid
    else: 
        covid_world = covid[covid['Country/Region'] == country_name]
    
    covid_world = covid_world[(covid_world['ObservationDate']>=start_date) & (covid_world['ObservationDate']<=end_date)]

    total_recovered = [
        dbc.CardHeader(f'Total Recovered Cases in {country_name}', className='text-center', style={'color':'black'}),
        dbc.CardBody([
            html.H1(human_format(covid_world['Recovered'].sum()),
            className='text-center')
        ]),
    ]

    return total_recovered

## Callback Map Confirmed
@app.callback(
    Output(component_id='mapconfirmed', component_property='figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
)

def update_plot4(start_date, end_date):
    covid_world = covid[(covid['ObservationDate']>=start_date) & (covid['ObservationDate']<=end_date)]

    map1 = pd.pivot_table(
        data=covid_world,
        index='CountryCode',
        values='Confirmed',
        aggfunc='sum').reset_index()

    map_confirmed = px.choropleth(
        map1,
        locations='CountryCode',
        locationmode='ISO-3',
        color_continuous_scale='YlOrBr',
        color='Confirmed',
        title='Countries with nCov Exposure of Total Confirmed Cases',
        template = 'ggplot2')

    return map_confirmed

## Callback Map Deaths
@app.callback(
    Output(component_id='mapdeaths', component_property='figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
)

def update_plot5(start_date, end_date):
    covid_world = covid[(covid['ObservationDate']>=start_date) & (covid['ObservationDate']<=end_date)]

    map2 = pd.pivot_table(
        data=covid_world,
        index='CountryCode',
        values='Deaths',
        aggfunc='sum').reset_index()

    map_deaths = px.choropleth(
        map2,
        locations='CountryCode',
        locationmode='ISO-3',
        color_continuous_scale='reds',
        color='Deaths',
        title='Countries with nCov Exposure of Total Death Cases',
        template = 'ggplot2')

    return map_deaths

## Callback Map Recovered
@app.callback(
    Output(component_id='maprecovered', component_property='figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
)

def update_plot6(start_date, end_date):
    covid_world = covid[(covid['ObservationDate']>=start_date) & (covid['ObservationDate']<=end_date)]

    map3 = pd.pivot_table(
        data=covid_world,
        index='CountryCode',
        values='Recovered',
        aggfunc='sum').reset_index()

    map_recovered = px.choropleth(
        map3,
        locations='CountryCode',
        locationmode='ISO-3',
        color_continuous_scale='mint',
        color='Recovered',
        title='Countries with nCov Exposure of Total Recovered Cases',
        template = 'ggplot2')

    return map_recovered

## Callback Line Confirmed
@app.callback(
    Output(component_id='lineconfirmed', component_property='figure'),
    Input(component_id='choose_country', component_property='value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
)

def update_plot7(country_name, start_date, end_date):
    if country_name == 'All Countries' :
        covid_world = covid
    else: 
        covid_world = covid[covid['Country/Region'] == country_name]
    
    covid_world = covid_world[(covid_world['ObservationDate']>=start_date) & (covid_world['ObservationDate']<=end_date)]

    total_confirmed_per_date = pd.pivot_table(
        data=covid_world,
        index='ObservationDate',
        values='Confirmed',
        aggfunc='sum').sort_values(by='ObservationDate')
    
    line_confirmed = px.line(
        total_confirmed_per_date,
        title=f'COVID-19 Confirmed Cases per Date in {country_name}',
        template = 'ggplot2')
    
    line_confirmed.update_layout(
        xaxis_title="Observation Date",
        yaxis_title="Total Confirmed",
    )

    line_confirmed.layout.update(showlegend=False)
    
    line_confirmed.update_traces(line_color='#f0c808')

    return line_confirmed

## Callback Line Death
@app.callback(
    Output(component_id='linedeaths', component_property='figure'),
    Input(component_id='choose_country', component_property='value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
)

def update_plot8(country_name, start_date, end_date):
    if country_name == 'All Countries' :
        covid_world = covid
    else: 
        covid_world = covid[covid['Country/Region'] == country_name]
    
    covid_world = covid_world[(covid_world['ObservationDate']>=start_date) & (covid_world['ObservationDate']<=end_date)]

    total_deaths_per_date = pd.pivot_table(
        data=covid_world,
        index='ObservationDate',
        values='Deaths',
        aggfunc='sum').sort_values(by='ObservationDate')
    
    line_death = px.line(
        total_deaths_per_date,
        title=f'COVID-19 Death Cases per Date in {country_name}',
        template = 'ggplot2')
    
    line_death.update_layout(
        xaxis_title="Observation Date",
        yaxis_title="Total Deaths",
    )

    line_death.layout.update(showlegend=False)
    
    line_death.update_traces(line_color='#d00000')

    return line_death

## Callback Line Recovered
@app.callback(
    Output(component_id='linerecovered', component_property='figure'),
    Input(component_id='choose_country', component_property='value'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
)

def update_plot9(country_name, start_date, end_date):
    if country_name == 'All Countries' :
        covid_world = covid
    else: 
        covid_world = covid[covid['Country/Region'] == country_name]
    
    covid_world = covid_world[(covid_world['ObservationDate']>=start_date) & (covid_world['ObservationDate']<=end_date)]

    total_recovered_per_date = pd.pivot_table(
        data=covid_world,
        index='ObservationDate',
        values='Recovered',
        aggfunc='sum').sort_values(by='ObservationDate')
    
    line_recovered = px.line(
        total_recovered_per_date,
        title=f'COVID-19 Recovered Cases per Date in {country_name}',
        template = 'ggplot2')
    
    line_recovered.update_layout(
        xaxis_title="Observation Date",
        yaxis_title="Total Recovered",
    )

    line_recovered.layout.update(showlegend=False)
    
    line_recovered.update_traces(line_color='#008B8B')

    return line_recovered

if __name__ == "__main__":
    app.run_server()