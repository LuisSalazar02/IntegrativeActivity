from flask import Flask, jsonify
from flask_cors import CORS  # Importa CORS
from ..city_model.model import CityModel
from ..city_model.agents import CarAgent, SemaphoreAgent

model = CityModel(5)
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Habilita CORS para todas las rutas

@app.route("/step", methods=['GET'])
def update_step():
    # Obtener posiciones de los agentes tipo CarAgent
    agents_data = []
    for agent in model.agents_by_type[CarAgent]:
        agents_data.append({"x": agent.pos[0] * 10, "y": agent.pos[1] * 10})

    # Obtener estados de los semáforos tipo SemaphoreAgent
    semaphores_data = []
    for semaphore in model.agents_by_type[SemaphoreAgent]:
        semaphores_data.append(semaphore.state)

    data = {
        "agents": agents_data,
        "semaphores": semaphores_data
    }
    
    model.step()

    return jsonify(data)

if __name__ == "__main__":
    app.run(host ='127.0.0.1', port=5000, debug=True)