from dash import html, dcc
import dash_bootstrap_components as dbc

from deploy_chatbot_python.config import constants


layout = dbc.Container(
    [
        html.H2(constants.DASHBOARD_TITLE, className="text-center my-4"),
        dbc.Card(
            dbc.CardBody(
                [
                    # Chat history display
                    html.Div(
                        id="chat-history",
                        style={
                            "height": "600px",
                            "overflowY": "auto",
                            "border": "1px solid #ccc",
                            "padding": "10px",
                            "marginBottom": "15px",
                        },
                    ),
                    # User input area
                    dbc.InputGroup(
                        [
                            dcc.Input(
                                id="user-input",
                                placeholder=constants.USER_PLACEHOLDER_MESSAGE,
                                type="text",
                                debounce=True,
                                style={"width": "90%"},
                            ),
                            dbc.Button(
                                constants.SEND_BUTTON_TEXT,
                                id="send-button",
                                color="primary",
                                n_clicks=0,
                                style={"width": "10%"},
                            ),
                        ],
                        className="mb-3",
                    ),
                    # Error message display
                    html.Div(id="error-message", className="text-danger"),
                    # Hidden store for chat history
                    dcc.Store(id="chat-store", data=[]),
                ]
            )
        ),
    ],
    fluid=True,
)

def make_chat_element(message: str, text_align: str, bubble_color: str) -> html.Div:
    chat_element = html.Div(
        html.Div(
            message,
            style={
                "backgroundColor": bubble_color,
                "padding": "10px 15px",
                "borderRadius": "15px",
                "maxWidth": "60%",
                "display": "inline-block",
                "whiteSpace": "pre-wrap",
                "boxShadow": "0px 1px 2px rgba(0,0,0,0.2)",
            },
        ),
        style={
            "textAlign": text_align,
            "margin": "5px 10px",
        },
    )
    return chat_element
