import os

import boto3
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)


dynamodb_client = boto3.client('dynamodb')

if os.environ.get('IS_OFFLINE'):
    dynamodb_client = boto3.client(
        'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000'
    )


DOCUMENTS_TABLE = os.environ['DOCUMENTS_TABLE']


@app.route('/documents/<string:doc_id>')
def get_document(doc_id):
    result = dynamodb_client.get_item(
        TableName=DOCUMENTS_TABLE, Key={'docId': {'S': doc_id}}
    )
    item = result.get('Item')
    if not item:
        return jsonify({'error': 'Could not find document with provided "docId"'}), 404

    return jsonify(
        {'docId': item.get('docId').get('S'), 'name': item.get('name').get('S')}
    )


@app.route('/documents', methods=['POST'])
def create_document():
    doc_id = request.json.get('docId')
    name = request.json.get('name')
    if not doc_id or not name:
        return jsonify({'error': 'Please provide both "docId" and "name"'}), 400

    dynamodb_client.put_item(
        TableName=DOCUMENTS_TABLE, Item={'docId': {'S': doc_id}, 'name': {'S': name}}
    )

    return jsonify({'docId': doc_id, 'name': name})


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
