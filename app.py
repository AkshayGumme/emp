import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import mysql.connector

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the web app
app.layout = dbc.Container(
    [
        html.H1("Employee Database"),
        dbc.Input(id='username-input', type='text', placeholder='Enter username'),
        dbc.Input(id='id-input', type='text', placeholder='Enter ID'),
        dbc.Button('Submit', id='submit-button', n_clicks=0, color='primary', className='mt-3'),
        html.Div(id='output-message', className='mt-3')
    ],
    fluid=True
)

# MySQL database connection
db_config = {
    'host': 'mydatabase.cpghpon9delb.us-east-1.rds.amazonaws.com',
    'user': 'admin1',
    'password': 'amulya123',
    'database': 'employee',
}

# Define a function to update the database with user input
def update_database(username, user_id):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    try:
        # Use placeholders for values to prevent SQL injection
        cursor.execute("INSERT INTO empdetail (username, user_id) VALUES (%s, %s)", (username, user_id))
        connection.commit()
        return "Record added successfully!"
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        cursor.close()
        connection.close()

# Define callback to update the database when the button is clicked
@app.callback(
    Output('output-message', 'children'),
    [Input('submit-button', 'n_clicks')],
    [Input('username-input', 'value'),
     Input('id-input', 'value')]
)
def update_database_callback(n_clicks, username, user_id):
    if n_clicks > 0:
        return update_database(username, user_id)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
