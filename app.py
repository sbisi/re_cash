from importlib import import_module
import inspect
from textwrap import dedent
import os

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from tqdm import tqdm

def Header(name, app):
    title = html.H1(name, style={"margin-top": 15})
    logo = html.Img(
        #src=app.get_asset_url('dash-logo.png'),


        src=app.get_asset_url('dash-logo.png'), style={"float": "right", "height": 40, "marginTop": 30, "marginRight": 20}

        #style={'float': 'right', 'height': 60,"marginTop": 20, "marginRight": 40}
    )
    link = html.A(logo, href="https://www.pom.ch/")

    return dbc.Row([dbc.Col(title, md=8), dbc.Col(link, md=4)])


def format_demo_name(demo):
    return demo.replace("usage-", "").replace("-", " ").title()


ignored_demos = ["usage-events.py", "usage-style-prop.py", "usage-geopandas.py"]

deck_demos = [
    n.replace(".py", "").replace("usage-", "")
    for n in sorted(os.listdir("./demos"))
    if ".py" in n and n not in ignored_demos
]

print(os.getcwd())
deck_modules = {demo: import_module(f"demos.usage-{demo}") for demo in tqdm(deck_demos)}

print("Loaded demos:", deck_demos)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

app_selection = html.Div(
    [
        dbc.Label("Visualizing Model", width=3),
        dbc.Col(
            dbc.Select(
                id="demo-selection",
                options=[
                    {"label": demo.replace("-", " ").title(), "value": demo}
                    for demo in deck_demos
                ],
                style={'background-color':'white'},
                className="form-control-plaintext",
                value=deck_demos[0],
            ),
#            width=9,
#            style={ 'border':'2px solid white', 'width':'200px', 'margin':'0 auto'},
        ),
    ],
#    row=True,
)

tab_style = {"height": "calc(100vh - 230px)", "padding": "15px"}
# tab_style = {'max-height': 'calc(100vh - 210px)'}
tabs = dbc.Tabs(
    [
        dbc.Tab(dcc.Markdown(id="description", style=tab_style), label="Description"),
        dbc.Tab(dcc.Markdown(id="source-code", style=tab_style), label="Source Code"),
    ]
)

layout = [
    Header("Dash Deck Explorer", app),
    html.Br(),
    dcc.Location(id="url", refresh=False),
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    id="deck-card", style={"height": "calc(100vh - 110px)"}, body=True
                ),
                md=6,
            ),
            dbc.Col([app_selection, tabs], md=6),
        ]
    ),
]

app.layout = dbc.Container(layout, fluid=True)


@app.callback(Output("url", "pathname"), Input("demo-selection", "value"))
def update_url(name):
    return "/deck-explorer/" + name


@app.callback(
    [
        Output("deck-card", "children"),
        Output("description", "children"),
        Output("source-code", "children"),
    ],
    Input("url", "pathname"),
)
def update_demo(pathname):
    if pathname in ["/deck-explorer/", None, "/"]:
        return dash.no_update

    name = pathname.split("/")[-1]

    module = deck_modules[name]
    deck_component = module.app.layout
    desc = module.__doc__
    code = f"```\n{inspect.getsource(module)}\n```"

    end = dedent(
        
        f"""

    -----
    
    HALLO 

    """)

    return deck_component, desc+end, code


if __name__ == "__main__":
    app.run_server(debug=True)