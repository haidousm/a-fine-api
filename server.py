from flask import Flask, jsonify
from fapi.utils.utils import *
from os import path

app = Flask(__name__)
model = None


@app.before_first_request
def _load_model():
    global model
    model_path = path.abspath(
        path.join(path.dirname(__file__), "models", "mnist_conv_16_32_dense_1568_64_64_10_softmax.model.gz"))
    model = load_model(model_path)
    model.finalize()
    if not model:
        print("Model not found!")
        exit(1)


@app.route('/')
@crossdomain(origin='*')
def home_endpoint():
    return 'hey cutie ;)'


@app.route('/predict', methods=['POST'])
@crossdomain(origin='*')
def get_prediction():
    global model
    if request.method == 'POST':
        image_data = request.get_json(force=True)
        image_data = resize_image(image_data)

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
