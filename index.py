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

header_label = html.Div([html.H2('Легионъ имя мне'), html.H4(html.A('Числа кириллицей (малый счет)', href='https://ru.wikipedia.org/wiki/Система_записи_чисел_кириллицей', target='_blank'))], 
                        style={'text-align': 'center', 'margin': '2%'})

input_number_form = dbc.FormGroup(
    [
        dbc.Label('Число', html_for='input_number', width=3),
        dbc.Col(
            html.Div([           
                dbc.Input(id='input_number', type='number', style={'background-color': '#00bc7e'}, placeholder=f'1 - {MAXNUMBER}', min=1, max=MAXNUMBER, step=1),
                html.P(),
                dbc.Button('Случайное', id='btn_random', color='primary', outline=True)]),
            width={'size': 8, 'offset': 1}, lg={'size': 3, 'offset': 0}),
    ],
    row=True
)

bgcolor_form = dbc.FormGroup(
    [
        dbc.Label('Цвет фона', html_for='bgcolor', width=3),
        dbc.Col(
            dbc.Input(id='bgcolor', type='color', value='#000000'),
            width={'size': 8, 'offset': 1}, lg={'size': 3, 'offset': 0}
        )
    ],
    row=True
)

fgcolor_form = dbc.FormGroup(
    [
        dbc.Label('Цвет текста', html_for='fgcolor', width=3),
        dbc.Col(
            dbc.Input(id='fgcolor', type='color', value='#ffffff'),
            width={'size': 8, 'offset': 1}, lg={'size': 3, 'offset': 0}
        )
    ],
    row=True
)

size_form = dbc.FormGroup(
    [
        dbc.Label('Размер', html_for='sizerange', width=3),
        dbc.Col(
            dcc.Slider(id='sizerange', min=64, max=960, value=256, step=64),
            width={'size': 8, 'offset': 1}, lg={'size': 3, 'offset': 0}
        )
    ],
    row=True
)

options_form = dbc.FormGroup(
    [
        dbc.Label('Опции', html_for='options_checklist', width=3),
        dbc.Col(
            dbc.Checklist(
                id='options_checklist',
                options=[
                    {'label': 'Нет фона', 'value': 0},
                    {'label': 'Титло', 'value': 1},
                    {'label': 'Простой Леодр', 'value': 2},
                    {'label': 'Простая Колода', 'value': 3},
                ],
                value=[0, 1]),
            width={'size': 8, 'offset': 1}, lg={'size': 3, 'offset': 0}
        )
    ],
    row=True
)

form_all = html.Div(dbc.Form(id='form_all', children=[input_number_form, bgcolor_form, fgcolor_form, size_form, options_form]), 
                    style={'margin-top': '5%', 'margin-left': '5%', 'margin-right': '5%'})

img_card = html.Div(
    dcc.Loading(html.Img(id='img_number', src='', style={'width': '100%', 'height': 'auto', 'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'})), 
    style={'text-align': 'center', 'margin': '5%', 'display': 'inline-block', 'white-space': 'nowrap'})

footer = dbc.Navbar([
    dbc.NavLink('Iskander Shafikov, 2021', href='mailto:s00mbre@gmail.com', style={'color': 'black'})
], fixed='bottom')

#======================== MAIN LAYOUT ========================#

app.layout = html.Div(
    [
        header_label,
        form_all,
        img_card,
        footer
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
def generate_image(number, bgcolor, fgcolor, fontsize, options, old_number, old_bgcolor, old_fgcolor, old_fontsize, old_options):
    ctx = dash.callback_context
    fired_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

    if not fired_id in ('input_number', 'bgcolor', 'fgcolor', 'sizerange', 'options_checklist'):
        raise PreventUpdate

    if (fired_id == 'input_number' and not number) or (not old_number):
        return ''

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

@app.callback(
    Output('input_number', 'value'),
    Input('btn_random', 'n_clicks'))
def random_number(n):
    if not n: raise PreventUpdate
    return Cyrnum.random_number()

#-----------------------------------------------------------------------------------#

if __name__ == '__main__':
    # app.run_server(host='localhost', debug=DEBUG)
    app.run_server(debug=DEBUG)