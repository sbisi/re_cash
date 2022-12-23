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
import dash_html_components as html
import pydeck as pdk
import pandas as pd

# mapbox_api_token = os.getenv("MAPBOX_ACCESS_TOKEN")
mapbox_api_token = "pk.eyJ1IjoicGV0ZXJzdGF1YjYxIiwiYSI6ImNsYnhjenFyejE1d3Q0MG55NjBjZDJ6aWoifQ.xgY2YrkCbL2pq0CletAT5g"

""" GANZES DATENSET EINLESEN !

#reading re_cash_data
re_cash = pd.read_csv("co2_landscape.csv")
re_cash.info()
re_cash.head()

# eliminating not necessary data
re_cash_columns = re_cash.iloc[:,[7,8,14,15,23]] # select column 14 und 15 (canton, community,  Longtitude, Latitude)
re_cash_columns.info()
re_cash_columns.head()

# specific data for the canton AG & location Windisch
re_cash_columns_canton = re_cash_columns.loc[re_cash_columns["GDEKT"] == "AG"]
re_cash_columns_community = re_cash_columns.loc[re_cash_columns["GDENAME"] == "Windisch"]
re_cash_columns_community.info()
re_cash_columns_community.head()

# reduction the big size of data with random function
re_cash_columns_random = re_cash_columns.sample(frac = 0.10, random_state=12)
re_cash_columns_random.info()
re_cash_columns_random.head()
"""


# NUR REDUZIERTES FILE EINLESEN WEGEN GITHUB-LIMITIERUNG AUF 25 GB !
re_cash_columns_random = pd.read_csv("co2_landscape_random_reduced.csv")

"""# visualizing with hexagon layer (pydeck)"""

tooltip = {
   "html": "<b>Elevation Value:</b> {elevationValue}",
   "style": {
        "backgroundColor": "steelblue",
        "color": "white"
   }
}

layer = pdk.Layer(
    'HexagonLayer',  # `type` positional argument is here
    re_cash_columns_random, 
    get_position=['Longitude', 'Latitude'],
    auto_highlight=True,
    elevation_scale=20,
    pickable=True,
    elevation_range=[0, 3000],
    extruded=True,
    coverage=1)

view_state = pdk.ViewState(
    longitude=8.1355,
    latitude=46.7,
    zoom=7,
    min_zoom=6,
    max_zoom=15,
    pitch=40.5,
    bearing=-20.36)


# Combined all of it and render a viewport
r = pdk.Deck(layers=[layer], 
             initial_view_state=view_state,
             tooltip=tooltip,
             api_keys={"mapbox":mapbox_api_token},
             map_provider="mapbox",
             map_style=pdk.map_styles.MAPBOX_DARK, 
    )

# Combined all of it and render a viewport
r.to_html('peter_staub.html')

app = dash.Dash(__name__)

app.layout = html.Div(
    dash_deck.DeckGL(
        r.to_json(), id="deck-gl", mapboxKey=r.mapbox_key
    )
)


if __name__ == "__main__":
    app.run_server(debug=True)