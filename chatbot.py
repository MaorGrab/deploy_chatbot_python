import json

import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import requests

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Chatbot Dashboard"

# Define the layout of the app
app.layout = dbc.Container(
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

# Callback to handle user input and update chat history with user's message and placeholder
@app.callback(
    Output("chat-store", "data"),
    Output("user-input", "value"),
    Output("error-message", "children"),
    Input("send-button", "n_clicks"),
    Input("user-input", "n_submit"),
    State("user-input", "value"),
    State("chat-store", "data"),
    prevent_initial_call=True,
)
def update_chat(n_clicks, n_submit, user_message, chat_data):  # pylint: disable=unused-argument
    if not user_message:
        return dash.no_update, dash.no_update, "Please enter a message before sending."

    if not chat_data:
        chat_data = []

    # Append user's message
    chat_data.append({"sender": "user", "message": user_message})

    # Append placeholder for bot's response
    chat_data.append({"sender": "bot", "message": "Typing..."})

    return chat_data, "", ""

# Callback to fetch bot response and update the placeholder
@app.callback(
    Output("chat-store", "data", allow_duplicate=True),
    Input("chat-store", "data"),
    prevent_initial_call=True,
)
def fetch_bot_response(chat_data):
    # Check if the last message is a placeholder
    if chat_data and chat_data[-1]["sender"] == "bot" and chat_data[-1]["message"] == "Typing...":
        # Extract the user's message
        user_message = chat_data[-2]["message"]

        try:
            # Send POST request to backend API
            response = requests.post(
                "http://localhost:8000/query",
                json={"text": user_message},
                timeout=60,
            )
            response.raise_for_status()
            data = response.json()
            bot_reply = data.get("response", {}).get("response", "No response received.")
        except requests.exceptions.RequestException as e:
            bot_reply = f"An error occurred: {str(e)}"
        except json.JSONDecodeError:
            bot_reply = "Received an invalid JSON response from the server."

        # Update the placeholder with the actual bot response
        chat_data[-1]["message"] = bot_reply

    return chat_data

# Callback to render chat history
@app.callback(
    Output("chat-history", "children"),
    Input("chat-store", "data"),
)
def render_chat_history(chat_data):
    chat_elements = []
    for msg in chat_data:
        alignment = "right" if msg["sender"] == "user" else "left"
        chat_elements.append(
            html.Div(
                f"{msg['sender'].capitalize()}: {msg['message']}",
                style={"textAlign": alignment, "margin": "5px"},
            )
        )
    return chat_elements

if __name__ == "__main__":
    app.run(debug=True)
