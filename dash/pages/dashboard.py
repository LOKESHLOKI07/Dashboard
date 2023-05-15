import numpy as np
import pandas as pd
import mysql.connector as sql
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash import callback
from dash.dependencies import Input, Output, State
import time

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

df1.loc[df1['Article_ID'] == 1, :] = df1.loc[df1['Article_ID'] == 1, :].drop_duplicates()
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

# Define layout
dash.register_page(__name__)

layout = html.Div(children=[
    html.H2(children='Top Service and Event Analysis with Customer Name'),
    dcc.Tab(label='Dashboard', value='1_day', children=[
        dcc.Tabs(id='date-range-tabs', value='1_day', children=[
            dcc.Tab(label='1 Day', value='1_day', children=[
                dcc.DatePickerRange(
                    id='1-day-date-range',
                    min_date_allowed=data_final['Create_Time'].min(),
                    max_date_allowed=data_final['Create_Time'].max(),
                    start_date=data_final['Create_Time'].max() - pd.Timedelta(days=1),
                    end_date=data_final['Create_Time'].max()
                ),
            ]),
            dcc.Tab(label='7 Days', value='7_day', children=[
                dcc.DatePickerRange(
                    id='7-day-date-range',
                    min_date_allowed=data_final['Create_Time'].min(),
                    max_date_allowed=data_final['Create_Time'].max(),
                    start_date=data_final['Create_Time'].max() - pd.Timedelta(days=7),
                    end_date=data_final['Create_Time'].max()
                ),
            ]),
            dcc.Tab(label='30 Days', value='30_day', children=[
                dcc.DatePickerRange(
                    id='30-day-date-range',
                    min_date_allowed=data_final['Create_Time'].min(),
                    max_date_allowed=data_final['Create_Time'].max(),
                    start_date=data_final['Create_Time'].max() - pd.Timedelta(days=30),
                    end_date=data_final['Create_Time'].max()
                ),
            ])
        ]),
        html.Button('Submit', id='submit-button', n_clicks=0),
        dcc.Loading(
            id="loading",
            type="default",
            children=[html.Div(id="chart-container")],
        ),

    ])
])


# Define callback function
@callback(
    Output('chart-container', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('date-range-tabs', 'value'),
     State('1-day-date-range', 'start_date'),
     State('1-day-date-range', 'end_date'),
     State('7-day-date-range', 'start_date'),
     State('7-day-date-range', 'end_date'),
     State('30-day-date-range', 'start_date'),
     State('30-day-date-range', 'end_date')])
