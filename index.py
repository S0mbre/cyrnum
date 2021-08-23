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

IMGHDR = \
"""
data:image/png;base64,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u+ZJALzO/rK0407b+1meFErvlwEcmcmAEzPNgp6bc2Jz9zMZexvA9TJpcdAzAsBT5/QB6OYfmCz5yRglgOZUND8Y8oWYfQcmGBWoRr+ZvS41ClkzjeD8HZ4na/e/vroGyvxuM+MRffYJmkaMqft7AZSiv026OyZgHhIyIwgKLuQXEtQCTvvbOLZyckuoHwTNzMKbfiPm0tAYysgoJUU93Lf4oruXgs2EGZTmhbG/ByOsjU2W74f6yCoJ576REjCSaMfchAI/tT0KtnSuoRB4ae3dbXe/CsC9MkLovg2IHqG0cWCjEEk2vDabStEHAbzdzH53JPKVX3f3n0jX3XeVEpaJ4USfbWYhRSQ5EJ8C4PY9mjwjc/BGTZ4m7Lqlc+XCBz8MCGGjjnoD6c2+uI84bQtSGnxtFJupmS3h+4BAzWKOEYRLJlejlNABJaC0uRAqb8DfhdmPiWUeMVmb1McCYyG0IzqDElDaDFvMmrSucVeIGBXiERyf2YAI7foGTOma16earUWUgPBpQ4BDiOccbR8o26rZTporVs10tBKwakb6bjoBd6cwe7+0u00b0cZEhZPC75sZI2joaRFIzGhf+MNpd/sPALxo1d16d380AE543AHkKcMXGF3IzM47KOBb/awbzoz3LFwVVZwOCo+DWA93542mfeZyVJBpXrNWZbbEOG2+/Lseh39uxHwoMp6TGctR6Ui+L8twWs3H6UK7O7cS+3YAt0jRxfjnL5oZTz5XfpIAzzSZ9j0SA7bPB7j5ZGb0GSg+LYaMZMaACLwbZaeMKa1R47tVLq5LTVS0plyfn1rvYoUW+EJmXIX7QU+f6tY0nBY/HOj3DDVLc8i/SyYroTG0TuSZ8Tp6nK6z3JuWl5SATWsxlVcEREAEREAEREAEREAEJhKQEjARoD4XAREQAREQAREQAREQgU0jICVg01pM5RUBERABERABERABERCBiQSkBEwEqM9FQAREQAREQAREQAREYNMISAnYtBZTeUVABERABERABERABERgIgEpARMB6nMREAEREAEREAEREAER2DQCUgI2rcVUXhEQAREQAREQAREQARGYSEBKwESA+lwEREAEREAEREAEREAENo2AlIBNazGVVwREQAREQAREQAREQAQmEpASMBGgPhcBERABERABERABERCBTSMgJWDTWkzlFQEREAEREAEREAEREIGJBKQETASoz0VABERABERABERABERg0whICdi0FlN5RUAEREAEREAEREAERGAiASkBEwHqcxEQAREQAREQAREQARHYNAJSAjatxVReERABERABERABERABEZhIQErARID6XAREQAREQAREQAREQAQ2jYCUgE1rMZVXBERABERABERABERABCYSkBIwEaA+FwEREAEREAEREAEREIFNIyAlYNNaTOUVAREQAREQAREQAREQgYkEpARMBKjPRUAEREAEREAEREAERGDTCEgJ2LQWU3lFQAREQAREQAREQAREYCIBKQETAepzERABERABERABERABEdg0AlICNq3FVF4REAEREAEREAEREAERmEhASsBEgPpcBERABERABERABERABDaNgJSATWsxlVcEREAEREAEREAEREAEJhKQEjARoD4XAREQAREQAREQAREQgU0jICVg01pM5RUBERABERABERABERCBiQSkBEwEqM9FQAREQAREQAREQAREYNMISAnYtBZTeUVABERABERABERABERgIgEpARMB6nMREAEREAEREAEREAER2DQC/x8rp9Xl6qNcigAAAABJRU5ErkJggg==
"""

#========================== LAYOUTS =========================#


headerimg = html.Div(html.Img(id='img_header', src=IMGHDR), 
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