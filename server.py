from flask import Flask, jsonify
from fapi.utils.utils import *
from os import path

app = Flask(__name__)
model = None


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


if __name__ == "__main__":
    model_path = path.abspath(
        path.join(path.dirname(__file__), "models", "mnist_model_16_16_32_32_1568_64_64.model.gz"))
    model = load_model(model_path)
    model.finalize()
    if not model:
        print("Model not found!")
        exit(1)
    app.run(host='0.0.0.0', port=8080)
