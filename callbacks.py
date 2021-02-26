# import dash_core_components as dcc
# import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
# import numpy as np
import dash
# import dash_table
# from dash_table.Format import Format, Group, Scheme
# import dash_table.FormatTemplate as FormatTemplate
# from datetime import datetime as dt
from app import app
import plotly.express as px
from wordcloud import WordCloud
from io import BytesIO
import base64

corporate_colors = {
    'pink-red': 'rgb(255, 90, 95)',
    'blue-green': 'rgb(0, 166, 153)',
    'orange': 'rgb(252, 100, 45)',
    'dark-grey': 'rgb(72, 72, 72)',
    'white': 'rgb(251, 251, 252)',
    'light-grey': 'rgb(118, 118, 118)',
}

externalgraph_rowstyling = {
    'margin-left': '15px',
    'margin-right': '15px'
}

externalgraph_colstyling = {
    'border-radius': '10px',
    'border-style': 'solid',
    'border-width': '1px',
    'border-color': corporate_colors['dark-grey'],
    'background-color': corporate_colors['dark-grey'],
    'box-shadow': '0px 0px 17px 0px rgba(186, 218, 212, .5)',
    'padding-top': '10px'
}

filterdiv_borderstyling = {
    'border-radius': '0px 0px 10px 10px',
    'border-style': 'solid',
    'border-width': '1px',
    'border-color': corporate_colors['blue-green'],
    'background-color': corporate_colors['blue-green'],
    'box-shadow': '2px 5px 5px 1px rgba(255, 101, 131, .5)'
}

navbarcurrentpage = {
    'text-decoration': 'underline',
    'text-decoration-color': corporate_colors['pink-red'],
    'text-shadow': '0px 0px 1px rgb(251, 251, 252)'
}

recapdiv = {
    'border-radius': '10px',
    'border-style': 'solid',
    'border-width': '1px',
    'border-color': 'rgb(251, 251, 252, 0.1)',
    'margin-left': '15px',
    'margin-right': '15px',
    'margin-top': '15px',
    'margin-bottom': '15px',
    'padding-top': '5px',
    'padding-bottom': '5px',
    'background-color': 'rgb(251, 251, 252, 0.1)'
}

recapdiv_text = {
    'text-align': 'left',
    'font-weight': '350',
    'color': corporate_colors['white'],
    'font-size': '1.5rem',
    'letter-spacing': '0.04em'
}

corporate_title = {
    'font': {
        'size': 16,
        'color': corporate_colors['white']}
}

corporate_xaxis = {
    'showgrid': False,
    'linecolor': corporate_colors['light-grey'],
    'color': corporate_colors['light-grey'],
    'tickangle': 315,
    'titlefont': {
        'size': 12,
        'color': corporate_colors['light-grey']},
    'tickfont': {
        'size': 11,
        'color': corporate_colors['light-grey']},
    'zeroline': False
}

corporate_yaxis = {
    'showgrid': True,
    'color': corporate_colors['light-grey'],
    'gridwidth': 0.5,
    'gridcolor': corporate_colors['light-grey'],
    'linecolor': corporate_colors['light-grey'],
    'titlefont': {
        'size': 12,
        'color': corporate_colors['light-grey']},
    'tickfont': {
        'size': 11,
        'color': corporate_colors['light-grey']},
    'zeroline': False
}

corporate_font_family = 'Dosis'

corporate_legend = {
    'orientation': 'h',
    'yanchor': 'bottom',
    'y': 1.01,
    'xanchor': 'right',
    'x': 1.05,
    'font': {'size': 9, 'color': corporate_colors['light-grey']}
}

corporate_margins = {'l': 5, 'r': 5, 't': 45, 'b': 15}

corporate_layout = go.Layout(
    font = {'family': corporate_font_family},
    title = corporate_title,
    title_x = 0.5,  # Align chart title to center
    paper_bgcolor = 'rgba(0,0,0,0)',
    plot_bgcolor = 'rgba(0,0,0,0)',
    xaxis = corporate_xaxis,
    yaxis = corporate_yaxis,
    height = 270,
    legend = corporate_legend,
    margin = corporate_margins
)

