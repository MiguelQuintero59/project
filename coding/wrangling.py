"""

"""
__author__ = 'Miguel Quintero'

import pandas as pd


def cleaning(path='../data'):
    """
    Comienza el proceso de limpieza de datos

    Parameters
    ----------
    path: str
        Ubicacion de la carpeta de datos
    """

    airbnb_df = pd.read_csv(path +'/cartagena.csv',
                            dtype='str')

    airbnb_df = airbnb_df[airbnb_df.price_rate.apply(lambda x: x.isnumeric())]

    airbnb_df = airbnb_df.loc[:, ~airbnb_df.columns.str.contains('^Unnamed')]

    airbnb_df = airbnb_df.drop(['total_price', 'price_rate_type', 'url', 'min_nights',
                                'monthly_price_factor', 'weekly_price_factor', 'amenities',
                                'notes', 'additional_house_rules', 'interaction', 'access',
                                'transit', 'response_rate', 'neighborhood_overview', 'rating_checkin',
                                'rating_cleanliness', 'rating_location', 'rating_value', 'description'],
                               axis=1, inplace=True)

    airbnb_df["latitude"] = pd.to_numeric(airbnb_df['latitude'],
                                          downcast='float')
    airbnb_df["longitude"] = pd.to_numeric(airbnb_df['longitude'],
                                           downcast='float')
    airbnb_df["price_rate"] = pd.to_numeric(airbnb_df['price_rate'],
                                            downcast='float')

    airbnb_df.to_csv(path + '/00_raw/airbnb_cleaning_data.csv', index=False)

    return "Fin"
