from flask import Flask, jsonify, Response
from ..city_model.model import CityModel
from ..city_model.agents import CarAgent, SemaphoreAgent

model = CityModel(5)
app = Flask(__name__)

@app.route("/positions")
def get_positions():
    data = []
    for agent in model.agents_by_type[CarAgent]:
        data.append({"x": agent.pos[0], "z": agent.pos[1]})
    return jsonify(data)

@app.route("/states")
def get_states():
    data = []
    for semaphore in model.agents_by_type[SemaphoreAgent]:
        data.append({"state": semaphore.state})
    return jsonify(data)

@app.route("/step")
def update_step():
    model.step()
    return Response(status=200)

if __name__ == "__main__":
    app.run(host ='127.0.0.1', port = 8000, debug=True)