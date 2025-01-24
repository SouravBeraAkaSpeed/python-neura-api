from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Hello, Vercel!"})

@app.route("/execute", methods=["POST"])
def execute():
    code = request.json.get("code", "")
    # Example response; replace with actual Jupyter kernel execution
    return jsonify({"result": f"Executed code: {code}"})

# Vercel's serverless requires this
def handler(event, context):
    from flask_lambda import FlaskLambda
    lambda_app = FlaskLambda(app)
    return lambda_app(event, context)
