# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv(r"C:/Users/Aziz/Desktop/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                dcc.Dropdown(id='site-dropdown',
                                             options=[{'label': 'All Sites', 'value': 'ALL'},
                                                      {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                      {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                      {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                      {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                                             value='ALL',
                                             placeholder='Select the Launch Site here',
                                             searchable=True),
                                html.Br(),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the
                                # site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                marks={0: '0',
                                                       100: '100'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie(value):
    if value == 'ALL':
        pie_chart = px.pie(data_frame=spacex_df,
                           values='class',
                           names='Launch Site',
                           title='Total number of successful landings for all Launch Sites')
        return pie_chart
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == value].groupby(['Launch Site', 'class']). \
            size().reset_index(name='class count')
        title = f'Total launches for site {value}'
        pie_chart_2 = px.pie(data_frame=filtered_df,
                             values='class count',
                             names='class',
                             title=title)
        return pie_chart_2


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(value1, value2):
    filtered_df_2_1 = spacex_df[(spacex_df['Payload Mass (kg)'] > value2[0]) & \
                               (spacex_df['Payload Mass (kg)'] < value2[1])]
    if value1 == 'ALL':
        scatter_chart = px.scatter(data_frame=filtered_df_2_1,
                                   x='Payload Mass (kg)',
                                   y='class',
                                   color='Booster Version Category',
                                   title='Correlation between Payload and Success for all Launch Sites')
        return scatter_chart
    else:

        filtered_df_2_2 = filtered_df_2_1[filtered_df_2_1['Launch Site'] == value1]
        scatter_chart_2 = px.scatter(data_frame=filtered_df_2_2,
                                     x='Payload Mass (kg)',
                                     y='class',
                                     color='Booster Version Category',
                                     title=f'Correlation between Payload and Success for site {value1}')
        return scatter_chart_2


# Run the app


if __name__ == '__main__':
    app.run_server()
