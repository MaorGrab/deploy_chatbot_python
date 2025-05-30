import dash
import dash_bootstrap_components as dbc

from deploy_chatbot_python.frontend.callbacks import Callbacks
from deploy_chatbot_python.frontend.layout import layout
from deploy_chatbot_python.config import constants

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = constants.APP_TITLE

app.layout = layout
Callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
