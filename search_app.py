"""
frontend of the search tab, includes:
1. functions to create widget
2. layout
"""
import dash_bootstrap_components as dbc
from dash import html, dcc, Dash, Input, Output, State
import dash_leaflet as dl
from whitenoise import WhiteNoise


################################################################################ 
# search widget
################################################################################ 
### 2. search input box 
def create_search_textbox():
    return dbc.InputGroup([
                    dbc.Input(id="input", placeholder="search business...", type="text", debounce=True,style = {"height": "50px", "margin-top":"20px"}),
                    dbc.Button(id = "speech", 
                                   style = {"width": "30px", "height":"30px", "background-image": 'url(speech.png)', 
                                            "background-size": "cover",
                                            "border-color": "transparent", "background-color":"transparent","margin-top": "30px", "margin-left":"-30px"}, 
                                   color = "transparent",
                               )
                ])

### 3. search click button
def create_search_button():
    return dbc.Button(id='search_button', 
                      style = {"width": "50px", "height":"50px", "background-image": 'url(search_button_logo.png)', 
                                "background-size": "cover",
                                "border-color": "transparent", "background-color":"transparent","margin-top": "20px"}, 
                      color = "transparent")



################################################################################ 
# search tab content
################################################################################ 
search_content = html.Div([dbc.Row([dbc.Col(create_search_textbox(), md = 8), ###create search bar
                                  dbc.Col(create_search_button(), md = 1),
                                  ],
                            justify="left",
                            className="g-0",
                            style = {"margin-left": "15%"}
                            ),

                        ### create a box for map
                        dbc.Row([
                        dbc.Col(dl.Map(children = [dl.TileLayer(), dl.LayerGroup(id="container", children = [])], id = "map", preferCanvas=True, \
                                        zoom = 10, center = (33.4484, -112.074)))
                        ], style = {"margin-left":"5%", "margin-right":"5%","margin-top":"5px", "border":"2px solid gray", "width":"90%", "height":"600px"}),

                        # dcc.Store stores the intermediate value
                        dcc.Store(id='search-query-saved'),
                       ])




################################################################################ 
# main App
################################################################################ 
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], prevent_initial_callbacks=True, suppress_callback_exceptions = True)
server = app.server
server.wsgi_app = WhiteNoise(server.wsgi_app, root="static/")
app.title = "business"
app._favicon = ("desk.svg")
app.layout = dbc.Container(
    [
        #html.Img(src="assets/cell.svg", style={'height':'10%', 'width':'10%', "margin-top":"30px", "margin-left":"70px"}),
        html.Div(style = {"height": '10%', "margin-top": "30px"}),
        html.Hr(),
        dbc.Row(
                    dbc.Tab(search_content, label="Search", disabled = False),
                ),
    ], fluid = True)



################################################################################ 
# recalls
################################################################################ 
@app.callback(Output("container", "children"),
              [Input("search_button", "n_clicks"),
               Input("input", "n_submit"),
               State("input", "value")]
)
def save_input_search_query(clicks, nsub, input_value):
    ### save model prediction of user input query to dcc.Store
    search_query = input_value.strip() if input_value else "" ## if not input anything, input_value == None
    if (clicks is not None and search_query != "") or (nsub is not None and search_query != ""):
        return [dl.Marker(position=[33.522143, -112.018481], children=dl.Tooltip("Golf Club"))]
    return []


if __name__ == '__main__':
    #app.run_server(host = "localhost", port = 9011, debug = True)
    app.run(debug = False)