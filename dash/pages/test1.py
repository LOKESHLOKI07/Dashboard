# import numpy as np
# import pandas as pd
# import mysql.connector as sql
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import plotly.express as px
# from dash import callback
#
# db_connection = sql.connect(host='otrs.futurenet.in', database='otrs5', user='readuser2', password='6FbUDa5VM')
# query = '''SELECT t.id AS ticketid,t.tn,t.title AS ticketname,th.id AS ticket_history_id,th.name AS ticket_history_name,a.id AS article_id,a.ticket_id AS article_ticket_id,a.article_type_id as article_type_id,a.a_body AS message,q.id AS queue_id,q.name AS queue_name,t.create_time AS create_time
# FROM ticket AS t
# INNER  JOIN ticket_history AS th ON th.ticket_id = t.id
# INNER  JOIN article AS a ON a.id=th.article_id
# INNER  JOIN queue AS q ON t.queue_id  = q.id
# where q.id IN (40)'''
#
# df = pd.read_sql(query, con=db_connection)
# data = df[['ticketid', 'ticketname', 'article_type_id', 'message', 'create_time']]
#
# host = data['message'].str.extract(r'Host:\s+([\w\.-]+)', expand=False)
# ip = data['message'].str.extract(r'Address:\s+([\d.]+)', expand=False)
# event = data['message'].str.extract(r'Event:\s+([^\n]+)', expand=False)
# service = data['message'].str.extract(r'Service:\s+(\w+)', expand=False)
# df1 = pd.DataFrame({'Ticket_ID': df['tn'], 'Ticket_Name': df['ticketname'], 'Article_ID': data['article_type_id'],
#                     'message': data['message'], 'Host_Name': host, 'IP_Address': ip, 'Event': event, 'Service': service,
#                     'Create_Time': data['create_time']})
#
# df1.loc[data['article_type_id'] == 1, 'Host_Name']
# df1.loc[data['article_type_id'] == 1, 'IP_Address']
# df1.loc[data['article_type_id'] == 1, 'Event']
# df1.loc[data['article_type_id'] == 1, 'Service']
#
# df1_filter = df1[df1['Article_ID'] == 1]
# df1_filter['Customer_Name'] = df1['Ticket_Name'].str.split(' :: ').str[0]
# df1_filter['Customer_Name'] = df1['Ticket_Name'].str.split(':').str[0]
# df1_filter = df1_filter.drop(index=0)
# df1_final = df1_filter[['Ticket_ID', 'Customer_Name', 'Host_Name', 'IP_Address', 'Event', 'Service', 'Create_Time']]
# df1_final = df1_final.sort_values(by=['Customer_Name', 'Host_Name'])
# df1_final_cp = df1_final.copy()
#
# dummies = pd.get_dummies(df1_final_cp[['Event', 'Service']], dummy_na=True)
# dummies.drop(['Service_nan', 'Event_nan'], axis=1, inplace=True)
# dummies.columns = dummies.columns.str.split('_').str.get(1)
#
# df1_final_cpp = pd.concat([df1_final_cp, dummies], axis=1)
#
# exclude_cols = ['Event', 'Service']
# data_final = df1_final_cpp.loc[:, ~df1_final_cpp.columns.isin(exclude_cols)]
# print(data_final)
# print(data_final.columns)
#
# # Define the app and layout
#
# dash.register_page(__name__)
# layout = html.Div(children=[
#     html.H2(children='Customer EPO Analysis'),
#
#     dcc.Dropdown(
#         id='customer-dropdown',
#         options=[{'label': customer, 'value': customer} for customer in data_final['Customer_Name'].unique()],
#         value=data_final['Customer_Name'].unique()[0]
#     ),
#     # Create the bar chart
#     dcc.Graph(id='cpu-count-graph'),
#     dcc.Graph(id='filesystem-count-graph'),
#     dcc.Graph(id='HTTP-count-graph'),
#     dcc.Graph(id='Interface-count-graph'),
#     dcc.Graph(id='Memory-count-graph'),
#     dcc.Graph(id='Uptime-count-graph'),
#     dcc.Graph(id='? -> CRIT'),
#     dcc.Graph(id='? -> WARN'),
#     dcc.Graph(id='CRIT -> OK'),
#     dcc.Graph(id='CRIT -> UNKN'),
#     dcc.Graph(id='CRIT -> WARN'),
#     dcc.Graph(id='DOWN -> UP'),
#     dcc.Graph(id='OK -> CRIT'),
#     dcc.Graph(id='OK -> UNKN'),
#     dcc.Graph(id='OK -> WARN'),
#     dcc.Graph(id='UNKN -> CRIT'),
#     dcc.Graph(id='UNRE -> DOWN'),
#     dcc.Graph(id='UNRE -> UP'),
#     dcc.Graph(id='UP -> DOWN'),
#     dcc.Graph(id='WARN -> CRIT'),
#     dcc.Graph(id='WARN -> UNKN'),
#
# ])
#
#
# # Define the callback for updating the bar chart
# @callback(
#     dash.dependencies.Output('cpu-count-graph', 'figure'),
#     dash.dependencies.Output('filesystem-count-graph', 'figure'),
#     dash.dependencies.Output('HTTP-count-graph', 'figure'),
#     dash.dependencies.Output('Interface-count-graph', 'figure'),
#     dash.dependencies.Output('Memory-count-graph', 'figure'),
#     dash.dependencies.Output('Uptime-count-graph', 'figure'),
#     dash.dependencies.Output('? -> CRIT', 'figure'),
#     dash.dependencies.Output('? -> WARN', 'figure'),
#     dash.dependencies.Output('CRIT -> OK', 'figure'),
#     dash.dependencies.Output('CRIT -> UNKN', 'figure'),
#     dash.dependencies.Output('CRIT -> WARN', 'figure'),
#     dash.dependencies.Output('DOWN -> UP', 'figure'),
#     dash.dependencies.Output('OK -> CRIT', 'figure'),
#     dash.dependencies.Output('OK -> UNKN', 'figure'),
#     dash.dependencies.Output('OK -> WARN', 'figure'),
#     dash.dependencies.Output('UNKN -> CRIT', 'figure'),
#     dash.dependencies.Output('UNRE -> DOWN', 'figure'),
#     dash.dependencies.Output('UNRE -> UP', 'figure'),
#     dash.dependencies.Output('UP -> DOWN', 'figure'),
#     dash.dependencies.Output('WARN -> CRIT', 'figure'),
#     dash.dependencies.Output('WARN -> UNKN', 'figure'),
#
#     [dash.dependencies.Input('customer-dropdown', 'value')]
# )
# def update_graph(customer):
#     cpu = data_final[data_final['CPU'] != 0]
#     cpu = cpu[cpu['Customer_Name'] == customer]
#     top10_cpu = cpu.groupby('Host_Name')['CPU'].count().reset_index(name='CPU_Count')
#
#     filesystem = data_final[data_final['Filesystem'] != 0]
#     filesystem = filesystem[filesystem['Customer_Name'] == customer]
#     top10_filesystem = filesystem.groupby('Host_Name')['Filesystem'].count().reset_index(name='Filesystem_Count')
#
#     HTTP = data_final[data_final['HTTP'] != 0]
#     HTTP = HTTP[HTTP['Customer_Name'] == customer]
#     top10_HTTP = HTTP.groupby('Host_Name')['HTTP'].count().reset_index(name='HTTP_Count')
#
#     Interface = data_final[data_final['Interface'] != 0]
#     Interface = Interface[Interface['Customer_Name'] == customer]
#     top10_Interface = Interface.groupby('Host_Name')['Interface'].count().reset_index(name='Interface_Count')
#
#     Memory = data_final[data_final['Memory'] != 0]
#     Memory = Memory[Memory['Customer_Name'] == customer]
#     top10_Memory = Memory.groupby('Host_Name')['Memory'].count().reset_index(name='Memory_Count')
#
#     Uptime = data_final[data_final['Uptime'] != 0]
#     Uptime = Uptime[Uptime['Customer_Name'] == customer]
#     top10_Uptime = Uptime.groupby('Host_Name')['Uptime'].count().reset_index(name='Uptime_Count')
#
#
#     #? -> CRIT
#     CRIT = data_final[data_final['? -> CRIT'] != 0]
#     CRIT = CRIT[CRIT['Customer_Name'] == customer]
#     top10_CRIT = CRIT.groupby('Host_Name')['? -> CRIT'].count().reset_index(name='? -> CRIT')
#
#     WARN= data_final[data_final['? -> WARN'] != 0]
#     WARN = WARN[WARN['Customer_Name'] == customer]
#     top10_WARN = WARN.groupby('Host_Name')['? -> WARN'].count().reset_index(name='? -> WARN')
#
#
#
#     OK = data_final[data_final['CRIT -> OK'] != 0]
#     OK = OK[OK['Customer_Name'] == customer]
#     top10_OK= OK.groupby('Host_Name')['CRIT -> OK'].count().reset_index(name='CRIT -> OK')
#
#     UNKN = data_final[data_final['CRIT -> UNKN'] != 0]
#     UNKN = UNKN[UNKN['Customer_Name'] == customer]
#     top10_UNKN = UNKN.groupby('Host_Name')['CRIT -> UNKN'].count().reset_index(name='CRIT -> UNKN')
#
#     WARN1 = data_final[data_final['CRIT -> WARN'] != 0]
#     WARN1 = WARN1[WARN1['Customer_Name'] == customer]
#     top10_WARN1 = WARN1.groupby('Host_Name')['CRIT -> WARN'].count().reset_index(name='CRIT -> WARN')
#
#     UP = data_final[data_final['DOWN -> UP'] != 0]
#     UP = UP[UP['Customer_Name'] == customer]
#     top10_UP = UP.groupby('Host_Name')['DOWN -> UP'].count().reset_index(name='DOWN -> UP')
#
#     # OK -> CRIT
#     CRIT1 = data_final[data_final['OK -> CRIT'] != 0]
#     CRIT1 = CRIT1[CRIT1['Customer_Name'] == customer]
#     top10_CRIT1 = CRIT1.groupby('Host_Name')['OK -> CRIT'].count().reset_index(name='OK -> CRIT_Count')
#
#     UNKN1 = data_final[data_final['OK -> UNKN'] != 0]
#     UNKN1= UNKN1[UNKN1['Customer_Name'] == customer]
#     top10_UNKN1 = UNKN1.groupby('Host_Name')['OK -> UNKN'].count().reset_index(name='OK -> UNKN')
#
#     WARN2 = data_final[data_final['OK -> WARN'] != 0]
#     WARN2 = WARN2[WARN2['Customer_Name'] == customer]
#     top10_WARN2 = WARN2.groupby('Host_Name')['OK -> WARN'].count().reset_index(name='OK -> WARN')
#
#     CRIT2 = data_final[data_final['UNKN -> CRIT'] != 0]
#     CRIT2 = CRIT2[CRIT2['Customer_Name'] == customer]
#     top10_CRIT2 = CRIT2.groupby('Host_Name')['UNKN -> CRIT'].count().reset_index(name='UNKN -> CRIT')
#
#     DOWN = data_final[data_final['UNRE -> DOWN'] != 0]
#     DOWN = DOWN[DOWN['Customer_Name'] == customer]
#     top10_DOWN = DOWN.groupby('Host_Name')['UNRE -> DOWN'].count().reset_index(name='UNRE -> DOWN')
#
#     UP1 = data_final[data_final['UNRE -> UP'] != 0]
#     UP1 = UP1[UP1['Customer_Name'] == customer]
#     top10_UP1 = UP1.groupby('Host_Name')['UNRE -> UP'].count().reset_index(name='UNRE -> UP')
#
#     DOWN1 = data_final[data_final['UP -> DOWN'] != 0]
#     DOWN1 = DOWN1[DOWN1['Customer_Name'] == customer]
#     top10_DOWN1 = DOWN1.groupby('Host_Name')['UP -> DOWN'].count().reset_index(name='UP -> DOWN')
#
#     CRIT3 = data_final[data_final['WARN -> CRIT'] != 0]
#     CRIT3 = CRIT3[CRIT3['Customer_Name'] == customer]
#     top10_CRIT3 = CRIT3.groupby('Host_Name')['WARN -> CRIT'].count().reset_index(name='WARN -> CRIT')
#
#     UNKN2 = data_final[data_final['WARN -> UNKN'] != 0]
#     UNKN2 = UNKN2[UNKN2['Customer_Name'] == customer]
#     top10_UNKN2 = UNKN2.groupby('Host_Name')['WARN -> UNKN'].count().reset_index(name='WARN -> UNKN')
#
#
#
#     # Create the bar chart
#     fig_cpu = px.bar(top10_cpu, x='Host_Name', y='CPU_Count', title=f'CPU Count for {customer}')
#     fig_filesystem = px.bar(top10_filesystem, x='Host_Name', y='Filesystem_Count',
#                             title=f'Filesystem Count for {customer}')
#     fig_HTTP = px.bar(top10_HTTP, x='Host_Name', y='HTTP_Count', title=f'HTTP Count for {customer}')
#     fig_Interface = px.bar(top10_Interface, x='Host_Name', y='Interface_Count', title=f'Interface Count for {customer}')
#     fig_Memory = px.bar(top10_Memory, x='Host_Name', y='Memory_Count', title=f'Memory Count for {customer}')
#     fig_Uptime = px.bar(top10_Uptime, x='Host_Name', y='Uptime_Count', title=f'Uptime Count for {customer}')
#     fig_CRIT = px.bar(top10_CRIT, x='Host_Name', y='? -> CRIT', title=f'? -> CRIT Count for {customer}')
#     fig_WARN = px.bar(top10_WARN, x='Host_Name', y='? -> WARN', title=f'? -> WARN Count for {customer}')
#     fig_OK = px.bar(top10_OK, x='Host_Name', y='CRIT -> OK', title=f'CRIT -> OK Count for {customer}')
#     fig_UNKN = px.bar(top10_UNKN, x='Host_Name', y='CRIT -> UNKN', title=f'CRIT -> UNKN Count for {customer}')
#     fig_WARN1 = px.bar(top10_WARN1, x='Host_Name', y='CRIT -> WARN', title=f'CRIT -> WARN Count for {customer}')
#     fig_UP = px.bar(top10_UP, x='Host_Name', y='DOWN -> UP', title=f'DOWN -> UP Count for {customer}')
#     fig_CRIT1 = px.bar(top10_CRIT1, x='Host_Name', y='OK -> CRIT_Count', title=f'OK -> CRIT Count for {customer}')
#     fig_UNKN1 = px.bar(top10_UNKN1, x='Host_Name', y='OK -> UNKN', title=f'OK -> UNKN Count for {customer}')
#     fig_WARN2 = px.bar(top10_WARN2, x='Host_Name', y='OK -> WARN', title=f'OK -> WARN Count for {customer}')
#     fig_CRIT2 = px.bar(top10_CRIT2, x='Host_Name', y='UNKN -> CRIT', title=f'UNKN -> CRIT Count for {customer}')
#     fig_DOWN = px.bar(top10_DOWN, x='Host_Name', y='UNRE -> DOWN', title=f'UNRE -> DOWN Count for {customer}')
#
#     fig_UP1 = px.bar(top10_UP1, x='Host_Name', y='UNRE -> UP', title=f'UNRE -> UP Count for {customer}')
#
#     fig_DOWN1 = px.bar(top10_DOWN1, x='Host_Name', y='UP -> DOWN', title=f'UP -> DOWN Count for {customer}')
#     fig_CRIT3 = px.bar(top10_CRIT3, x='Host_Name', y='WARN -> CRIT', title=f'WARN -> CRIT Count for {customer}')
#     fig_UNKN2 = px.bar(top10_UNKN2, x='Host_Name', y='WARN -> UNKN', title=f'WARN -> UNKN Count for {customer}')
#
#
#     return fig_cpu, fig_filesystem, fig_HTTP, fig_Interface, fig_Memory, fig_Uptime ,fig_CRIT,fig_WARN,fig_OK,fig_UNKN,fig_WARN1,fig_UP,fig_CRIT1,fig_UNKN1,fig_WARN2,fig_CRIT2,fig_DOWN,fig_UP1,fig_DOWN1,fig_CRIT3,fig_UNKN2
