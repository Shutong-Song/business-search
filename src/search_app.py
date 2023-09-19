"""
frontend of the search tab, includes:
1. functions to create widget
2. layout
"""
import dash_bootstrap_components as dbc
from dash import html, dcc, Dash, Input, Output, State
import dash_leaflet as dl
from whitenoise import WhiteNoise



states_abbr = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
       'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
       'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
       'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN',
       'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
states_name = ['Alaska', 'Alabama', 'Arkansas', 'Arizona', 'California',
       'Colorado', 'Connecticut', 'District of Columbia', 'Delaware',
       'Florida', 'Georgia', 'Hawaii', 'Iowa', 'Idaho', 'Illinois',
       'Indiana', 'Kansas', 'Kentucky', 'Louisiana', 'Massachusetts',
       'Maryland', 'Maine', 'Michigan', 'Minnesota', 'Missouri',
       'Mississippi', 'Montana', 'North Carolina', 'North Dakota',
       'Nebraska', 'New Hampshire', 'New Jersey', 'New Mexico', 'Nevada',
       'New York', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
       'Puerto Rico', 'Rhode Island', 'South Carolina', 'South Dakota',
       'Tennessee', 'Texas', 'Utah', 'Virginia', 'Vermont', 'Washington',
       'Wisconsin', 'West Virginia', 'Wyoming']
state_mapping = {'AK': [63.588753, -154.493062], 'AL': [32.318231, -86.902298], 'AR': [35.20105, -91.831833], 'AZ': [34.048928, -111.093731], 'CA': [36.778261, -119.417932], 'CO': [39.550051, -105.782067], 'CT': [41.603221, -73.087749], 'DC': [38.905985, -77.033418], 'DE': [38.910832, -75.52767], 'FL': [27.664827, -81.515754], 'GA': [32.157435, -82.907123], 'HI': [19.898682, -155.665857], 'IA': [41.878003, -93.097702], 'ID': [44.068202, -114.742041], 'IL': [40.633125, -89.398528], 'IN': [40.551217, -85.602364], 'KS': [39.011902, -98.484246], 'KY': [37.839333, -84.270018], 'LA': [31.244823, -92.145024], 'MA': [42.407211, -71.382437], 'MD': [39.045755, -76.641271], 'ME': [45.253783, -69.445469], 'MI': [44.314844, -85.602364], 'MN': [46.729553, -94.6859], 'MO': [37.964253, -91.831833], 'MS': [32.354668, -89.398528], 'MT': [46.879682, -110.362566], 'NC': [35.759573, -79.0193], 'ND': [47.551493, -101.002012], 'NE': [41.492537, -99.901813], 'NH': [43.193852, -71.572395], 'NJ': [40.058324, -74.405661], 'NM': [34.97273, -105.032363], 'NV': [38.80261, -116.419389], 'NY': [43.299428, -74.217933], 'OH': [40.417287, -82.907123], 'OK': [35.007752, -97.092877], 'OR': [43.804133, -120.554201], 'PA': [41.203322, -77.194525], 'PR': [18.220833, -66.590149], 'RI': [41.580095, -71.477429], 'SC': [33.836081, -81.163725], 'SD': [43.969515, -99.901813], 'TN': [35.517491, -86.580447], 'TX': [31.968599, -99.901813], 'UT': [39.32098, -111.093731], 'VA': [37.431573, -78.656894], 'VT': [44.558803, -72.577841], 'WA': [47.751074, -120.740139], 'WI': [43.78444, -88.787868], 'WV': [38.597626, -80.454903], 'WY': [43.075968, -107.290284]}

################################################################################ 
# search widget
################################################################################ 
### 1. search input box 
def create_search_textbox():
    return dbc.InputGroup([
                    dbc.Input(id="input", placeholder="search business...", type="text", debounce=True,style = {"height": "50px", "margin-top":"20px"}),
                    dbc.Button(id = "speech", 
                                   style = {"width": "30px", "height":"30px", "background-image": "url(speech.png)",
                                            "background-size": "cover",
                                            "border-color": "transparent", "background-color":"transparent","margin-top": "30px", "margin-left":"-30px"}, 
                                   color = "transparent",
                               )
                ])

### 2. search state dropdown
def create_search_dd():
    return dcc.Dropdown(
    [{"label":abbr, "value":abbr, "search":full_name} for abbr, full_name in zip(list(state_mapping.keys()), states_name)],
    value = "NY",
    placeholder = "State",
    id = "state-dropdown",
    clearable=False,
    style={"margin-top":"20px", "height":"50px", "background-color":"dark", "textAlign":"left", 'font-size': '100%',"verticalAlign": "bottom"}
)

### 3. search click button
def create_search_button():
    return dbc.Button(id='search_button', 
                      style = {"width": "50px", "height":"50px", "background-image": "url(search_button_logo.png)",
                                "background-size": "cover",
                                "border-color": "transparent", "background-color":"transparent","margin-top": "20px"}, 
                      color = "transparent")



################################################################################ 
# search tab content
################################################################################ 
search_content = html.Div([dbc.Row([dbc.Col(create_search_textbox(), md = 8), ###create search bar
                                    dbc.Col(create_search_dd(), md = 1),
                                  dbc.Col(create_search_button(), md = 1),
                                  ],
                            justify="left",
                            className="g-0",
                            style = {"margin-left": "15%"}
                            ),

                        ### create a box for map
                        dbc.Row([
                        dbc.Col(dl.Map(children = [dl.TileLayer(), dl.LayerGroup(id="container", children = [])], id = "map", preferCanvas=True, \
                                        zoom = 7, center = (40.776676, -73.971321)))
                        ], style = {"margin-left":"5%", "margin-right":"5%","margin-top":"5px", "border":"2px solid gray", "width":"90%", "height":"600px"}),

                        # dcc.Store stores the intermediate value
                        dcc.Store(id='search-query-saved'),
                        html.Div(id = "test")
                       ])




################################################################################ 
# main App
################################################################################ 
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], prevent_initial_callbacks=True, suppress_callback_exceptions = True)
server = app.server
server.wsgi_app = WhiteNoise(server.wsgi_app, root="static/")
app.title = "business"
#app._favicon = ("/assets/favicon.ico")
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


### callback for dropdown select state and map will center to that state
@app.callback(
    Output("map", "center"),
    Input('state-dropdown', 'value')
)
def update_output(value):
    return [*state_mapping[value]]

if __name__ == '__main__':
    #app.run_server(host = "localhost", port = 9011, debug = True)
    app.run(debug = False)