# Arlo Cam Service
 Project that aims to provide a set of services to interact with
 [Arlo](https://www.arlo.com) systems.

# Architecture
The project proposes an architecture based on App Engine Flexible environment.
The mechanism of interaction in Gunicorn and Flask

# UC covering webhook to response Google Assistant Agent action

```
def connect_tensor_xray():
    try:
        arlo = PyArlo('user', read_file("pass.txt"))  # connect to pyarlo library
        cam = arlo.cameras[2]  # selecting cam
        cam.schedule_snapshot()  # take picture

        time.sleep(3) # wait if is necesarry

        r = requests.get("url_endpoint" + cam.snapshot_url) 
        return r
    except Exception as e:
        return [{"error"}]


@app.route('/arlo', methods=['POST'])
def tensor_photo():
   try:
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

        else:
            res = {'speech': 'nothing', 'displayText': 'nothing'}

        final = make_response(jsonify(res))
        return final
```
