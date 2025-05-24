import dash
import dash_bootstrap_components as dbc

import callbacks
from layout import layout

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Chatbot Dashboard"

app.layout = layout

if __name__ == "__main__":
    app.run(debug=True)