################################################
##Data Mapping from data 00_raw
################################################

sales_filepath = 'data/00_raw/airbnb_cleaning_data.csv'

sales_fields = {
    'reporting_group_l1': 'room_and_property_type',
    'reporting_group_l2': 'name',
    'price_rate': 'price_rate',
    # 'sales': 'Sales Units',
    # 'revenues': 'Revenues',
    # 'sales target': 'Sales Targets',
    # 'rev target': 'Rev Targets',
    # 'num clients': 'nClients',
    'latitude': 'latitude',
    'longitude': 'longitude',
    'room_type': 'room_type',
    'summary': 'summary',
    'review_count': 'review_count',
    'review_score': 'review_score',
    'rating_accuracy': 'rating_accuracy',
    'rating_communication': 'rating_communication',
    'star_rating': 'star_rating',
    'satisfaction_guest': 'satisfaction_guest'
}

# 000 - IMPORT DATA

sales_import = pd.read_csv(sales_filepath)
# sales_import = xls.parse('Static')


# Create L1 dropdown options
repo_groups_l1 = sales_import[sales_fields['reporting_group_l1']].unique()
repo_groups_l1_all_2 = [
    {'label': k, 'value': k} for k in sorted(repo_groups_l1)
]
repo_groups_l1_all_1 = [{'label': '(Select All)', 'value': 'All'}]
repo_groups_l1_all = repo_groups_l1_all_1 + repo_groups_l1_all_2

# Initialise L2 dropdown options
repo_groups_l2 = sales_import[sales_fields['reporting_group_l2']].unique()
repo_groups_l2_all_2 = [
    {'label': k, 'value': k} for k in sorted(repo_groups_l2)
]
repo_groups_l2_all_1 = [{'label': '(Select All)', 'value': 'All'}]
repo_groups_l2_all = repo_groups_l2_all_1 + repo_groups_l2_all_2

# Create Dictionary
repo_groups_l1_l2 = {}
for l1 in repo_groups_l1:
    l2 = sales_import[sales_import[sales_fields['reporting_group_l1']] == l1][
        sales_fields['reporting_group_l2']].unique()
    repo_groups_l1_l2[l1] = l2

# 000 - DEFINE ADDITIONAL FUNCTIONS

def plot_wordcloud(text):
    wc = WordCloud(max_font_size=70, max_words=100, background_color="white").generate(text)
    return wc.to_image()

# 001 - L2 DYNAMIC DROPDOWN OPTIONS

@app.callback(
    dash.dependencies.Output('reporting-groups-l2dropdown-sales', 'options'),
    [dash.dependencies.Input('reporting-groups-l1dropdown-sales', 'value')])
def l2dropdown_options(l1_dropdown_value):
    isselect_all = 'Start' #Initialize isselect_all
    #Rembember that the dropdown value is a list !
    for i in l1_dropdown_value:
        if i == 'All':
            isselect_all = 'Y'
            break
        elif i != '':
            isselect_all = 'N'
        else:
            pass
    #Create options for individual selections
    if isselect_all == 'N':
        options_0 = []
        for i in l1_dropdown_value:
            options_0.append(repo_groups_l1_l2[i])
        options_1 = [] # Extract string of string
        for i1 in options_0:
            for i2 in i1:
                options_1.append(i2)
        options_list = [] # Get unique values from the string
        for i in options_1:
            if i not in options_list:
                options_list.append(i)
            else:
                pass
        options_final_1 = [
            {'label' : k, 'value' : k} for k in sorted(options_list)]
        options_final_0 = [{'label' : '(Select All)', 'value' : 'All'}]
        options_final = options_final_0 + options_final_1
    #Create options for select all or none
    else:
        options_final_1 = [
            {'label' : k, 'value' : k} for k in sorted(repo_groups_l2)]
        options_final_0 = [{'label' : '(Select All)', 'value' : 'All'}]
        options_final = options_final_0 + options_final_1

    return options_final

