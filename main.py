import base64
import logging

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


@app.route('/arlo', methods=['POST'])
def tensor_photo():
    USERNAME = 'user'
    PASSWORD = read_file("pass.txt")

    try:

        req = request.get_json(silent=True, force=True)
        action = req.get('result').get('action')

        if action == 'image.analysis':
            arlo = Arlo(USERNAME, PASSWORD)

            cameras = arlo.GetDevices('camera')

            # Take the snapshot.
            arlo.TakeSnapshot(cameras[2])

            # Compose the response to API.AI

            res = {'speech': 'I found your pet',
                   'displayText': 'I found your pet',
                   'contextOut': req['result']['contexts']}

        else:

            res = {'speech': 'error', 'displayText': 'error'}

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
