import logging
import mesa
import numpy as np
from mesa.visualization import Slider, SolaraViz, make_space_component
from model import CityModel
from agents import SemaphoreAgent, CarAgent

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Definir los parámetros del modelo
model_params = {
    "car_count": {
        "type": "SliderInt",
        "value": 10,
        "label": "Number of Cars",
        "min": 1,
        "max": 50,
        "step": 1,
    }
}

# Definir cómo se visualizarán los agentes
def agent_portrayal(agent):
    try:
        if isinstance(agent, SemaphoreAgent):
            portrayal = {"size": 6, "color": "green" if agent.state else "red", "shape": "circle"}
        elif isinstance(agent, CarAgent):
            portrayal = {"size": 4, "color": "blue", "shape": "circle"}
        else:
            portrayal = {}
        logger.debug(f"Agent portrayal: {agent} -> {portrayal}")
        return portrayal
    except Exception as e:
        logger.error(f"Error in agent portrayal: {e}")
        return {}

# Configurar capas para visualización
propertylayer_portrayal = {
    "structure": {"color": "gray", "alpha": 0.5, "colorbar": False},
    "parking_spot": {"color": "yellow", "alpha": 0.5, "colorbar": False},
    "semaphore": {"color": "orange", "alpha": 0.5, "colorbar": False},
}

# Crear modelo inicial
try:
    logger.debug("Initializing CityModel...")
    model = CityModel(car_count=model_params["car_count"]["value"])
    logger.info("CityModel initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing CityModel: {e}")
    raise

# Crear componente de espacio
try:
    logger.debug("Creating space component...")
    space_graph = make_space_component(agent_portrayal, propertylayer_portrayal)
    logger.info("Space component created successfully.")
except Exception as e:
    logger.error(f"Error creating space component: {e}")
    raise

# Configurar visualización con SolaraViz
try:
    logger.debug("Setting up SolaraViz...")
    page = SolaraViz(
        model,
        components=[space_graph],
        model_params=model_params,
        name="City Model with Cars and Semaphores",
    )
    logger.info("SolaraViz setup successfully.")
except Exception as e:
    logger.error(f"Error setting up SolaraViz: {e}")
    raise

# Ensure `page` is exposed for the server
try:
    logger.debug("Exposing the page object...")
    page  # This must be the last line to make the page accessible.
    logger.info("Page object exposed successfully.")
except Exception as e:
    logger.error(f"Error exposing the page object: {e}")
    raise
