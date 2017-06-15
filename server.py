#!flask/bin/python
from flask import Flask, request, Response
import json

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api', methods=['GET'])
def api():
    # Term that the user typed in the search bar
    term = request.args['q'] if 'q' in request.args else None

    # The response should look like this and should depend on the term
    example_response = {'total_count': 2, 'items': [{'id': '01', 'name': 'unfresh salad'}, {'id': '02', 'name': 'chicken'}]}
    resp = Response(json.dumps(example_response), 
        mimetype='application/json')

    # Allow X-origin
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

if __name__ == '__main__':
    app.run(debug=False)