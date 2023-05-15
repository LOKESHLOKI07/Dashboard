import dash
import dash_bootstrap_components as dbc
from dash import Dash, html

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Dashboard", href="/dashboard")),
            dbc.NavItem(dbc.NavLink("Analytics", href="/analytics")),
        ],
        brand="Monitoring Insights",
        brand_href="#",
        color="primary",
        dark=True,
    ),
    dash.page_container
])

if __name__ == '__main__':
    app.run_server(host='192.168.100.213', debug=True)
