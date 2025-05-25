import json

import dash
from dash import callback, Input, Output, State
import requests

from src.app.layout import make_chat_element


# Callback to handle user input and update chat history with user's message and placeholder
@callback(
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
@callback(
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
@callback(
    Output("chat-history", "children"),
    Input("chat-store", "data"),
)
def render_chat_history(chat_data):
    chat_elements = []
    for msg in chat_data:
        alignment = "right" if msg["sender"] == "user" else "left"
        chat_elements.append(make_chat_element(msg, alignment))
    return chat_elements