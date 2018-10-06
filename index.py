from flask import Flask, render_template, request, jsonify
from interactive import myprocess
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route("/", methods=['POST'])
def predict():

    return jsonify(myprocess(request.get_json().get('query'),request.get_json().get('k')))

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)
