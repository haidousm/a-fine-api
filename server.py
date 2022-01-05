import cv2
import numpy as np
import pyparsing

from utils.Model import Model
from datetime import timedelta
from flask import Flask, make_response, request, current_app, jsonify
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))

    if not isinstance(origin, pyparsing.basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """ Determines which methods are allowed
        """
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        """The decorator function
        """

        def wrapped_function(*args, **kwargs):
            """Caries out the actual cross domain code
            """
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)

    return decorator


model = None
app = Flask(__name__)


def load_model():
    global model
    model = Model.load('')


@app.route('/')
def home_endpoint():
    return 'hey cutie ;)'


@app.route('/predict', methods=['POST', 'GET'])
@crossdomain(origin='*')
def get_prediction():
    global model
    if request.method == 'POST':
        image_data = request.get_json(force=True)
        image_data = np.array(image_data).astype(np.float32) / 255
        image_data = cv2.resize(image_data, dsize=(28, 28))
        image_data = np.expand_dims(image_data, axis=0)
        image_data = np.expand_dims(image_data, axis=0)

        confidences = model.predict(image_data)
        prediction = model.output_layer_activation.predictions(confidences)

        prediction = int(prediction[0])
        confidence = confidences[0].tolist()
        response = make_response(
            jsonify(
                {"prediction": prediction, "confidence": confidence}
            ),
            200,
        )
        response.headers["Content-Type"] = "application/json"

        return response
    else:
        return "nothing to GET here, ahahaha GET it? ok."


if __name__ == "__main__":
    load_model()
    app.run()

