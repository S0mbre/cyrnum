# -*- coding: utf-8 -*-
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components.themes import DARKLY

meta_tags = [{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.5, minimum-scale=0.5'}]
ext_css = [dbc.themes.DARKLY] # https://bootswatch.com/darkly/

app = dash.Dash(__name__, suppress_callback_exceptions=True, meta_tags=meta_tags, external_stylesheets=ext_css)

app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-QCSXQ3REHF"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-QCSXQ3REHF');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

app.title = 'Легионъ имя мне: числа кириллицей'
app.config.suppress_callback_exceptions = True

server = app.server