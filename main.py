import base64
import logging
import time

from flask import Flask, render_template, request, jsonify, make_response
from Arlo import Arlo


app = Flask(__name__)


@app.route('/')
def arlo_snapshot():
    return render_template('index.html', **locals())

def read_file(filename, string=True):
    with open(filename, 'rb') as input:
        ciphertext = input.read()
        plaintext = base64.b64decode(ciphertext)
        if string:
            return plaintext.decode('utf8')

@app.route('/arlo/', methods=['POST'])
def tensor_photo():
    USERNAME = 'user'
    PASSWORD = read_file("pass.txt")

    try:
        arlo = Arlo(USERNAME, PASSWORD)

        cameras = arlo.GetDevices('camera')

        # Take the snapshot.
        arlo.TakeSnapshot(cameras[2])

        # Compose the response to API.AI
        res = {'speech': 'yes',
               'displayText': 'yes'}

        return make_response(jsonify(res))

    except Exception as e:
        res = {'speech': 'error', 'displayText': 'error'}
        return make_response(jsonify(res))


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
