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
site_options = [{'label': i, 'value': i} for i in spacex_df['Launch Site'].unique()]
site_options.insert(0,{'label': 'All Sites', 'value': 'ALL'},)
print(site_options)
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Div(["Launch Site: ",dcc.Dropdown(id='site-dropdown',
                                                                       options=site_options,
                                                                       placeholder='Select a Launch Site here',
                                                                       value='ALL',
                                                                       searchable = True
                                                                       )]),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                               
                                html.Div(dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                    100: '100'},
                                                value=[min_payload, max_payload])),
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
            filtered_df = spacex_df[spacex_df['class'] == 1]

            fig = px.pie(filtered_df, values='class', 
            names='Launch Site', 
            title='Total Success Launches by Site')
            return fig
    else:
       

        filtered_df=    spacex_df[spacex_df['Launch Site'] == entered_site].groupby('class')['Launch Site'].count().reset_index()

        fig = px.pie(filtered_df, values='Launch Site', 
        names='class', 
        title='Total Success Launches by Site '+ entered_site)
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site,payload_slider):
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['Payload Mass (kg)'] > payload_slider[0]][spacex_df['Payload Mass (kg)'] < payload_slider[1]]
        fig = px.scatter(filtered_df, y='class', 
            x='Payload Mass (kg)', 
            title='Total Success Launches by All Sites',
            color="Booster Version Category")
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site][spacex_df['Payload Mass (kg)'] > payload_slider[0]][spacex_df['Payload Mass (kg)'] < payload_slider[1]]
        print(payload_slider[0])
        print(filtered_df)

        fig = px.scatter(filtered_df, y='class', 
            x='Payload Mass (kg)', 
            title='Total Success Launches by Site' + entered_site,
            color="Booster Version Category")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()

