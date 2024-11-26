from flask import Flask, jsonify
from ..city_model.model import CityModel
from ..city_model.agents import CarAgent, SemaphoreAgent

model = CityModel(5)
app = Flask(__name__)

@app.route("/positions")
def get_positions():
    data = {"agents":[], "semaphores":{}}
    for agent in model.agents_by_type[CarAgent]:
        data["agents"].append(agent.pos)
    for semaphore in model.agents_by_type[SemaphoreAgent]:
        data["semaphores"].append(semaphore.state)
    model.step()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host ='127.0.0.1', port = 8000, debug=True)