from fine.datasets import load_mnist
from fine.models import Sequential

from fine.layers import Conv2D
from fine.layers import MaxPool2D
from fine.layers import Flatten
from fine.layers import Dense

from fine.activations import ReLU
from fine.activations import Softmax

from fine.loss import CategoricalCrossEntropy

from fine.models.model_utils import Categorical

from fine.optimizers import Adam

from os import path

if __name__ == "__main__":
    X_train, y_train, X_test, y_test = load_mnist()

    model = Sequential(
        layers=[
            Conv2D(16, (1, 3, 3)),
            ReLU(),
            Conv2D(16, (16, 3, 3)),
            ReLU(),
            MaxPool2D((2, 2)),

            Conv2D(32, (16, 3, 3)),
            ReLU(),
            Conv2D(32, (32, 3, 3)),
            ReLU(),
            MaxPool2D((2, 2)),

            Flatten(),
            Dense(1568, 64),
            ReLU(),
            Dense(64, 64),
            ReLU(),
            Dense(64, 10),
            Softmax()
        ],
        loss=CategoricalCrossEntropy(),
        optimizer=Adam(decay=1e-3),
        accuracy=Categorical()
    )

    model.finalize()
    model.train(X_train, y_train, epochs=1, batch_size=120, print_every=100)
    model.evaluate(X_test, y_test, batch_size=120)

    # get abs path to save model
    save_path = path.abspath(
        path.join(path.dirname(__file__), "..", "..", "models", "mnist_model_16_16_32_32_1568_64_64.model"))
    model.save(save_path)
