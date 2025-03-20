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
import aspose.slides as slides
os.environ["MPLCONFIGDIR"] = "/tmp"

# Set the backend for matplotlib to avoid Tkinter-related issues
plt.switch_backend('Agg')

# Create a Flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:3001",
     "https://www.toil-labs.com", "https://www.neura.toil-labs.com"])

# Define a route for the home page


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Hello, From Neura Data Analysis Tool!"})


@app.route("/convert-ppt-to-pdf", methods=["POST"])
def convert_ppt_to_pdf():
    try:
        # Step 1: Get File URI
        data = request.json
        file_uri = data.get("fileUri")
        if not file_uri:
            return jsonify({"error": "fileUri is required"}), 400

        # Step 2: Download the PPT/PPTX file
        pptx_filename = "temp_presentation.pptx"
        pdf_filename = "temp_presentation.pdf"

        response = requests.get(file_uri, stream=True)
        if response.status_code == 200:
            with open(pptx_filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
        else:
            return jsonify({"error": "Failed to download the file"}), 400

        # Step 3: Convert PPTX to PDF using Aspose.Slides
        with slides.Presentation(pptx_filename) as presentation:
            presentation.save(pdf_filename, slides.export.SaveFormat.PDF)

        # Step 4: Read PDF and encode in base64
        with open(pdf_filename, "rb") as pdf_file:
            pdf_base64 = base64.b64encode(pdf_file.read()).decode("utf-8")

        # Clean up files
        os.remove(pptx_filename)
        os.remove(pdf_filename)

        return jsonify({
            "base64": pdf_base64,
            "mimeType": "application/pdf"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
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
    allowed_origins = ["http://localhost:3001",
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
