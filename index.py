import dash_core_components as dcc
import dash_html_components as html
import dash

from app import app
from app import server
from layouts import airbnb, page2, page3
import callbacks

app.title = 'Project Lv.4'
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/airbnb-overview':
         return airbnb
    elif pathname == '/apps/page2':
         return page2
    elif pathname == '/apps/page3':
         return page3
    else:
        return airbnb # This is the "home page"

if __name__ == '__main__':
    app.run_server(debug=False, port=8060)