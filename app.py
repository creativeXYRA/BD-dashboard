import os
import dash
from dash import html, dcc
import logging

# Set up logging to help with debugging
logging.basicConfig(level=logging.INFO)
logging.info("Starting the Dash application...")

# Get the port from the environment variable provided by Cloud Run
port = int(os.environ.get('PORT', 8080))
logging.info(f"Using port: {port}")

# Create the Dash app instance
app = dash.Dash(__name__)
server = app.server

# Define a simple health check endpoint
@server.route('/_ah/health')
def health_check():
    """Google Cloud health check endpoint."""
    logging.info("Health check endpoint hit.")
    return 'ok', 200

# Define the layout of the dashboard
app.layout = html.Div(
    className="container mx-auto p-4",
    children=[
        html.H1("Hello, Cloud Run!", className="text-4xl font-bold text-center text-blue-600 mb-4"),
        html.P("Your Dash app is running.", className="text-center text-gray-700 mb-6"),
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )
    ]
)

# The server runs on the port specified by Cloud Run's environment variable.
if __name__ == '__main__':
    logging.info("Running the server locally.")
    app.run_server(host='0.0.0.0', port=port, debug=False)

