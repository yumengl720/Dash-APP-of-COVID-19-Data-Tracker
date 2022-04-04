import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dash.exceptions import PreventUpdate
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

# Load Dataset


# load and process the first dataset
state_vac = pd.read_csv(r'/Users/mengmengmeng/Desktop/stat430/final/COVID-19_Vaccinations_in_the_United_States_Jurisdiction.csv')
state_vac['Date'] = pd.to_datetime(state_vac['Date']).dt.strftime("%Y/%m/%d")
state_vac  =state_vac.loc[~state_vac['Location'].isin(['BP2','DD2','IH2','VA2'])]
mytotaldates = {i:x for i,x in enumerate(sorted(state_vac['Date'].unique()))}
a = (list(mytotaldates.keys()))

# load and process the second dataset
county_vac = pd.read_csv(r'/Users/mengmengmeng/Desktop/stat430/final/COVID-19_Vaccinations_in_the_United_States_County.csv')
county_vac = county_vac.loc[county_vac['Recip_State']!='UNK',:]
county_vac['Date'] = pd.to_datetime(county_vac['Date']).dt.strftime("%Y/%m/%d")
def f(x):
    return str(x).zfill(5)
county_vac['FIPS'] = county_vac['FIPS'].apply(f)

# load and process the third dataset
trans = pd.read_csv(r'/Users/mengmengmeng/Desktop/stat430/final/United_States_COVID-19_County_Level_of_Community_Transmission_as_Originally_Posted.csv')
trans.dropna(inplace=True)
trans['report_date'] = pd.to_datetime(trans['report_date']).dt.strftime("%Y/%m/%d")
def fun(x):
    x = str(x)
    x = x.replace(',','')
    return float(x)
trans.loc[trans['cases_per_100K_7_day_count_change']=='suppressed','cases_per_100K_7_day_count_change']=5
trans['cases_per_100K_7_day_count_change']=trans['cases_per_100K_7_day_count_change'].map(fun)
trans.loc[:,'Daily_new_cases_7_day_moving_average']=trans.loc[:,'cases_per_100K_7_day_count_change']/7
us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}
trans['state_name'] = trans['state_name'].map(us_state_to_abbrev)

# get a list a US State names to be used in RadioItem
available_state = sorted(trans['state_name'].unique())


