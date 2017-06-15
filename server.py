#!flask/bin/python

from flask import Flask, request, Response
import json
import sys
import SQLQuery

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api/search', methods=['GET'])
def api_search():
    # Term that the user typed in the search bar
    term = request.args['q'] if 'q' in request.args else None

    term = term.replace('"', '').replace ('\'', '')
    #print (term)
    # The response should look like this and should depend on the term
    # example_response = {'total_count': 2, 'items': [{'id': '01', 'name': 'unfresh salad'}, {'id': '02', 'name': 'chicken'}]}
    response = SQLQuery.searchFoodByText(term)
    resp = Response(json.dumps(response), 
        mimetype='application/json')

    # Allow X-origin
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@app.route('/api/optimiser', methods=['GET'])
def api_optimiser():
    # Term that the user typed in the search bar
    data = request.args['data'] if 'data' in request.args else None

    response = {'valid': True, 'items': [{'id': '123', 'name': 'salad', 'calories': 34, 'fibre': 12, 'iron': 3, 'amount': 0.5}]}
    resp = Response(json.dumps(response), 
        mimetype='application/json')

    # Allow X-origin
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

@app.route('/api/product', methods=['GET'])
def api_product():
    # Term that the user typed in the search bar
    product_id = request.args['id'] if 'id' in request.args else None

    response = SQLQuery.searchFoodNutritionByID(product_id)
    resp = Response(json.dumps(response), 
        mimetype='application/json')

    # Allow X-origin
    resp.headers['Access-Control-Allow-Origin'] = '*'

    return resp

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')