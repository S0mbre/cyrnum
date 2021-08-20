# -*- coding: utf-8 -*-
import sys, os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app, server
from cyrnum import Cyrnum, MAXNUMBER

DEBUG = True

#========================== LAYOUTS =========================#

input_number_form = dbc.FormGroup(
    [
        dbc.Label('Число', html_for='input_number', width=2),
        dbc.Col(
            dbc.Input(id='input_number', type='number', placeholder=f'Введите число (от 1 до {MAXNUMBER})', min=1, max=MAXNUMBER, step=1, style={'width': '50%'}),
            width=10,
        )
    ],
    row=True
)

bgcolor_form = dbc.FormGroup(
    [
        dbc.Label('Цвет фона', html_for='bgcolor', width=2),
        dbc.Col(
            dbc.Input(id='bgcolor', type='color', value='#ffffff', style={'width': '50%'}),
            width=10,
        )
    ],
    row=True
)

fgcolor_form = dbc.FormGroup(
    [
        dbc.Label('Цвет текста', html_for='fgcolor', width=2),
        dbc.Col(
            dbc.Input(id='fgcolor', type='color', value='#000000', style={'width': '50%'}),
            width=10,
        )
    ],
    row=True
)

size_form = dbc.FormGroup(
    [
        dbc.Label('Размер текста', html_for='sizerange', width=2),
        dbc.Col(
            dcc.Slider(id='sizerange', min=16, max=1024, value=256, step=16),
            width=10,
        )
    ],
    row=True
)

form_all = html.Div(dbc.Form(id='form_all', children=[input_number_form, bgcolor_form, fgcolor_form, size_form]), style={'margin-left': '20%', 'margin-right': '20%'})

#======================== MAIN LAYOUT ========================#

app.layout = html.Div(
    [
        form_all    
    ], style={'margin': '10%'})

#======================== CALLBACKS ========================#



#-----------------------------------------------------------------------------------#

if __name__ == '__main__':
    app.run_server(host='localhost', debug=DEBUG)
    #app.run_server(debug=DEBUG)