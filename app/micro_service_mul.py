import os

import requests
from flask import Flask, request

from app.lib.arithmetic import my_mul
from app.messages import make_response
from app import config

app = Flask(__name__)

@app.route('/', methods=["GET"])
def health_check():
    payload = {
                "message": "welcome to the example microservice mul",
                "status": "success"
            }
    return make_response(payload, 200)


@app.route('/mul', methods=["POST"])
def mul():
    l = request.get_json()['list']
    payload = {
        "message": "my mul function from microservice",
        "status": "success",
        "result" : my_mul(*l),
    }
    return make_response(payload)

@app.route('/both', methods=["POST"])
def both():
    l = request.get_json()['list']
    payload = {
        "message": "my mul function from microservice",
        "status": "success",
        "result" : my_mul(*l),
    }
    r_payload = {
            "list": l
    }
    response = requests.post(f'http://{config.SUM_HOST}:{config.SUM_PORT}/sum', json=r_payload).json()
    payload["sum"] = response
    return make_response(payload)



if __name__ == "__main__":
    app.run(
        debug=config.DEBUG_MODE, host="0.0.0.0", port=os.getenv('PORT', config.MUL_PORT)
        )