# Design Dash app layout
app.layout = html.Div([
	html.Div([
		html.H1('US COVID-19 Data Tracker',style=dict(display='flex', justifyContent='center')),
	    html.Br(),
	    # Input 1
	    dcc.RadioItems(
	    	id='vac_opts',
	    	options=[
	    	{'label':'Fully Vaccinated', 'value':'Series_Complete_Pop_Pct'},
	    	{'label':'At Least 1 Dose','value':'Administered_Dose1_Pop_Pct'}
	    	],
	    	value = 'Series_Complete_Pop_Pct',
	    	labelStyle={'display': 'inline-block'},
	    	style=dict(display='flex', justifyContent='center')
	    	),
	    # Graph 1
	    dcc.Graph(id='graph',style={'width': '100%', 'height': '100%','textAlign': 'center'}),
	    html.Br(),
	    # Input 2
	    dcc.Slider(
	        id='Date',
	        min=a[0],
	        max=a[-1],
	        #marks=mytotaldates,
	        value=a[-1]
	    	),
	    html.Div(id='display-selected-date1')
	    ]),
    html.Div([

		html.Div([
			html.H6('Please choose a State'),
			# Input 3
			dcc.Dropdown(
			    id='state',
			    options=[{'label': i, 'value': i} for i in available_state],
			    value='AK'
					),
			html.Br(),
			# Input 5
			dcc.RadioItems(
				id='vac_opts_2',
				options=[
				{'label':'Fully Vaccinated', 'value':'Series_Complete_Pop_Pct'},
				{'label':'At Least 1 Dose','value':'Administered_Dose1_Pop_Pct'}
						],
				value = 'Series_Complete_Pop_Pct',
				labelStyle={'display': 'inline-block'},
				style=dict(display='flex', justifyContent='center')
				),
			html.Br(),
			#dcc.Graph(id='graph2',style={'width': '100%', 'height': '100%','textAlign': 'center'}),
			dcc.Graph(id='graph2'),
			html.Br(),
			# Input 6
			dcc.Slider(
			    id='Date2'
				),
			html.Div(id='display-selected-date2')
			], style={'width': '48%', 'display': 'inline-block'}),
		html.Div([
			html.H6('Please choose a County'),
			# Input 4
			dcc.Dropdown(
			    id='county'),
			html.Br(),
			# Input 7
			dcc.RangeSlider(
			    id='Date3'
				),
			html.Div(id='display-selected-date3'),
			html.Br(),
			# Graph 3
			dcc.Graph(id='graph3'),
			html.Br(),
			# Graph 4
			dcc.Graph(id='graph4')

			], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
	])
])	

# design feedback of input 2: selecting a date will show the selections
@app.callback(
	Output('display-selected-date1','children'),
	Input('Date', 'value'))
def display_date_1(selected_date):
	return "Date: {}".format(mytotaldates[selected_date])
# update graph 1
@app.callback(
    Output('graph', 'figure'),
    Input('vac_opts', 'value'),
    Input('Date', 'value'))

def update_figure(selected_opts,selected_date):
	selected_data = state_vac.loc[state_vac['Date']==mytotaldates[selected_date],['Location',selected_opts]]
	fig = go.Figure(data = go.Choropleth(
	    locations=selected_data['Location'], # Spatial coordinates
	    z = selected_data[selected_opts], # Data to be color-coded
	    locationmode = 'USA-states', # set of locations match entries in `locations`
	    #range_color = (0,100),
	    #autocolorscale=False,
	    colorscale = 'Blues',
	    zmin=0,
	    zmax=80,

	    colorbar_title = "Percentage of State Population Vaccinated",
	    hovertext = selected_data['Location'],
	    hovertemplate = "<b>%{hovertext}</b><br> <br>%: %{z}<extra></extra>"
	))

	fig.update_layout(
	    margin={"r":0,"t":50,"l":300,"b":0},geo_scope='usa', title={
        'text': "US State Map Colored by Vaccination %  at {}".format(mytotaldates[selected_date]),
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}
	)
	return fig


# set dependent county options based on state options
@app.callback(
	Output('county','options'),
	Input('state','value'))
def set_county_options(selected_state):
	return [{'label': i, 'value': i} for i in sorted(trans.loc[trans['state_name']==selected_state,'county_name'].unique())]

@app.callback(
	Output('county','value'),
	Input('county','options'))
def set_county_value(available_options):
	
	return available_options[0]['value']


# set dependent input6 &7
@app.callback(
	Output('Date2','min'),
    Output('Date2','max'),
    #Output('Date2','marks'),
    Output('Date2','value'),
    Output('Date3','min'),
    Output('Date3','max'),
    #Output('Date3','marks'),
    Output('Date3','value'),
    Input('state', 'value'),
    Input('county','value'))
def set_date_options(selected_state,selected_county):
    mytotaldates2 = {i:x for i,x in enumerate(sorted(county_vac.loc[county_vac['Recip_State']==selected_state,['Date']]['Date'].unique()))}

    a2 = list(mytotaldates2.keys())

    totaldates3 = {i:x for i,x in enumerate(sorted(trans.loc[(trans['state_name']==selected_state)&(trans['county_name']==selected_county),['report_date']]['report_date'].unique()))}
    a3 = list(totaldates3.keys())
    if len(a3)==0:
        raise PreventUpdate
    else:
        return a2[0],a2[-1],a2[-1],a3[0],a3[-1],[a3[0],a3[-1]]


	
 
# Update graph 2 and give feedback of input6 selection
@app.callback(
    Output('graph2', 'figure'),
    Output('display-selected-date2','children'),
    Input('vac_opts_2', 'value'),
    Input('Date2', 'value'),
    Input('state','value'))
def update_figure2(selected_opts,selected_date,selected_state):
	mytotaldates2 = {i:x for i,x in enumerate(sorted(county_vac.loc[county_vac['Recip_State']==selected_state,['Date']]['Date'].unique()))}
	selected_data_2 = county_vac.loc[(county_vac['Date']==mytotaldates2[selected_date])&(county_vac['Recip_State']==selected_state),['FIPS','Recip_County',selected_opts]]
	fig = px.choropleth(selected_data_2, geojson=counties, locations='FIPS', color=selected_opts,
                           color_continuous_scale="Blues",
                           range_color=[0,80],
                           scope="usa",
                           labels={'Recip_County':'County','Administered_Dose1_Pop_Pct':'% of at least one doze','Series_Complete_Pop_Pct':'% of fully vaccinated'},
                           hover_data=['FIPS','Recip_County',selected_opts]
                          )
	fig.update_layout(margin={"r":0,"t":100,"l":0,"b":0},title={
        'text': "{} map colored by vaccination %  at {}".format(selected_state,mytotaldates2[selected_date]),
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
	return fig,"Date: {}".format(mytotaldates2[selected_date])

# update graph 3 & 4
@app.callback(
    Output('graph3', 'figure'),
    Output('graph4', 'figure'),
    Output('display-selected-date3','children'),
    Input('state', 'value'),
    Input('county', 'value'),
    Input('Date3','value'))
def update_figure3(selected_state,selected_county,selected_date_opts):
	
	mytotaldates3 = {i:x for i,x in enumerate(sorted(trans.loc[(trans['state_name']==selected_state)&(trans['county_name']==selected_county),['report_date']]['report_date'].unique()))}
	selected_data_3 = trans.loc[(trans['report_date']>=mytotaldates3[selected_date_opts[0]])&(trans['report_date']<=mytotaldates3[selected_date_opts[1]])&(trans['state_name']==selected_state)&(trans['county_name']==selected_county),['report_date','percent_test_results_reported_positive_last_7_days']]
	selected_data_3.sort_values('report_date',ascending=True,inplace=True)

	fig3 = px.line(selected_data_3, x='report_date', y="percent_test_results_reported_positive_last_7_days",labels={'report_date':'Report date','percent_test_results_reported_positive_last_7_days':'Percentage of positivity in last 7 days'})
	fig3.update_layout(title={
        'text': "Daily % Positivity of {},{} from {} to {}".format(selected_county,selected_state,mytotaldates3[selected_date_opts[0]],mytotaldates3[selected_date_opts[1]]),
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
	selected_data_4 = trans.loc[(trans['report_date']>=mytotaldates3[selected_date_opts[0]])&(trans['report_date']<=mytotaldates3[selected_date_opts[1]])&(trans['state_name']==selected_state)&(trans['county_name']==selected_county),['report_date','Daily_new_cases_7_day_moving_average']]
	selected_data_4.sort_values('report_date',ascending=True,inplace=True)
	fig4 = px.line(selected_data_4, x='report_date', y="Daily_new_cases_7_day_moving_average",labels={'report_date':'Report date','Daily_new_cases_7_day_moving_average':'Daily new cases 7-day moving average per 100K'})
	fig4.update_layout(title={
        'text': "Daily New Cases Per 100K - 7-day Moving Average",
       'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
	return fig3,fig4,"Date: {}-{}".format(mytotaldates3[selected_date_opts[0]],mytotaldates3[selected_date_opts[1]])
	
if __name__ == '__main__':
    app.run_server(debug=True)
