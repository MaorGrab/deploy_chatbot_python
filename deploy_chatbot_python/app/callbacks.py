import json
from dataclasses import dataclass

import dash
from dash import callback, Input, Output, State
import requests

from deploy_chatbot_python.app.layout import make_chat_element
from deploy_chatbot_python.api.server import Query
import deploy_chatbot_python.config.constants as constants


@dataclass
class Callbacks:
    app: dash.Dash

    def __post_init__(self):
        self._register_callbacks()

    def _register_callbacks(self) -> None:
        # Callback to handle user input and update chat history with user's message and placeholder
        @self.app.callback(
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
            chat_data.append({"sender": "bot", "message": constants.BOT_PLACEHOLDER_MESSAGE})

            return chat_data, "", ""

        # Callback to fetch bot response and update the placeholder
        @self.app.callback(
            Output("chat-store", "data", allow_duplicate=True),
            Input("chat-store", "data"),
            prevent_initial_call=True,
        )
        def fetch_bot_response(chat_data):
            if not chat_data or (chat_data[-1]["sender"] != "bot"):
                return chat_data
            # Check if the last message is a placeholder
            if chat_data[-1]["message"] == constants.BOT_PLACEHOLDER_MESSAGE:
                # Extract the user's message
                user_message = chat_data[-2]["message"]

                try:
                    # Send POST request to backend API
                    response = requests.post(
                        url=constants.API_POST_ENDPOINT_URL,
                        json=Query(text=user_message).model_dump(),
                        timeout=constants.POST_REQUEST_TIMEOUT,
                    )
                    response.raise_for_status()
                    data = response.json()
                    bot_reply = data.get("response", "No response received.")
                except requests.exceptions.RequestException as e:
                    bot_reply = f"An error occurred: {str(e)}"
                except json.JSONDecodeError:
                    bot_reply = "Received an invalid JSON response from the server."
                except Exception:
                    bot_reply = "An error has occured. Please contact the creator of this Chatbot"
                    raise

                # Update the placeholder with the actual bot response
                chat_data[-1]["message"] = bot_reply

            return chat_data

        # Callback to render chat history
        @self.app.callback(
            Output("chat-history", "children"),
            Input("chat-store", "data"),
        )
        def render_chat_history(chat_data):
            chat_elements = []
            for msg in chat_data:
                is_user = msg["sender"] == 'user'
                text_align = "right" if is_user else "left"
                bubble_color = "#DCF8C6" if text_align == 'right' else "#FFFFFF"
                chat_element = make_chat_element(msg['message'], text_align, bubble_color)
                chat_elements.append(chat_element)
            return chat_elements
