from dash import html, dcc
import dash_bootstrap_components as dbc


layout = dbc.Container(
    [
        html.H2("🤖 Chatbot Interface", className="text-center my-4"),
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
                                placeholder="Type your message here...",
                                type="text",
                                debounce=True,
                                style={"width": "90%"},
                            ),
                            dbc.Button(
                                "Send",
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

def make_chat_element(msg: str, alignment: str) -> html.Div:
    chat_element = html.Div(
        f"{msg['sender'].capitalize()}: {msg['message']}",
        style={"textAlign": alignment, "margin": "5px"},
        )
    return chat_element