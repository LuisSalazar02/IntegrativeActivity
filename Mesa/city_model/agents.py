import mesa

class CarAgent(mesa.Agent):
    def __init__(self, model):
        self.speed = 1

class SemaphoreAgent(mesa.Agent):
    def __init__(self, model, controlled_cells, state):
        # A state equal to True means green
        self.state = state
        self.controlled_cells = controlled_cells
        for cell in self.controlled_cells:
            model.grid.properties["semaphore"].set_cell(cell, self.state)

    def toggle_state(self):
        if model.global_steps % 5 == 0:
            self.state = not self.state
            for cell in self.controlled_cells:
                model.grid.properties["semaphore"].set_cell(cell, self.state)