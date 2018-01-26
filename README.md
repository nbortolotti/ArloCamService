# Arlo Cam Service
 Project that aims to provide a set of services to interact with
 [Arlo](https://www.arlo.com) systems.

# Architecture
The project proposes an architecture based on App Engine Flexible environment.
The mechanism of interaction in Gunicorn and Flask

# UC covering webhook to response Google Assistant Agent action

```
@app.route('/arlo', methods=['POST'])
def tensor_photo():
    try:
        # connect to Arlo using PyArlo library.
        arlo = PyArlo('user', read_file("pass.txt"))

        req = request.get_json(silent=True, force=True)
        action = req.get('result').get('action')

        # detect action from DialogFlow agent description.
        if action == 'image.analysis':
            cam = arlo.cameras[2]
            cam.schedule_snapshot()

            tags = connect_tensor_xray(cam.snapshot_url)
            for element in tags:
                for key, value in element.iteritems():
                    if "dog" in key:
                        res = {'speech': 'Your pet is inside your house in the main room',
                               'displayText': 'Your pet is inside your house in the main room',
                               'contextOut': req['result']['contexts']}
        else:
            res = {'speech': 'error', 'displayText': 'error'}

        final = make_response(jsonify(res))
        return final
```
