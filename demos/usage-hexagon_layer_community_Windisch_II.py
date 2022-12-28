"""
Adapted from: https://pydeck.gl/gallery/arc_layer.html

Map of commutes to work within a segment of downtown San Francisco using a
deck.gl ArcLayer.

Green indicates a start point, and red indicates the destination.

The data is collected by the US Census Bureau and viewable in the 2017
LODES data set: https://lehd.ces.census.gov/data/
"""
import os

import dash
import dash_deck
import pydeck as pdk
import pandas as pd

from dash import dcc
from dash import html

# mapbox_api_token = os.getenv("MAPBOX_ACCESS_TOKEN")
mapbox_api_token = "pk.eyJ1IjoicGV0ZXJzdGF1YjYxIiwiYSI6ImNsYnhjenFyejE1d3Q0MG55NjBjZDJ6aWoifQ.xgY2YrkCbL2pq0CletAT5g"


# NUR REDUZIERTES FILE EINLESEN WEGEN GITHUB-LIMITIERUNG AUF 25 GB !
re_cash_columns_Windisch_CH = pd.read_csv("co2_landscape_community_Windisch.csv")

# EXAMPLE WINDISCH

df = re_cash_columns_Windisch_CH

# Define a layer to display on a map

layer_windisch = pdk.Layer(
    "GridLayer", df, pickable=True, extruded=True, cell_size=30, elevation_scale=2, get_position=['Longitude', 'Latitude'],
)

# view_state = pdk.ViewState(latitude=46.7, longitude=8.22106, zoom=100, min_zoom=2)
# Set height and width variables
# view = pdk.View(type="_GlobeView", controller=True, width=1000, height=100)

view_state = pdk.ViewState(latitude=47.4747, longitude=8.21907, zoom=14, bearing=0, pitch=50,width=100, height=100)

# Render
r = pdk.Deck(layers=[layer_windisch], 
             initial_view_state=view_state, 
             tooltip={"text": "{position}\nCount: {count}"},
             api_keys={"mapbox":mapbox_api_token},
             map_provider="mapbox",
             map_style=pdk.map_styles.MAPBOX_DARK,       
            )


# r.to_html("grid_layer.html")

app = dash.Dash(__name__)

app.layout = html.Div(
    dash_deck.DeckGL(
        r.to_json(), id="deck-gl", mapboxKey=r.mapbox_key
    )
)


if __name__ == "__main__":
    app.run_server(debug=True)