from dash import dcc, html
from ..config import color_list1, color_list2
from ..data import get_data

def generate_description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H2("Road Safety Dashboard"),
            html.Div(
                id="intro",
                children="A tool developed for the course JBI100 for use in visualising traffic accident data in Great Britain during 2015.",
            ),
        ],
    )


def generate_control_card():
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.H5("Bar chart x-axis"),
            dcc.Dropdown(
                id="dropdown1",
                options=[{"label":x,"value":x} for x in get_data()[0].columns],
                value=get_data()[0].columns[11],
                clearable=False
            ),
            #html.Br(),
            html.H5("Bar chart y-axis"),
            dcc.Dropdown(
                id="dropdown2",
                options=[{"label":x,"value":x} for x in get_data()[0].columns],
                value=get_data()[0].columns[10],
                clearable=False,
                className="dropdown"
            ),
            #html.Br(),
            html.H5('Select attributes for Sunburst chart'),
            dcc.Dropdown(
                id="sunburstmenu",
                options=[{"label":x,"value":x} for x in get_data()[0].columns],
                value= [get_data()[3].columns[58], get_data()[3].columns[59]],
                multi=True
            ),
            #html.Br(),
            html.H5('Select attribute for map, box plot, and cal plot'),
            dcc.Dropdown(
                id="boxmenu",
                options=[{"label":x,"value":x} for x in get_data()[0].columns],
                value =get_data()[0].columns[10],
                clearable=False,
            ),
            #html.Br(),
            #html.H5('Select attribute for map coloring'),
            #dcc.Dropdown(
            #    id="cartomenu",
            #    options=[{"label":x,"value":x} for x in get_data()[0].columns],
            #    value =get_data()[0].columns[10],
            #    clearable=False,
            #),
            #html.Br(),
            html.H5('Select map timerange'),
            dcc.RadioItems(
                id='timerange',
                options=[
                    {'label': 'Month', 'value': 'Month'},
                    {'label': 'Day of the week', 'value': 'Day of the week'},
                    {'label': 'Hour', 'value': 'Hour'}
                ],
                value='Month'
            ),
            html.H5('Select color mode'),
            dcc.RadioItems(
                id='colormode',
                options=[{'value': x, 'label': x} 
                        for x in ['discrete', 'continuous']],
                value='discrete'
            ),
            
        ], style={"textAlign": "float-left"}
    )


def make_menu_layout():
    return [generate_description_card(), generate_control_card()]
