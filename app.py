# -*- coding: utf-8 -*-
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components.themes import DARKLY
from whitenoise import WhiteNoise

meta_tags = [{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
ext_css = [dbc.themes.DARKLY] # https://bootswatch.com/darkly/

app = dash.Dash(__name__, suppress_callback_exceptions=True, meta_tags=meta_tags, external_stylesheets=ext_css) 
app.title = 'CYRNUMS'
app.config.suppress_callback_exceptions = True

server = app.server
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static')