from flask import Flask, request, jsonify
from dash import Dash, html
import threading
import sqlite3
import signal_hound_control  # Make sure this contains the updated sweep function

# Initialize the Dash app with an external Flask server
server = Flask(__name__)
app = Dash(__name__, server=server)
app.layout = html.Div([])  # Minimal layout

# Global variables for the loop and error handling
is_running = False
sweep_thread = None
last_error = ""

def init_db():
    conn = sqlite3.connect('signal_hound_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sweep_data (
            unix_time INTEGER,
            frequency_MHz INTEGER,
            amp_mW INTEGER
        )
    ''')
    conn.commit()
    conn.close()


def run_sweep():
    global is_running, last_error
    while is_running:
        try:
            signal_hound_control.sweep()  # Calls the sweep function that writes data to the DB
        except Exception as e:
            last_error = str(e)
            print(f"Error during sweep: {e}")
            is_running = False

# Flask route to control the Signal Hound program
@server.route('/control', methods=['POST'])
def control():
    global is_running, sweep_thread, last_error
    command = request.json.get("command")
    
    if command == "start":
        if is_running:
            return jsonify({"message": "already running", "error": last_error})
        else:
            is_running = True
            last_error = ""  # Reset the last error
            sweep_thread = threading.Thread(target=run_sweep)
            sweep_thread.start()
            return jsonify({"message": "started running"})
    elif command == "stop":
        is_running = False
        sweep_thread.join()  # Wait for the sweep thread to finish
        if last_error:
            return jsonify({"message": "stopped with error", "error": last_error})
        return jsonify({"message": "stopped"})
    else:
        return jsonify({"message": "invalid command"})

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run_server(debug=True, port=7000)