@app.callback(
    dash.dependencies.Output("histogram", "figure"),
    [dash.dependencies.Input("reporting-groups-l1dropdown-sales", "value"),
     dash.dependencies.Input('reporting-groups-l2dropdown-sales', 'value')])
def display_color(reporting_l1_dropdown,reporting_l2_dropdown):

    # Filter based on the dropdowns
    isselect_all_l1 = 'Start' #Initialize isselect_all
    isselect_all_l2 = 'Start' #Initialize isselect_all
    ## L1 selection (dropdown value is a list!)
    for i in reporting_l1_dropdown:
        if i == 'All':
            isselect_all_l1 == 'Y'
            break
        elif i != '':
            isselect_all_l1 = 'N'
        else:
            pass
    #Filtering according to selection
    if isselect_all_l1 == 'N':
        sales_df_1 = sales_import.loc[sales_import[sales_fields['reporting_group_l1']].isin(reporting_l1_dropdown), : ].copy()
    else:
        sales_df_1 = sales_import.copy()


    ## L2 selection (dropdown value is a list!)
    for i in reporting_l2_dropdown:
        if i == 'All':
            isselect_all_l2 == 'Y'
            break
        elif i != '':
            isselect_all_l2 = 'N'
        else:
            pass
    #Filtering according to selection l2
    if isselect_all_l2 == 'N':
        sales_df = sales_df_1.loc[sales_import[sales_fields['reporting_group_l2']].isin(reporting_l2_dropdown), : ].copy()
    else:
        sales_df = sales_df_1.copy()
    del sales_df_1

    #Aggregate dataframe
    cols = [sales_fields['price_rate'], sales_fields['reporting_group_l1']]
    df =  sales_df[cols]

    #Building the graph
    data = go.Histogram(x = df[sales_fields['price_rate']])
    fig = go.Figure(data =data, layout = corporate_layout)

    corporate_margins_here = corporate_margins
    corporate_margins_here['t'] = 65
    fig.update_layout(
        title={'text' : "Price Rate Histogram"},
        xaxis = {'title' : "Price Rate", 'tickangle' : 0},
        yaxis = {'title' : "Count"},
        margin = corporate_margins_here)
    return fig

@app.callback(
    dash.dependencies.Output("heatmap", "figure"),
    [dash.dependencies.Input("reporting-groups-l1dropdown-sales", "value"),
     dash.dependencies.Input('reporting-groups-l2dropdown-sales', 'value')])
def heatmap(reporting_l1_dropdown,reporting_l2_dropdown):

    # Filter based on the dropdowns
    isselect_all_l1 = 'Start' #Initialize isselect_all
    isselect_all_l2 = 'Start' #Initialize isselect_all
    ## L1 selection (dropdown value is a list!)
    for i in reporting_l1_dropdown:
        if i == 'All':
            isselect_all_l1 == 'Y'
            break
        elif i != '':
            isselect_all_l1 = 'N'
        else:
            pass
    #Filtering according to selection
    if isselect_all_l1 == 'N':
        sales_df_1 = sales_import.loc[sales_import[sales_fields['reporting_group_l1']].isin(reporting_l1_dropdown), : ].copy()
    else:
        sales_df_1 = sales_import.copy()


    ## L2 selection (dropdown value is a list!)
    for i in reporting_l2_dropdown:
        if i == 'All':
            isselect_all_l2 == 'Y'
            break
        elif i != '':
            isselect_all_l2 = 'N'
        else:
            pass
    #Filtering according to selection l2
    if isselect_all_l2 == 'N':
        sales_df = sales_df_1.loc[sales_import[sales_fields['reporting_group_l2']].isin(reporting_l2_dropdown), : ].copy()
    else:
        sales_df = sales_df_1.copy()
    del sales_df_1

    #Aggregate dataframe
    cols = [sales_fields['price_rate'], sales_fields['reporting_group_l1'], sales_fields['reporting_group_l2'], sales_fields['latitude'], sales_fields['longitude']]
    df =  sales_df[cols]

    fig = px.scatter_mapbox(df,
                            lat = df[sales_fields["latitude"]],
                            lon = df[sales_fields["longitude"]],
                            hover_name = df[sales_fields["reporting_group_l2"]],
                            hover_data = [sales_fields['reporting_group_l1'], sales_fields['price_rate']],
                            color_discrete_sequence = ["goldenrod"],
                            zoom = 14,
                            size = df[sales_fields['price_rate']],
                            height = 370)
    fig.update_layout(mapbox_style = "open-street-map",
                      margin = {"r": 0, "t": 0, "l": 0, "b": 0},
                      title={'text' : "HeatMap"},)
    fig.update_traces(marker = go.scattermapbox.Marker(sizeref = 12))
    return fig


