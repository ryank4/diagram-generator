import io

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS, cross_origin

from generate import generate_diagram

import os, os.path

from utility import image_cleanup

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
        return jsonify(message="Imports not allowed"), 500

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



if __name__ == '__main__':
    app.run(debug=True)