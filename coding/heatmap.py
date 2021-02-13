import pandas as pd
import folium
from folium.plugins import HeatMap


def heatmap(path='../data'):
    airbnb_df = pd.read_csv(path +'/00_raw/airbnb_cleaning_data.csv')
    folium_hmap = folium.Map(location=[10.3932, -75.4832],
                             zoom_start=10,
                             tiles="OpenStreetMap")

    hm_wide = HeatMap(list(zip(airbnb_df['latitude'], airbnb_df['longitude'], airbnb_df['price_rate'])),
                      min_opacity=0.1,
                      radius=10, blur=6,
                      zoom_start=60,
                      )
    return folium_hmap.add_child(hm_wide)