@app.callback(
    dash.dependencies.Output('image_wc', 'src'),
    [dash.dependencies.Input('image_wc', 'id')])
def make_image(b):
    data_text = ','.join(str(v) for v in sales_import['description'])
    data_text = data_text.replace('\n', ' ')
    data_text = data_text.replace("\ ", " ")
    img = BytesIO()
    plot_wordcloud(data_text).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

@app.callback(
    dash.dependencies.Output("price_rate", "figure"),
    [dash.dependencies.Input("reporting-groups-l1dropdown-sales", "value"),
     dash.dependencies.Input('reporting-groups-l2dropdown-sales', 'value')])
def star_rating(reporting_l1_dropdown,reporting_l2_dropdown):

    # Filter based on the dropdowns
    isselect_all_l1 = 'Start' #Initialize isselect_all
    isselect_all_l2 = 'Start' #Initialize isselect_all
    ## L1 selection (dropdown value is a list!)
    for i in reporting_l1_dropdown:
        if i == 'All':
            isselect_all_l1 == 'Y'
            break
        elif i != '':
            isselect_all_l1 = 'N'
        else:
            pass
    #Filtering according to selection
    if isselect_all_l1 == 'N':
        sales_df_1 = sales_import.loc[sales_import[sales_fields['reporting_group_l1']].isin(reporting_l1_dropdown), : ].copy()
    else:
        sales_df_1 = sales_import.copy()


    ## L2 selection (dropdown value is a list!)
    for i in reporting_l2_dropdown:
        if i == 'All':
            isselect_all_l2 == 'Y'
            break
        elif i != '':
            isselect_all_l2 = 'N'
        else:
            pass
    #Filtering according to selection l2
    if isselect_all_l2 == 'N':
        sales_df = sales_df_1.loc[sales_import[sales_fields['reporting_group_l2']].isin(reporting_l2_dropdown), : ].copy()
    else:
        sales_df = sales_df_1.copy()
    del sales_df_1

    scatter_df = sales_df[[sales_fields["reporting_group_l1"], sales_fields["reporting_group_l2"], sales_fields["star_rating"],
                     sales_fields["review_score"], sales_fields["price_rate"]]]
    scatter_df = scatter_df.dropna()
    scatter_df.reset_index(inplace = True, drop = True)

    data = go.Scatter(x = scatter_df[sales_fields["review_score"]],y = scatter_df[sales_fields["star_rating"]],
                      mode = 'markers',
                      # marker_size = scatter_df[sales_fields["review_score"]].count(),
                      line = {'color' : corporate_colors['blue-green'], 'width' : 0.5})
                      # hovertemplate = hovertemplate_xy)

    fig = go.Figure(data=data, layout=corporate_layout)

    fig.update_layout(
        title={'text' : "Buble Chart"},
        xaxis = {'title' : "Review Score"},
        yaxis = {'title' : "Star rating"}
    )

    return fig