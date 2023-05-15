import numpy as np
import pandas as pd
import mysql.connector as sql
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash import callback

db_connection = sql.connect(host='otrs.futurenet.in', database='otrs5', user='readuser2', password='6FbUDa5VM')
query = '''SELECT t.id AS ticketid,t.tn,t.title AS ticketname,th.id AS ticket_history_id,th.name AS ticket_history_name,a.id AS article_id,a.ticket_id AS article_ticket_id,a.article_type_id as article_type_id,a.a_body AS message,q.id AS queue_id,q.name AS queue_name,t.create_time AS create_time
FROM ticket AS t
INNER  JOIN ticket_history AS th ON th.ticket_id = t.id
INNER  JOIN article AS a ON a.id=th.article_id
INNER  JOIN queue AS q ON t.queue_id  = q.id
where q.id IN (40)'''

df = pd.read_sql(query, con=db_connection)
data = df[['ticketid', 'ticketname', 'article_type_id', 'message', 'create_time']]

host = data['message'].str.extract(r'Host:\s+([\w\.-]+)', expand=False)
ip = data['message'].str.extract(r'Address:\s+([\d.]+)', expand=False)
event = data['message'].str.extract(r'Event:\s+([^\n]+)', expand=False)
service = data['message'].str.extract(r'Service:\s+(\w+)', expand=False)
df1 = pd.DataFrame({'Ticket_ID': df['tn'], 'Ticket_Name': df['ticketname'], 'Article_ID': data['article_type_id'],
                    'message': data['message'], 'Host_Name': host, 'IP_Address': ip, 'Event': event, 'Service': service,
                    'Create_Time': data['create_time']})

df1.loc[data['article_type_id'] == 1, 'Host_Name']
df1.loc[data['article_type_id'] == 1, 'IP_Address']
df1.loc[data['article_type_id'] == 1, 'Event']
df1.loc[data['article_type_id'] == 1, 'Service']

df1_filter = df1[df1['Article_ID'] == 1]
df1_filter['Customer_Name'] = df1['Ticket_Name'].str.split(' :: ').str[0]
df1_filter['Customer_Name'] = df1['Ticket_Name'].str.split(':').str[0]
df1_filter = df1_filter.drop(index=0)
df1_final = df1_filter[['Ticket_ID', 'Customer_Name', 'Host_Name', 'IP_Address', 'Event', 'Service', 'Create_Time']]
df1_final = df1_final.sort_values(by=['Customer_Name', 'Host_Name'])
df1_final_cp = df1_final.copy()

dummies = pd.get_dummies(df1_final_cp[['Event', 'Service']], dummy_na=True)
dummies.drop(['Service_nan', 'Event_nan'], axis=1, inplace=True)
dummies.columns = dummies.columns.str.split('_').str.get(1)

df1_final_cpp = pd.concat([df1_final_cp, dummies], axis=1)

exclude_cols = ['Event', 'Service']
data_final = df1_final_cpp.loc[:, ~df1_final_cpp.columns.isin(exclude_cols)]

# Define the app and layout

dash.register_page(__name__)
layout = html.Div(children=[
    html.H2(children='Customer EPO Analysis'),

    dcc.Dropdown(
        id='customer-dropdown',
        options=[{'label': customer, 'value': customer} for customer in data_final['Customer_Name'].unique()],
        value=data_final['Customer_Name'].unique()[0]
    ),
    # Create the bar chart
    dcc.Graph(id='cpu-count-graph'),
    dcc.Graph(id='filesystem-count-graph')

])


# Define the callback for updating the bar chart
@callback(
    dash.dependencies.Output('cpu-count-graph', 'figure'),
    dash.dependencies.Output('filesystem-count-graph', 'figure'),
    [dash.dependencies.Input('customer-dropdown', 'value')]
)
def update_graph(customer):
    cpu = data_final[data_final['CPU'] != 0]
    cpu = data_final[data_final['Customer_Name'] == customer]
    top10_cpu = cpu.groupby('Host_Name')['CPU'].count().reset_index(name='CPU_Count')

    filesystem = data_final[data_final['Filesystem'] != 0]
    filesystem = data_final[data_final['Customer_Name'] == customer]
    top10_filesystem = filesystem.groupby('Host_Name')['Filesystem'].count().reset_index(name='Filesystem_Count')

    # Create the bar chart
    fig_cpu = px.bar(top10_cpu, x='Host_Name', y='CPU_Count', title=f'CPU Count for {customer}')
    fig_filesystem = px.bar(top10_filesystem, x='Host_Name', y='Filesystem_Count', title=f'Filesystem Count for {customer}')

    return fig_cpu, fig_filesystem
