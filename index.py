# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app, server
from cyrnum import Cyrnum, MAXNUMBER
import utils

DEBUG = False

#========================== LAYOUTS =========================#

headerimg = html.Div(html.Img(id='img_header', src='static/titlecn.png'), 
                    style={'text-align': 'center', 'margin': '2%', 'white-space': 'nowrap'})

input_number_form = dbc.FormGroup(
    [
        dbc.Label('Число', html_for='input_number', width=2),
        dbc.Col(
            dbc.Input(id='input_number', type='number', placeholder=f'Введите число (от 1 до {MAXNUMBER})', min=1, max=MAXNUMBER, step=1, style={'width': '35%'}),
            width=10
        )
    ],
    row=True
)

bgcolor_form = dbc.FormGroup(
    [
        dbc.Label('Цвет фона', html_for='bgcolor', width=2),
        dbc.Col(
            dbc.Input(id='bgcolor', type='color', value='#ffffff', style={'width': '35%'}),
            width=10
        )
    ],
    row=True
)

fgcolor_form = dbc.FormGroup(
    [
        dbc.Label('Цвет текста', html_for='fgcolor', width=2),
        dbc.Col(
            dbc.Input(id='fgcolor', type='color', value='#000000', style={'width': '35%'}),
            width=10
        )
    ],
    row=True
)

size_form = dbc.FormGroup(
    [
        dbc.Label('Размер текста', html_for='sizerange', width=2),
        dbc.Col(
            dcc.Slider(id='sizerange', min=16, max=1024, value=256, step=16, marks={i: str(i) for i in range(32, 1025, 32)}),
            width=10
        )
    ],
    row=True
)

options_form = dbc.FormGroup(
    [
        dbc.Label('Опции', html_for='options_checklist', width=2),
        dbc.Col(
            dbc.Checklist(
                id='options_checklist',
                options=[
                    {'label': 'Нет фона', 'value': 0},
                    {'label': 'Титло', 'value': 1},
                    {'label': 'Простой Леодр', 'value': 2},
                    {'label': 'Простая Колода', 'value': 3},
                ],
                value=[1]),
            width=10
        )
    ],
    row=True
)

form_all = html.Div(dbc.Form(id='form_all', children=[input_number_form, bgcolor_form, fgcolor_form, size_form, options_form]), style={'margin-left': '10%', 'margin-right': '10%'})

img_card = html.Div(
    dcc.Loading(html.Img(id='img_number', src='', style={'width': '100%', 'height': 'auto', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'})), 
    style={'text-align': 'center', 'margin': '5%', 'display': 'inline-block', 'white-space': 'nowrap'})

#======================== MAIN LAYOUT ========================#

app.layout = html.Div(
    [
        headerimg,
        form_all,
        img_card  
    ], style={'margin-bottom': '5%'})

#======================== CALLBACKS ========================#

def get_pic_data(number, bgcolor, fgcolor, fontsize, transparent, titlo, simple_leodr, simple_koloda):
    try:
        cn = Cyrnum(fontsize, bgcolor, fgcolor, transparent, koloda_simple=simple_koloda, leodr_simple=simple_leodr, titlo=titlo, draw_exceptions=True)
        img = cn[number]
        tempfile = utils.tmpfile(ext='png')
        img.save(tempfile)
        return utils.b64img_encode(tempfile, 'png')

    except:
        utils.print_traceback()
        return ''

@app.callback(
    Output('img_number', 'src'),    
    Input('input_number', 'value'),
    Input('bgcolor', 'value'),
    Input('fgcolor', 'value'),
    Input('sizerange', 'value'),
    Input('options_checklist', 'value'),
    State('input_number', 'value'),
    State('bgcolor', 'value'),
    State('fgcolor', 'value'),
    State('sizerange', 'value'),
    State('options_checklist', 'value'))
def register__update_pic(number, bgcolor, fgcolor, fontsize, options, old_number, old_bgcolor, old_fgcolor, old_fontsize, old_options):
    ctx = dash.callback_context
    fired_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

    if fired_id == 'input_number':
        return get_pic_data(int(number), old_bgcolor, old_fgcolor, old_fontsize, *[i in old_options for i in range(4)]) if number else ''

    elif fired_id == 'bgcolor':
        return get_pic_data(int(old_number), bgcolor, old_fgcolor, old_fontsize, *[i in old_options for i in range(4)]) if old_number else ''

    elif fired_id == 'fgcolor':
        return get_pic_data(int(old_number), old_bgcolor, fgcolor, old_fontsize, *[i in old_options for i in range(4)]) if old_number else ''

    elif fired_id == 'sizerange':
        return get_pic_data(int(old_number), old_bgcolor, old_fgcolor, fontsize, *[i in old_options for i in range(4)]) if old_number else ''

    elif fired_id == 'options_checklist':
        return get_pic_data(int(old_number), old_bgcolor, old_fgcolor, old_fontsize, *[i in options for i in range(4)]) if old_number else ''

    raise PreventUpdate

#-----------------------------------------------------------------------------------#

if __name__ == '__main__':
    # app.run_server(host='localhost', debug=DEBUG)
    app.run_server(debug=DEBUG)