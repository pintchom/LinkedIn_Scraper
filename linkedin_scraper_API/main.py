from flask import Flask, request, jsonify, json
from flask_cors import CORS
from LinkedIn_Scraper import main

app = Flask(__name__)
CORS(app) #Cross Origin Resource Sharing -- Handles multi domain/platform data sharing

@app.route("/link", methods=["POST"]) #link route -- running site through 3000 local port, no need to actually put /link
def create_user():
    data = request.get_json()
    try:
        accountData = main(data['data'])  # calling scraper with user inputted LinkedIn URL
        accountData = json.loads(accountData)  # temp storage of scraper output
        return jsonify(accountData), 200  # POST request response 
    except Exception as e:
        return jsonify({"error": "Bad Link, Try Again"}), 500

if __name__ == '__main__':
    app.run(debug = True) 