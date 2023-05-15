# import plotly.graph_objects as go
# import pandas as pd
# import numpy as np
# import pandas as pd
# import mysql.connector as sql
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import plotly.express as px
# from dash import callback
#
# import dash_table
# from dash_table.Format import Format
# import plotly.express as px
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
#     dcc.Graph(id='Uptime-count-graph'),
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
#     dcc.Graph(id='Memory-count-graph'),
#     dcc.Graph(id='crit-graph'),
#
#     html.Div(id='hovered-data-table', style={'margin-top': '20px', 'font-family': 'Arial, sans-serif'}),
# ])
#
#
# # Define the callback for updating the bar chart
# @callback(
#     [dash.dependencies.Output('cpu-count-graph', 'figure'),
#      dash.dependencies.Output('filesystem-count-graph', 'figure'),
#      dash.dependencies.Output('HTTP-count-graph', 'figure'),
#      dash.dependencies.Output('Interface-count-graph', 'figure'),
#      dash.dependencies.Output('Uptime-count-graph', 'figure'),
#      dash.dependencies.Output('? -> WARN', 'figure'),
#      dash.dependencies.Output('CRIT -> OK', 'figure'),
#      dash.dependencies.Output('CRIT -> UNKN', 'figure'),
#      dash.dependencies.Output('CRIT -> WARN', 'figure'),
#      dash.dependencies.Output('DOWN -> UP', 'figure'),
#      dash.dependencies.Output('OK -> CRIT', 'figure'),
#      dash.dependencies.Output('OK -> UNKN', 'figure'),
#      dash.dependencies.Output('OK -> WARN', 'figure'),
#      dash.dependencies.Output('UNKN -> CRIT', 'figure'),
#      dash.dependencies.Output('UNRE -> DOWN', 'figure'),
#      dash.dependencies.Output('UNRE -> UP', 'figure'),
#      dash.dependencies.Output('UP -> DOWN', 'figure'),
#      dash.dependencies.Output('WARN -> CRIT', 'figure'),
#      dash.dependencies.Output('WARN -> UNKN', 'figure'),
#
#      dash.dependencies.Output('Memory-count-graph', 'figure'),
#      dash.dependencies.Output('crit-graph', 'figure'),
#      dash.dependencies.Output('hovered-data-table', 'children')],  # Update the property to 'children'
#     [dash.dependencies.Input('customer-dropdown', 'value'),
#      dash.dependencies.Input('Memory-count-graph', 'clickData'),
#      dash.dependencies.Input('crit-graph', 'clickData')]
# )
# def update_graph(customer, memory_click_data, crit_click_data):
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
#
#     Uptime = data_final[data_final['Uptime'] != 0]
#     Uptime = Uptime[Uptime['Customer_Name'] == customer]
#     top10_Uptime = Uptime.groupby('Host_Name')['Uptime'].count().reset_index(name='Uptime_Count')
#
#     WARN= data_final[data_final['? -> WARN'] != 0]
#     WARN = WARN[WARN['Customer_Name'] == customer]
#     top10_WARN = WARN.groupby('Host_Name')['? -> WARN'].count().reset_index(name='? -> WARN')
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
#     UNKN1 = UNKN1[UNKN1['Customer_Name'] == customer]
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
#     Memory = data_final[data_final['Memory'] != 0]
#     Memory = Memory[Memory['Customer_Name'] == customer]
#     top10_Memory = Memory.groupby('Host_Name')['Memory'].count().reset_index(name='Memory_Count')
#
#     # Filter the data for the selected customer and non-zero ? -> CRIT
#     CRIT = data_final[data_final['? -> CRIT'] != 0]
#     CRIT = CRIT[CRIT['Customer_Name'] == customer]
#     top10_CRIT = CRIT.groupby('Host_Name')['? -> CRIT'].count().reset_index(name='? -> CRIT')
#
#     # cpu
#     create_times_cpu = cpu.groupby('Host_Name')['Create_Time'].apply(list)
#     time_series_strings_cpu = create_times_cpu.apply(
#         lambda times: '<br>'.join(f'Create Time: {time}' for time in times))
#
#
#
#     # Prepare the Create_Time values for each bar in Filesystem graph
#     create_times_filesystem = filesystem.groupby('Host_Name')['Create_Time'].apply(list)
#     # Format the time series as a string for each bar in Filesystem graph
#     time_series_strings_filesystem = create_times_filesystem.apply(
#         lambda times: '<br>'.join(f'Create Time: {time}' for time in times))
#
#     #http
#     create_times_http = HTTP.groupby('Host_Name')['Create_Time'].apply(list)
#     time_series_strings_http = create_times_http.apply(
#         lambda times: '<br>'.join(f'Create Time: {time}' for time in times))
#
#     #interface
#     create_times_interface = Interface.groupby('Host_Name')['Create_Time'].apply(list)
#     time_series_strings_interface = create_times_interface.apply(
#         lambda times: '<br>'.join(f'Create Time: {time}' for time in times))
#
#     # warn
#     create_times_WARN = WARN.groupby('Host_Name')['Create_Time'].apply(list)
#     time_series_strings_WARN = create_times_WARN.apply(
#         lambda times: '<br>'.join(f'Create Time: {time}' for time in times))
#
#     #ok
#     create_times_OK = OK.groupby('Host_Name')['Create_Time'].apply(list)
#     time_series_strings_OK = create_times_OK.apply(
#         lambda times: '<br>'.join(f'Create Time: {time}' for time in times))
#
#     #unkn
#     create_times_UNKN = UNKN.groupby('Host_Name')['Create_Time'].apply(list)
#     time_series_strings_UNKN = create_times_UNKN.apply(
#         lambda times: '<br>'.join(f'Create Time: {time}' for time in times))
#
#     #warn1
#     create_times_WARN1 = WARN1.groupby('Host_Name')['Create_Time'].apply(list)
#     time_series_strings_WARN1 = create_times_WARN1.apply(
#         lambda times: '<br>'.join(f'Create Time: {time}' for time in times))
#
#     #up
#     create_times_UP = UP.groupby('Host_Name')['Create_Time'].apply(list)
#     time_series_strings_UP = create_times_UP.apply(
#         lambda times: '<br>'.join(f'Create Time: {time}' for time in times))
#
#     #crit1
#     create_times_CRIT1 = CRIT1.groupby('Host_Name')['Create_Time'].apply(list)
#     time_series_strings_CRIT1 = create_times_CRIT1.apply(
#         lambda times: '<br>'.join(f'Create Time: {time}' for time in times))
#
#     #unkn1
#     create_times_UNKN1 = UNKN1.groupby('Host_Name')['Create_Time'].apply(list)
#     time_series_strings_UNKN1 = create_times_UNKN1.apply(
#         lambda times: '<br>'.join(f'Create Time: {time}' for time in times))
#     #warn2
#     create_times_WARN2 = WARN2.groupby('Host_Name')['Create_Time'].apply(list)
#     time_series_strings_WARN2 = create_times_WARN2.apply(
#         lambda times: '<br>'.join(f'Create Time: {time}' for time in times))
#    #crit2
#     create_times_CRIT2 = CRIT2.groupby('Host_Name')['Create_Time'].apply(list)
#     time_series_strings_CRIT2 = create_times_CRIT2.apply(
#         lambda times: '<br>'.join(f'Create Time: {time}' for time in times))
#     #down
#     create_times_DOWN = DOWN.groupby('Host_Name')['Create_Time'].apply(list)
#     time_series_strings_DOWN = create_times_DOWN.apply(
#         lambda times: '<br>'.join(f'Create Time: {time}' for time in times))
#
#     #up1
#     create_times_UP1 = UP1.groupby('Host_Name')['Create_Time'].apply(list)
#     time_series_strings_UP1 = create_times_UP1.apply(
#         lambda times: '<br>'.join(f'Create Time: {time}' for time in times))
#
#     #down1
#     create_times_DOWN1 = DOWN1.groupby('Host_Name')['Create_Time'].apply(list)
#     time_series_strings_DOWN1 = create_times_DOWN1.apply(
#         lambda times: '<br>'.join(f'Create Time: {time}' for time in times))
#     #crit3
#     create_times_CRIT3 = CRIT3.groupby('Host_Name')['Create_Time'].apply(list)
#     time_series_strings_CRIT3 = create_times_CRIT3.apply(
#         lambda times: '<br>'.join(f'Create Time: {time}' for time in times))
#     #unkn2
#     create_times_UNKN2 = UNKN2.groupby('Host_Name')['Create_Time'].apply(list)
#     time_series_strings_UNKN2 = create_times_UNKN2.apply(
#         lambda times: '<br>'.join(f'Create Time: {time}' for time in times))
#
#     # Prepare the Create_Time values for each bar in Uptime graph
#     create_times_uptime = Uptime.groupby('Host_Name')['Create_Time'].apply(list)
#     # Format the time series as a string for each bar in Uptime graph
#     time_series_strings_uptime = create_times_uptime.apply(
#         lambda times: '<br>'.join(f'Create Time: {time}' for time in times))
#
#     # Prepare the Create_Time values for each bar in Memory graph
#     create_times_memory = Memory.groupby('Host_Name')['Create_Time'].apply(list)
#     # Format the time series as a string for each bar in Memory graph
#     time_series_strings_memory = create_times_memory.apply(lambda times: '<br>'.join(f'Create Time: {time}' for time in times))
#
#     # Create the bar chart figure for Uptime
#     fig_cpu = go.Figure(data=[
#         go.Bar(
#             x=top10_cpu['Host_Name'],
#             y=top10_cpu['CPU_Count'],
#             text=top10_cpu['CPU_Count'],
#             customdata=time_series_strings_cpu,
#             hovertemplate='<b>CPU Count</b>: %{y}<br>' +
#                           '<b>Count:</b> %{text}<br><br>' +
#                           '<b>Time Series:</b><br>' +
#                           '%{customdata}',
#         )
#     ])
#
#     fig_cpu.update_layout(
#         xaxis={'title': 'Host Name'},
#         yaxis={'title': 'CPU Count'},
#         title=f'CPU Count for {customer}',
#         showlegend=False
#     )
#
#     fig_filesystem = go.Figure(data=[
#         go.Bar(
#             x=top10_filesystem['Host_Name'],
#             y=top10_filesystem['Filesystem_Count'],
#             text=top10_filesystem['Filesystem_Count'],
#             customdata=time_series_strings_filesystem,  # Update with correct variable name
#             hovertemplate='<b>Filesystem Count</b>: %{y}<br>' +
#                           '<b>Count:</b> %{text}<br><br>' +
#                           '<b>Time Series:</b><br>' +
#                           '%{customdata}',
#         )
#     ])
#
#     fig_filesystem.update_layout(
#         xaxis={'title': 'Host Name'},
#         yaxis={'title': 'Filesystem Count'},
#         title=f'Filesystem Count for {customer}',
#         showlegend=False
#     )
#
#     fig_HTTP = go.Figure(data=[
#         go.Bar(
#             x=top10_HTTP['Host_Name'],
#             y=top10_HTTP['HTTP_Count'],
#             text=top10_HTTP['HTTP_Count'],
#             customdata=time_series_strings_http,
#             hovertemplate='<b>HTTP Count</b>: %{y}<br>' +
#                           '<b>Count:</b> %{text}<br><br>' +
#                           '<b>Time Series:</b><br>' +
#                           '%{customdata}',
#         )
#     ])
#
#     fig_HTTP.update_layout(
#         xaxis={'title': 'Host Name'},
#         yaxis={'title': 'HTTP Count'},
#         title=f'HTTP Count for {customer}',
#         showlegend=False
#     )
#     fig_Interface = go.Figure(data=[
#         go.Bar(
#             x=top10_Interface['Host_Name'],
#             y=top10_Interface['Interface_Count'],
#             text=top10_Interface['Interface_Count'],
#             customdata=time_series_strings_interface,
#             hovertemplate='<b>Interface Count</b>: %{y}<br>' +
#                           '<b>Count:</b> %{text}<br><br>' +
#                           '<b>Time Series:</b><br>' +
#                           '%{customdata}',
#         )
#     ])
#
#     fig_Interface.update_layout(
#         xaxis={'title': 'Host Name'},
#         yaxis={'title': 'Interface Count'},
#         title=f'Interface Count for {customer}',
#         showlegend=False
#     )
#
#
#     # Create the bar chart figure for Memory
#     fig_Uptime = go.Figure(data=[
#         go.Bar(
#             x=top10_Uptime['Host_Name'],
#             y=top10_Uptime['Uptime_Count'],
#             text=top10_Uptime['Uptime_Count'],
#             customdata=time_series_strings_uptime,  # Add customdata with time series strings
#             hovertemplate='<b>Uptime Count</b>: %{y}<br>' +
#                           '<b>Count:</b> %{text}<br><br>' +
#                           '<b>Time Series:</b><br>' +
#                           '%{customdata}',
#         )
#     ])
#
#     fig_Uptime.update_layout(
#         xaxis={'title': 'Host Name'},
#         yaxis={'title': 'Uptime Count'},
#         title=f'Uptime Count for {customer}',
#         showlegend=False
#     )
#     fig_WARN = go.Figure(data=[
#         go.Bar(
#             x=top10_WARN['Host_Name'],
#             y=top10_WARN['? -> WARN'],
#             text=top10_WARN['? -> WARN'],
#             customdata=time_series_strings_WARN,
#             hovertemplate='<b>? -> WARN Count</b>: %{y}<br>' +
#                           '<b>Count:</b> %{text}<br><br>' +
#                           '<b>Time Series:</b><br>' +
#                           '%{customdata}',
#         )
#     ])
#
#     fig_WARN.update_layout(
#         xaxis={'title': 'Host Name'},
#         yaxis={'title': '? -> WARN Count'},
#         title=f'? -> WARN Count for {customer}',
#         showlegend=False
#     )
#     fig_OK = go.Figure(data=[
#         go.Bar(
#             x=top10_OK['Host_Name'],
#             y=top10_OK['CRIT -> OK'],
#             text=top10_OK['CRIT -> OK'],
#             customdata=time_series_strings_OK,
#             hovertemplate='<b>CRIT -> OK Count</b>: %{y}<br>' +
#                           '<b>Count:</b> %{text}<br><br>' +
#                           '<b>Time Series:</b><br>' +
#                           '%{customdata}',
#         )
#     ])
#
#     fig_OK.update_layout(
#         xaxis={'title': 'Host Name'},
#         yaxis={'title': 'CRIT -> OK Count'},
#         title=f'CRIT -> OK Count for {customer}',
#         showlegend=False
#     )
#     fig_UNKN = go.Figure(data=[
#         go.Bar(
#             x=top10_UNKN['Host_Name'],
#             y=top10_UNKN['CRIT -> UNKN'],
#             text=top10_UNKN['CRIT -> UNKN'],
#             customdata=time_series_strings_UNKN,
#             hovertemplate='<b>CRIT -> UNKN Count</b>: %{y}<br>' +
#                           '<b>Count:</b> %{text}<br><br>' +
#                           '<b>Time Series:</b><br>' +
#                           '%{customdata}',
#         )
#     ])
#
#     fig_UNKN.update_layout(
#         xaxis={'title': 'Host Name'},
#         yaxis={'title': 'CRIT -> UNKN Count'},
#         title=f'CRIT -> UNKN Count for {customer}',
#         showlegend=False
#     )
#     fig_WARN1 = go.Figure(data=[
#         go.Bar(
#             x=top10_WARN1['Host_Name'],
#             y=top10_WARN1['CRIT -> WARN'],
#             text=top10_WARN1['CRIT -> WARN'],
#             customdata=time_series_strings_WARN1,
#             hovertemplate='<b>CRIT -> WARN Count</b>: %{y}<br>' +
#                           '<b>Count:</b> %{text}<br><br>' +
#                           '<b>Time Series:</b><br>' +
#                           '%{customdata}',
#         )
#     ])
#
#     fig_WARN1.update_layout(
#         xaxis={'title': 'Host Name'},
#         yaxis={'title': 'CRIT -> WARN Count'},
#         title=f'CRIT -> WARN Count for {customer}',
#         showlegend=False
#     )
#     fig_UP = go.Figure(data=[
#         go.Bar(
#             x=top10_UP['Host_Name'],
#             y=top10_UP['DOWN -> UP'],
#             text=top10_UP['DOWN -> UP'],
#             customdata=time_series_strings_UP,
#             hovertemplate='<b>DOWN -> UP Count</b>: %{y}<br>' +
#                           '<b>Count:</b> %{text}<br><br>' +
#                           '<b>Time Series:</b><br>' +
#                           '%{customdata}',
#         )
#     ])
#
#     fig_UP.update_layout(
#         xaxis={'title': 'Host Name'},
#         yaxis={'title': 'DOWN -> UP Count'},
#         title=f'DOWN -> UP Count for {customer}',
#         showlegend=False
#     )
#     fig_CRIT1 = go.Figure(data=[
#         go.Bar(
#             x=top10_CRIT1['Host_Name'],
#             y=top10_CRIT1['OK -> CRIT_Count'],
#             text=top10_CRIT1['OK -> CRIT_Count'],
#             customdata=time_series_strings_CRIT1,
#             hovertemplate='<b>OK -> CRIT Count</b>: %{y}<br>' +
#                           '<b>Count:</b> %{text}<br><br>' +
#                           '<b>Time Series:</b><br>' +
#                           '%{customdata}',
#         )
#     ])
#
#     fig_CRIT1.update_layout(
#         xaxis={'title': 'Host Name'},
#         yaxis={'title': 'OK -> CRIT Count'},
#         title=f'OK -> CRIT Count for {customer}',
#         showlegend=False
#     )
#
#     fig_UNKN1 = go.Figure(data=[
#         go.Bar(
#             x=top10_UNKN1['Host_Name'],
#             y=top10_UNKN1['OK -> UNKN'],
#             text=top10_UNKN1['OK -> UNKN'],
#             customdata=time_series_strings_UNKN1,
#             hovertemplate='<b>OK -> UNKN Count</b>: %{y}<br>' +
#                           '<b>Count:</b> %{text}<br><br>' +
#                           '<b>Time Series:</b><br>' +
#                           '%{customdata}',
#         )
#     ])
#
#     fig_UNKN1.update_layout(
#         xaxis={'title': 'Host Name'},
#         yaxis={'title': 'OK -> UNKN Count'},
#         title=f'OK -> UNKN Count for {customer}',
#         showlegend=False
#     )
#     fig_WARN2 = go.Figure(data=[
#         go.Bar(
#             x=top10_WARN2['Host_Name'],
#             y=top10_WARN2['OK -> WARN'],
#             text=top10_WARN2['OK -> WARN'],
#             customdata=time_series_strings_WARN2,
#             hovertemplate='<b>OK -> WARN Count</b>: %{y}<br>' +
#                           '<b>Count:</b> %{text}<br><br>' +
#                           '<b>Time Series:</b><br>' +
#                           '%{customdata}',
#         )
#     ])
#
#     fig_WARN2.update_layout(
#         xaxis={'title': 'Host Name'},
#         yaxis={'title': 'OK -> WARN Count'},
#         title=f'OK -> WARN Count for {customer}',
#         showlegend=False
#     )
#     fig_CRIT2 = go.Figure(data=[
#         go.Bar(
#             x=top10_CRIT2['Host_Name'],
#             y=top10_CRIT2['UNKN -> CRIT'],
#             text=top10_CRIT2['UNKN -> CRIT'],
#             customdata=time_series_strings_CRIT2,
#             hovertemplate='<b>UNKN -> CRIT Count</b>: %{y}<br>' +
#                           '<b>Count:</b> %{text}<br><br>' +
#                           '<b>Time Series:</b><br>' +
#                           '%{customdata}',
#         )
#     ])
#
#     fig_CRIT2.update_layout(
#         xaxis={'title': 'Host Name'},
#         yaxis={'title': 'UNKN -> CRIT Count'},
#         title=f'UNKN -> CRIT Count for {customer}',
#         showlegend=False
#     )
#     fig_DOWN = go.Figure(data=[
#         go.Bar(
#             x=top10_DOWN['Host_Name'],
#             y=top10_DOWN['UNRE -> DOWN'],
#             text=top10_DOWN['UNRE -> DOWN'],
#             customdata=time_series_strings_DOWN,
#             hovertemplate='<b>UNRE -> DOWN Count</b>: %{y}<br>' +
#                           '<b>Count:</b> %{text}<br><br>' +
#                           '<b>Time Series:</b><br>' +
#                           '%{customdata}',
#         )
#     ])
#
#     fig_DOWN.update_layout(
#         xaxis={'title': 'Host Name'},
#         yaxis={'title': 'UNRE -> DOWN Count'},
#         title=f'UNRE -> DOWN Count for {customer}',
#         showlegend=False
#     )
#
#     fig_UP1 = go.Figure(data=[
#         go.Bar(
#             x=top10_UP1['Host_Name'],
#             y=top10_UP1['UNRE -> UP'],
#             text=top10_UP1['UNRE -> UP'],
#             customdata=time_series_strings_UP1,
#             hovertemplate='<b>UNRE -> UP Count</b>: %{y}<br>' +
#                           '<b>Count:</b> %{text}<br><br>' +
#                           '<b>Time Series:</b><br>' +
#                           '%{customdata}',
#         )
#     ])
#
#     fig_UP1.update_layout(
#         xaxis={'title': 'Host Name'},
#         yaxis={'title': 'UNRE -> UP Count'},
#         title=f'UNRE -> UP Count for {customer}',
#         showlegend=False
#     )
# #more than 50
#     fig_DOWN1 = go.Figure(data=[
#         go.Bar(
#             x=top10_DOWN1['Host_Name'],
#             y=top10_DOWN1['UP -> DOWN'],
#             text=top10_DOWN1['UP -> DOWN'],
#             customdata=time_series_strings_DOWN1,
#             hovertemplate='<b>UP -> DOWN Count</b>: %{y}<br>' +
#                           '<b>Count:</b> %{text}<br><br>' +
#                           '<b>Time Series:</b><br>' +
#                           '%{customdata}',
#         )
#     ])
#
#     fig_DOWN1.update_layout(
#         xaxis={'title': 'Host Name'},
#         yaxis={'title': 'UP -> DOWN Count'},
#         title=f'UP -> DOWN Count for {customer}',
#         showlegend=False
#     )
#
#     fig_CRIT3 = go.Figure(data=[
#         go.Bar(
#             x=top10_CRIT3['Host_Name'],
#             y=top10_CRIT3['WARN -> CRIT'],
#             text=top10_CRIT3['WARN -> CRIT'],
#             customdata=time_series_strings_CRIT3,
#             hovertemplate='<b>WARN -> CRIT Count</b>: %{y}<br>' +
#                           '<b>Count:</b> %{text}<br><br>' +
#                           '<b>Time Series:</b><br>' +
#                           '%{customdata}',
#         )
#     ])
#
#     fig_CRIT3.update_layout(
#         xaxis={'title': 'Host Name'},
#         yaxis={'title': 'WARN -> CRIT Count'},
#         title=f'WARN -> CRIT Count for {customer}',
#         showlegend=False
#     )
#
#     fig_UNKN2 = go.Figure(data=[
#         go.Bar(
#             x=top10_UNKN2['Host_Name'],
#             y=top10_UNKN2['WARN -> UNKN'],
#             text=top10_UNKN2['WARN -> UNKN'],
#             customdata=time_series_strings_UNKN2,
#             hovertemplate='<b>WARN -> UNKN Count</b>: %{y}<br>' +
#                           '<b>Count:</b> %{text}<br><br>' +
#                           '<b>Time Series:</b><br>' +
#                           '%{customdata}',
#         )
#     ])
#
#     fig_UNKN2.update_layout(
#         xaxis={'title': 'Host Name'},
#         yaxis={'title': 'WARN -> UNKN Count'},
#         title=f'WARN -> UNKN Count for {customer}',
#         showlegend=False
#     )
#
#     # Create the bar chart figure for Memory
#     fig_Memory = go.Figure(data=[
#         go.Bar(
#             x=top10_Memory['Host_Name'],
#             y=top10_Memory['Memory_Count'],
#             text=top10_Memory['Memory_Count'],
#             customdata=time_series_strings_memory,  # Add customdata with time series strings
#             hovertemplate='<b>Memory Count</b>: %{y}<br>' +
#                           '<b>Count:</b> %{text}<br><br>' +
#                           '<b>Time Series:</b><br>' +
#                           '%{customdata}',
#         )
#     ])
#
#     fig_Memory.update_layout(
#         xaxis={'title': 'Host Name'},
#         yaxis={'title': 'Memory Count'},
#         title=f'Memory Count for {customer}',
#         showlegend=False
#     )
#
#     # Prepare the Create_Time values for each bar in ? -> CRIT graph
#     create_times_crit = CRIT.groupby('Host_Name')['Create_Time'].apply(list)
#     # Format the time series as a string for each bar in ? -> CRIT graph
#     time_series_strings_crit = create_times_crit.apply(lambda times: '<br>'.join(f'Create Time: {time}' for time in times))
#
#     # Create the bar chart figure for ? -> CRIT
#     fig_CRIT = go.Figure(data=[
#         go.Bar(
#             x=top10_CRIT['Host_Name'],
#             y=top10_CRIT['? -> CRIT'],
#             text=top10_CRIT['? -> CRIT'],
#             customdata=time_series_strings_crit,  # Use the time series strings specific to ? -> CRIT graph
#             hovertemplate='<b>? -> CRIT Count</b>: %{y}<br>' +
#                           '<b>Count:</b> %{text}<br><br>' +
#                           '<b>Time Series:</b><br>' +
#                           '%{customdata}',
#         )
#     ])
#
#     fig_CRIT.update_layout(
#         xaxis={'title': 'Host Name'},
#         yaxis={'title': '? -> CRIT Count'},
#         title=f'? -> CRIT Count for {customer}',
#         showlegend=False
#     )
#
#     # Determine the trigger of the callback
#     trigger = dash.callback_context.triggered[0]['prop_id']
#
#     # Update the hovered data table based on the trigger
#     if 'Memory-count-graph' in trigger:
#         click_data = memory_click_data
#         time_series_strings = time_series_strings_memory
#     elif 'crit-graph' in trigger:
#         click_data = crit_click_data
#         time_series_strings = time_series_strings_crit
#     else:
#         click_data = None
#         time_series_strings = []
#
#     if click_data is not None:
#         point_data = click_data['points'][0]
#         host_name = point_data['x']
#         time_series = point_data['customdata']
#         if time_series:
#             time_series_list = time_series.split('<br>')
#             # Add host name and customer name to the data
#             host_name_div = html.Div(f"Host Name: {host_name}", className='host-name')
#             customer_name_div = html.Div(f"Customer: {customer}", className='customer-name')
#             data = [html.Div(time, className='time-series') for time in
#                     time_series_list]  # Create Div elements for each time series
#             data.insert(0, host_name_div)  # Insert the host name at the beginning
#             data.insert(1, customer_name_div)  # Insert the customer name after the host name
#             return fig_cpu,fig_filesystem,fig_HTTP,fig_Interface,fig_Uptime, fig_WARN,fig_OK,fig_UNKN ,fig_WARN1,fig_UP,fig_CRIT1,fig_UNKN1,fig_WARN2,fig_CRIT2,fig_DOWN,fig_UP1,fig_DOWN1,fig_CRIT3,fig_UNKN2,fig_Memory, fig_CRIT, data
#         else:
#             return fig_cpu,fig_filesystem,fig_HTTP,fig_Interface,fig_Uptime,fig_WARN,fig_OK,fig_UNKN ,fig_WARN1,fig_UP,fig_CRIT1,fig_UNKN1,fig_WARN2fig_CRIT2,fig_DOWN,fig_UP1,fig_DOWN1,fig_CRIT3,fig_UNKN2,fig_Memory, fig_CRIT, []
#
#     return fig_cpu,fig_filesystem,fig_HTTP,fig_Interface,fig_Uptime,fig_WARN,fig_OK,fig_UNKN ,fig_WARN1,fig_UP,fig_CRIT1,fig_UNKN1,fig_WARN2,fig_CRIT2,fig_DOWN,fig_UP1,fig_DOWN1,fig_CRIT3,fig_UNKN2, fig_Memory,fig_CRIT, []
#
