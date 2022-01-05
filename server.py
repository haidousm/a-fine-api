from flask import Flask
from fapi.utils.utils import *

app = Flask(__name__)


@app.route('/')
@crossdomain(origin='*')
def home_endpoint():
    return 'hey cutie ;)'


if __name__ == "__main__":
    app.run(host='0.0.0.0')
