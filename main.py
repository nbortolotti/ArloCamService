import base64
import logging
import requests

import time
from flask import Flask, render_template, request, jsonify, make_response
from pyarlo import PyArlo

app = Flask(__name__)

# entry point method
@app.route('/')
def arlo_snapshot():
    return render_template('index.html', **locals())


# method designed to extract the config data from a file.
def read_file(filename, string=True):
    with open(filename, 'rb') as input:
        ciphertext = input.read()
        plaintext = base64.b64decode(ciphertext)
        if string:
            return plaintext.decode('utf8')


# objective: method designed to connect  and pass a picture to TensorPhotoXRay.
def connect_tensor_xray():
    try:
        arlo = PyArlo('user', read_file("pass.txt"))
        cam = arlo.cameras[2]
        cam.schedule_snapshot()

        time.sleep(3)

        r = requests.get("url_endpoint" + cam.snapshot_url)  # todo: change for a post call
        return r
    except Exception as e:
        return [{"error"}]


def connect_tensor_xray_testing():
    # todo: use if needed check a typical response.
    try:
        return [{"person": 97}, {"chair": 95}, {"person": 95}, {"couch": 92}, {"chair": 82}, {"tv": 81}, {"tv": 81}, {"chair": 79}, {"dog": 76}, {"book": 65}]
    except Exception as e:
        return [{"error"}]


# objective: Google Assistant structure method using use a particular cam, to take a picture and provide
# the picture to TensorPhotoXRay service.
@app.route('/arlo', methods=['POST'])
def tensor_photo():
    try:
        # connect to Arlo using PyArlo library.

        req = request.get_json(silent=True, force=True)
        action = req.get('result').get('action')

        # detect action from DialogFlow agent description.
        if action == 'image.analysis':

            tags = connect_tensor_xray() # method to use the integration to TensorPhotoXRay

            for element in tags:
                for key, value in element.iteritems():
                    if "dog" in key:
                        # Compose the response to API.AI
                        res = {'speech': 'Your pet is inside your house in the main room',
                               'displayText': 'Your pet is inside your house in the main room',
                               'contextOut': req['result']['contexts']}


            if res != {'speech': 'Your pet is inside your house in the main room',
                       'displayText': 'Your pet is inside your house in the main room',
                       'contextOut': 'demo'}:
                res = {'speech': 'I can not find your pet at home',
                       'displayText': 'I can not find your pet at home',
                       'contextOut': 'demo'}
        else:
            res = {'speech': 'nothing', 'displayText': 'nothing'}

        final = make_response(jsonify(res))
        return final

    except Exception as e:
        res = {'speech': 'error', 'displayText': 'error'}
        final = make_response(jsonify(res))
        return final


@app.route('/arlo2', methods=['GET'])
def tensor_photo2():
    try:

        tags = connect_tensor_xray_testing()

        for element in tags:
            for key, value in element.iteritems():
                if "dog" in key:
                    # Compose the response to API.AI
                    res = {'speech': 'Your pet is inside your house in the main room',
                           'displayText': 'Your pet is inside your house in the main room',
                           'contextOut': 'demo'}

        if res != {'speech': 'Your pet is inside your house in the main room',
                   'displayText': 'Your pet is inside your house in the main room',
                   'contextOut': 'demo'}:
            res = {'speech': 'I can not find your pet at home',
                   'displayText': 'I can not find your pet at home',
                   'contextOut': 'demo'}


        final = make_response(jsonify(res))
        return final

    except Exception as e:
        res = {'speech': 'error', 'displayText': 'error'}
        final = make_response(jsonify(res))
        return final


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
