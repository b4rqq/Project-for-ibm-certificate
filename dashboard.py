# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#2503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id = 'site-dropdown',
                                               options=[{'label': 'All Sites', 'value': 'ALL'},
                                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}],
                                               value = 'ALL'),
                                
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-range',
                                        min=0, max=10000, step=1000,
                                        value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total success launches by site')
        return fig
    else:
        site_data = spacex_df[spacex_df['Launch Site'] == entered_site]
        counts = site_data['class'].value_counts()
        fig = px.pie(values=counts.values,
                    names=counts.index, 
                    title=f'Total success launches for site {entered_site}')
        return fig
        
        
        
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-range', component_property='value')])
def get_scatter_plot(entered_site, entered_range):
    kok = spacex_df[spacex_df['Payload Mass (kg)'].between(entered_range[0], entered_range[1])]
    if entered_site == 'ALL':
        fig = px.scatter(kok, 
        x = "Payload Mass (kg)",
        y = "class",
        title='Corelation between payload and success for all sites',
        color="Booster Version Category",
        range_y = [-0.25,1.25])
        return fig
    else:
        site_kok = kok[kok['Launch Site'] == entered_site]
        fig = px.scatter(site_kok, 
        x = "Payload Mass (kg)",
        y = "class",
        title=f'Corelation between payload and success for {entered_site}',
        color="Booster Version Category",
        range_y = [-0.25,1.25])
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server(port="8056")