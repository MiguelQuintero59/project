"""
Pipeline notebook for the project presentation Lv4.
"""

# Airbnb key 'd306zoyjsyarp7ifhu67rjxn52tv0t20'

if __name__ == '__main__':
    import os

    os.chdir('/Users/miguelquintero/Documents/airbnb/code')

    import wrangling
    import datetime
    import heatmap

    begin_time = datetime.datetime.now()
    """Variable para la medición del tiempo al momento de ejecutar todo el codigo"""

    print('Iniciando Cleaning de la información')
    wrangling.cleaning(path='../data/')

    print('Creando visualizaciones')
    heatmap.heatmap(path='../data')