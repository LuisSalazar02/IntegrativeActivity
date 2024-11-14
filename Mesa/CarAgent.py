import mesa
import seaborn as sns
import numpy as np
import pandas as pd

class CarAgent(mesa.Agent):
    def __init__(self, model):
        self.speed = 1