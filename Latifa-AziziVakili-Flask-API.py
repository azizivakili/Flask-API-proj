from flask import Flask, jsonify, request, make_response
from random import uniform
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import base64

app = Flask(__name__)

# Load the credentials dataset
credentials_df = pd.read_csv("credentials.csv")

@app.route("/status", methods=["GET"])
def status():
    # Return 1 to indicate that the API is working
    return jsonify({"status": 1})

@app.route("/welcome", methods=["GET"])
def welcome():
    # Get the username from the query string
    username = request.args.get("username")
    if username:
        return f"Welcome, {username}!", 200
    else:
        return "Please provide a username in the query string.", 400

@app.route("/permissions", methods=["POST"])
def permissions():
    # Get username and password from headers
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return "Authorization header is missing.", 401

    # Decode the authorization header
    try:
        username, password = base64.b64decode(auth_header.split(" ")[1]).decode("utf-8").split(":")
    except:
        return "Invalid Authorization header format.", 401

    # Check if the username and password match
    user = credentials_df[(credentials_df['username'] == username) & (credentials_df['password'] == int(password))]
    if user.empty:
        return "Unauthorized. Incorrect username or password.", 401

    # Extract v1 and v2 permissions
    v1_permission = bool(user['v1'].iloc[0])
    v2_permission = bool(user['v2'].iloc[0])

    # Create response
    response_data = {"v1": v1_permission, "v2": v2_permission}
    response_headers = {"username": username, "v1": str(v1_permission), "v2": str(v2_permission)}

    return jsonify(response_data), 200, response_headers

@app.route("/v1/sentiment", methods=["POST"])
def v1_sentiment():
    # Get the sentence from the request data
    sentence = request.json.get("sentence")
    if not sentence:
        return "Sentence is missing in the request body.", 400

    # Get username and password from headers
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return "Authorization header is missing.", 401

    # Decode the authorization header
    try:
        username, password = base64.b64decode(auth_header.split(" ")[1]).decode("utf-8").split(":")
    except:
        return "Invalid Authorization header format.", 401

    # Check if the username and password match
    user = credentials_df[(credentials_df['username'] == username) & (credentials_df['password'] == int(password))]
    if user.empty:
        return "Unauthorized. Incorrect username or password.", 401

    # Check if the user has access to v1
    v1_permission = bool(user['v1'].iloc[0])
    if not v1_permission:
        return "Unauthorized. User does not have access to v1.", 403

    # Return a random sentiment score between -1 and 1
    sentiment_score = uniform(-1, 1)
    return jsonify({"sentiment_score": sentiment_score}), 200

@app.route("/v2/sentiment", methods=["POST"])
def v2_sentiment():
    # Get the sentence from the request data
    sentence = request.json.get("sentence")
    if not sentence:
        return "Sentence is missing in the request body.", 400

    # Get username and password from headers
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return "Authorization header is missing.", 401

    # Decode the authorization header
    try:
        username, password = base64.b64decode(auth_header.split(" ")[1]).decode("utf-8").split(":")
    except:
        return "Invalid Authorization header format.", 401

    # Check if the username and password match
    user = credentials_df[(credentials_df['username'] == username) & (credentials_df['password'] == int(password))]
    if user.empty:
        return "Unauthorized. Incorrect username or password.", 401

    # Check if the user has access to v2
    v2_permission = bool(user['v2'].iloc[0])
    if not v2_permission:
        return "Unauthorized. User does not have access to v2.", 403

    # Initialize the Vader sentiment analyzer
    analyzer = SentimentIntensityAnalyzer()
    # Perform sentiment analysis and get the compound score
    sentiment_scores = analyzer.polarity_scores(sentence)
    compound_score = sentiment_scores["compound"]
    return jsonify({"sentiment_score": compound_score}), 200

if __name__ == "__main__":
    app.run(debug=True)
