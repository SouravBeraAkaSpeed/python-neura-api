import io
import base64
import sys
from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
from flask_cors import CORS  # Import flask-cors for CORS handling
import subprocess
import seaborn as sns
import os

os.environ["MPLCONFIGDIR"] = "/tmp"

# Set the backend for matplotlib to avoid Tkinter-related issues
plt.switch_backend('Agg')

# Create a Flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000",
     "https://www.toil-labs.com", "https://www.neura.toil-labs.com","https://www.chatmrt.com"])

# Define a route for the home page


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Hello, From Neura Data Analysis Tool!"})




# Define a route to execute Python code

@app.route("/execute", methods=["POST"])
def execute():
    code = request.json.get("code", "")
    output = {"stdout": "", "error": "", "charts": []}

    try:
        # Capture the standard output (print statements)
        captured_output = io.StringIO()
        sys.stdout = captured_output  # Redirect stdout to capture prints

        # Prepare the environment to execute code
        # Provide matplotlib in the execution context
        exec_globals = {"plt": plt}
        exec_locals = {}

        # Execute the code
        exec(code, exec_globals, exec_locals)

        # Capture printed output
        output["stdout"] = captured_output.getvalue()  # Store printed text

        # Check for generated plots and convert to base64
        if plt.get_fignums():
            for fig_num in plt.get_fignums():
                fig = plt.figure(fig_num)
                buf = io.BytesIO()
                fig.savefig(buf, format="png")
                buf.seek(0)
                encoded_image = base64.b64encode(buf.read()).decode("utf-8")
                output["charts"].append(encoded_image)
                buf.close()
                plt.close(fig)  # Close the figure to free memory

        # Reset the standard output
        sys.stdout = sys.__stdout__

        # Capture the result of the code (if any variable or return is present)
        output["stdout"] = output["stdout"] or exec_locals.get(
            "result", "Execution completed successfully.")
    except Exception as e:
        output["error"] = f"An error occurred: {str(e)}"

    response = jsonify(output)
    allowed_origins = ["http://localhost:3000",
                       "https://www.toil-labs.com", "https://www.neura.toil-labs.com"]
    origin = request.headers.get("Origin")

    if origin in allowed_origins:
        response.headers.add('Access-Control-Allow-Origin', origin)

    # Allow other necessary headers
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')

    return response


# Start the server when this script is executed directly
if __name__ == "__main__":
    try:
        app.run(debug=True, threaded=True)
    except Exception as e:
        print(f"Error occurred while starting the Data Analysis process: {e}")