def update_charts(n_clicks, date_range, start_date_1d, end_date_1d, start_date_7d, end_date_7d, start_date_30d,
                  end_date_30d):
    # Set start and end dates based on selected date range
    if date_range == '1_day':
        start_date = start_date_1d
        end_date = end_date_1d
    elif date_range == '7_day':
        start_date = start_date_7d
        end_date = end_date_7d
    elif date_range == '30_day':
        start_date = start_date_30d
        end_date = end_date_30d

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # CPU
    cpu = data_final[data_final['CPU'] != 0]
    cpu = cpu[(cpu['Create_Time'] >= start_date) & (cpu['Create_Time'] <= end_date)]
    top10_cpu = cpu.groupby('Customer_Name').size().reset_index(name='CPU_Count').sort_values(by='CPU_Count',
                                                                                              ascending=False)
    # FILESYSTEM
    filesystem = data_final[data_final['Filesystem'] != 0]
    filesystem = filesystem[(filesystem['Create_Time'] >= start_date) & (filesystem['Create_Time'] <= end_date)]
    top10_filesystem = filesystem.groupby('Customer_Name').size().reset_index(name='Filesystem_Count').sort_values(
        by='Filesystem_Count',
        ascending=False)

    # MEMORY
    memory = data_final[data_final['Memory'] != 0]
    memory = memory[(memory['Create_Time'] >= start_date) & (memory['Create_Time'] <= end_date)]
    top10_memory = memory.groupby('Customer_Name').size().reset_index(name='Memory_Count').sort_values(
        by='Memory_Count',
        ascending=False)

    # UPTIME
    uptime = data_final[data_final['Uptime'] != 0]
    uptime = uptime[(uptime['Create_Time'] >= start_date) & (uptime['Create_Time'] <= end_date)]
    top10_uptime = uptime.groupby('Customer_Name').size().reset_index(name='Uptime_Count').sort_values(
        by='Uptime_Count',
        ascending=False)

    # HTTP
    http = data_final[data_final['HTTP'] != 0]
    http = http[(http['Create_Time'] >= start_date) & (http['Create_Time'] <= end_date)]
    top10_http = http.groupby('Customer_Name').size().reset_index(name='HTTP_Count').sort_values(by='HTTP_Count',
                                                                                                 ascending=False)

    # Interface
    interface = data_final[data_final['Interface'] != 0]
    interface = interface[(interface['Create_Time'] >= start_date) & (interface['Create_Time'] <= end_date)]
    top10_interface = interface.groupby('Customer_Name').size().reset_index(name='Interface_Count').sort_values(
        by='Interface_Count',
        ascending=False)

    # ? -> CRIT
    CRIT = data_final[data_final['? -> CRIT'] != 0]
    CRIT = CRIT[(CRIT['Create_Time'] >= start_date) & (CRIT['Create_Time'] <= end_date)]
    top10_CRIT = CRIT.groupby('Customer_Name').size().reset_index(name='? -> CRIT').sort_values(by='? -> CRIT',
                                                                                                ascending=False)

    # CRIT -> OK
    OK = data_final[data_final['CRIT -> OK'] != 0]
    OK = OK[(OK['Create_Time'] >= start_date) & (OK['Create_Time'] <= end_date)]
    top10_OK = OK.groupby('Customer_Name').size().reset_index(name='CRIT -> OK').sort_values(by='CRIT -> OK',
                                                                                             ascending=False)

    # CRIT -> WARN
    WARN = data_final[data_final['CRIT -> WARN'] != 0]
    WARN = WARN[(WARN['Create_Time'] >= start_date) & (WARN['Create_Time'] <= end_date)]
    top10_WARN = WARN.groupby('Customer_Name').size().reset_index(name='CRIT -> WARN').sort_values(by='CRIT -> WARN',
                                                                                                   ascending=False)

    # DOWN -> UP
    UP = data_final[data_final['DOWN -> UP'] != 0]
    UP = UP[(UP['Create_Time'] >= start_date) & (UP['Create_Time'] <= end_date)]
    top10_UP = UP.groupby('Customer_Name').size().reset_index(name='DOWN -> UP').sort_values(by='DOWN -> UP',
                                                                                             ascending=False)

    # OK -> CRIT
    CRIT2 = data_final[data_final['OK -> CRIT'] != 0]
    CRIT2 = CRIT2[(CRIT2['Create_Time'] >= start_date) & (CRIT2['Create_Time'] <= end_date)]
    top10_CRIT2 = CRIT2.groupby('Customer_Name').size().reset_index(name='OK -> CRIT').sort_values(by='OK -> CRIT',
                                                                                                   ascending=False)

    # OK -> UNKN
    UNKNOWN = data_final[data_final['OK -> UNKN'] != 0]
    UNKNOWN = UNKNOWN[(UNKNOWN['Create_Time'] >= start_date) & (UNKNOWN['Create_Time'] <= end_date)]
    top10_UNKNOWN = UNKNOWN.groupby('Customer_Name').size().reset_index(name='OK -> UNKN').sort_values(by='OK -> UNKN',
                                                                                                       ascending=False)

    # OK -> WARN
    WARN2 = data_final[data_final['OK -> WARN'] != 0]
    WARN2 = WARN2[(WARN2['Create_Time'] >= start_date) & (WARN2['Create_Time'] <= end_date)]
    top10_WARN2 = WARN2.groupby('Customer_Name').size().reset_index(name='OK -> WARN').sort_values(by='OK -> WARN',
                                                                                                   ascending=False)

    # UNRE -> DOWN
    DOWN = data_final[data_final['UNRE -> DOWN'] != 0]
    DOWN = DOWN[(DOWN['Create_Time'] >= start_date) & (DOWN['Create_Time'] <= end_date)]
    top10_DOWN = DOWN.groupby('Customer_Name').size().reset_index(name='UNRE -> DOWN').sort_values(by='UNRE -> DOWN',
                                                                                                   ascending=False)

    # UNRE -> UP
    UP2 = data_final[data_final['UNRE -> UP'] != 0]
    UP2 = UP2[(UP2['Create_Time'] >= start_date) & (UP2['Create_Time'] <= end_date)]
    top10_UP2 = UP2.groupby('Customer_Name').size().reset_index(name='UNRE -> UP').sort_values(by='UNRE -> UP',
                                                                                               ascending=False)

    # UP -> DOWN
    DOWN2 = data_final[data_final['UP -> DOWN'] != 0]
    DOWN2 = DOWN2[(DOWN2['Create_Time'] >= start_date) & (DOWN2['Create_Time'] <= end_date)]
    top10_DOWN2 = DOWN2.groupby('Customer_Name').size().reset_index(name='UP -> DOWN').sort_values(by='UP -> DOWN',
                                                                                                   ascending=False)

    # WARN -> CRIT
    CRIT3 = data_final[data_final['WARN -> CRIT'] != 0]
    CRIT3 = CRIT3[(CRIT3['Create_Time'] >= start_date) & (CRIT3['Create_Time'] <= end_date)]
    top10_CRIT3 = CRIT3.groupby('Customer_Name').size().reset_index(name='WARN -> CRIT').sort_values(by='WARN -> CRIT',
                                                                                                     ascending=False)

    # Graphs

    fig_top10_cpu = px.bar(top10_cpu, x='Customer_Name', y='CPU_Count', title='Top CPU with Customer Name')
    fig_top10_filesystem = px.bar(top10_filesystem, x='Customer_Name', y='Filesystem_Count',
                                  title='Top Filesystem with Customer Name')
    fig_top10_memory = px.bar(top10_memory, x='Customer_Name', y='Memory_Count',
                              title='Top Memory with Customer Name')
    fig_top10_uptime = px.bar(top10_uptime, x='Customer_Name', y='Uptime_Count',
                              title='Top Uptime with Customer Name')
    fig_top10_http = px.bar(top10_http, x='Customer_Name', y='HTTP_Count',
                            title='Top HTTP with Customer Name')
    fig_top10_interface = px.bar(top10_interface, x='Customer_Name', y='Interface_Count',
                                 title='Top Interface with Customer Name')
    fig_top10_CRIT = px.bar(top10_CRIT, x='Customer_Name', y='? -> CRIT', title='Top ? -> CRIT with Customer Name')
    fig_top10_OK = px.bar(top10_OK, x='Customer_Name', y='CRIT -> OK', title='Top CRIT -> OK with Customer Name')
    fig_top10_WARN = px.bar(top10_WARN, x='Customer_Name', y='CRIT -> WARN', title='Top CRIT -> WARN with '
                                                                                   'Customer Name')
    fig_top10_UP = px.bar(top10_UP, x='Customer_Name', y='DOWN -> UP', title='Top DOWN -> UP with Customer Name')
    fig_top10_CRIT2 = px.bar(top10_CRIT2, x='Customer_Name', y='OK -> CRIT', title='Top OK -> CRIT with Customer Name')
    fig_top10_UNKNOWN = px.bar(top10_UNKNOWN, x='Customer_Name', y='OK -> UNKN',
                               title='Top OK -> UNKN with Customer Name')
    fig_top10_WARN2 = px.bar(top10_WARN2, x='Customer_Name', y='OK -> WARN', title='Top OK -> WARN with Customer Name')
    fig_top10_DOWN = px.bar(top10_DOWN, x='Customer_Name', y='UNRE -> DOWN',
                            title='Top UNRE -> DOWN with Customer Name')
    fig_top10_UP2 = px.bar(top10_UP2, x='Customer_Name', y='UNRE -> UP', title='Top UNRE -> UP with Customer Name')
    fig_top10_DOWN2 = px.bar(top10_DOWN2, x='Customer_Name', y='UP -> DOWN', title='Top UP -> DOWN with Customer Name')
    fig_top10_CRIT3 = px.bar(top10_CRIT3, x='Customer_Name', y='WARN -> CRIT', title='Top WARN -> CRIT with Customer '
                                                                                     'Name')

    # Create list of graph components to return
    charts = [
        dcc.Graph(
            id='bar-chart-top_cpu',
            figure=fig_top10_cpu
        ),

        dcc.Graph(
            id='bar-chart-top_filesystem',
            figure=fig_top10_filesystem
        ),

        dcc.Graph(
            id='bar-chart-top_memory',
            figure=fig_top10_memory
        ),

        dcc.Graph(
            id='bar-chart-top_uptime',
            figure=fig_top10_uptime
        ),

        dcc.Graph(
            id='bar-chart-top_http',
            figure=fig_top10_http
        ),

        dcc.Graph(
            id='bar-chart-top_interface',
            figure=fig_top10_interface
        ),

        dcc.Graph(
            id='bar-chart-top_? -> CRIT',
            figure=fig_top10_CRIT
        ),

        dcc.Graph(
            id='bar-chart-top_CRIT -> OK',
            figure=fig_top10_OK
        ),

        dcc.Graph(
            id='bar-chart-top_CRIT -> WARN',
            figure=fig_top10_WARN
        ),

        dcc.Graph(
            id='bar-chart-top_DOWN -> UP',
            figure=fig_top10_UP
        ),

        dcc.Graph(
            id='bar-chart-top_OK -> CRIT',
            figure=fig_top10_CRIT2
        ),
        dcc.Graph(
            id='bar-chart-bottom_OK -> UNKN',
            figure=fig_top10_UNKNOWN
        ),

        dcc.Graph(
            id='bar-chart-top_OK -> WARN',
            figure=fig_top10_WARN2
        ),

        dcc.Graph(
            id='bar-chart-top_UNRE -> DOWN',
            figure=fig_top10_DOWN
        ),

        dcc.Graph(
            id='bar-chart-top_UNRE -> UP',
            figure=fig_top10_UP2
        ),

        dcc.Graph(
            id='bar-chart-top_UP -> DOWN',
            figure=fig_top10_DOWN2
        ),

        dcc.Graph(
            id='bar-chart-top_WARN -> CRIT',
            figure=fig_top10_CRIT3
        ),

    ]

    # Only show the graphs if the Submit button has been clicked
    if n_clicks > 0:
        return charts
    else:
        return []
