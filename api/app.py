from flask import Flask, request, jsonify

# Create a Flask app
app = Flask(__name__)

# Define a route for the home page
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Hello, Vercel!"})

# Define a route to execute Python code (if needed)
@app.route("/execute", methods=["POST"])
def execute():
    code = request.json.get("code", "")
    # Add your logic to handle code execution here
    return jsonify({"result": f"Executed code: {code}"})

# Start the server when this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)
