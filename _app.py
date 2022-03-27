import io
from datetime import datetime

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS, cross_origin

import db.diagrams_db as db
from generate import generate_diagram

import os, os.path

from utils import image_cleanup

app = Flask(__name__)
cors = CORS(app, resources={r"http://localhost:3000/*": {"origins": "*"}})

@app.route('/diagram', methods=['POST'])
@cross_origin()
def diagram():
    request_data = request.get_json()

    result = generate_diagram(request_data)
    if isinstance(result, SyntaxError) or isinstance(result, SyntaxWarning):
        image_cleanup()
        return jsonify(message="Unrecognised Syntax"), 500
    if isinstance(result, NameError):
        image_cleanup()
        return jsonify(message=str(result)), 500
    if isinstance(result, TypeError):
        image_cleanup()
        return jsonify(message=str(result)), 500
    if isinstance(result, ImportError):
        image_cleanup()
        return jsonify(message="Imports already handled by application"), 500

    try:
        return_data = io.BytesIO()
        with open(result, 'rb') as fo:
            return_data.write(fo.read())
        # (after writing, cursor will be at last byte, so move it to start)
        return_data.seek(0)
        os.remove(result)
        response = send_file(return_data, mimetype='image/png')
    except Exception as e:
        response = e.__str__()

    return response


@app.route('/diagram/save', methods=['POST'])
@cross_origin()
def save_diagram():
    request_data = request.get_json()
    name = request_data['name']
    diagram_as_code = request_data['diagramCode']
    timestamp = datetime.now()

    diagram_details = {'name': name, 'code': diagram_as_code, 'timestamp': timestamp}

    result = db.save_diagrams_as_code(diagram_details)

    if result:
        response = {
            "response": "Diagram Saved Successfully"
        }
    else:
        response = {
            "response": "Error Saving Diagram"
        }

    return response

@app.route('/diagram/loadalldiagrams', methods=['GET'])
@cross_origin()
def load_all():
    loaded_diagrams = db.load_all_diagrams_as_code()
    diagrams = {}
    index = 0
    for document in loaded_diagrams:
        diagrams[index] = document['name']
        index += 1
    print(loaded_diagrams)
    return diagrams


@app.route('/diagram/loaddiagram', methods=['POST'])
@cross_origin()
def load_one():
    diagram_name = request.get_json()
    load_diagram = db.load_diagrams_as_code_by_name(diagram_name)

    if load_diagram is not False:
        diagram_data = {
            "name": load_diagram['name'],
            "code": load_diagram['code'],
        }
        return diagram_data
    else:
        return {
            "response": "Error Loading Diagrams as Code"
        }


if __name__ == '__main__':
    app.run(debug=True, port=5001)
