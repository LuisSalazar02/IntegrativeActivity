import mesa
from .agents import SemaphoreAgent

class CityModel(mesa.Model):
    def __init__(self, car_count, seed=None):
        super().__init__(seed=seed)
        self.width = 24
        self.height = 24
        self.structure_arr = [
            (2,2), (3,2), (4,2), (5,2), (6,2), (7,2), (8,2), (10,2), (11,2), (16,2), (17,2), (20,2), (21,2),
            (3,3), (4,3), (5,3), (6,3), (7,3), (8,3), (9,3), (10,3), (11,3), (16,3), (20,3), (21,3),
            (2,4), (3,4), (4,4), (5,4), (6,4), (7,4), (8,4), (9,4), (10,4), (16,4), (17,4), (21,4),
            (2,5), (3,5), (4,5), (5,5), (7,5), (8,5), (9,5), (10,5), (11,5), (16,5), (17,5), (20,5), (21,5),
            (2,8), (3,8), (4,8), (7,8), (9,8), (10,8), (11,8), (16,8), (17,8), (20,8), (21,8),
            (2,9), (3,9), (4,9), (7,9), (8,9), (9,9), (10,9), (11,9), (16,9), (17,9), (20,9),
            (2,10), (3,10), (7,10), (8,10), (9,10), (10,10), (17,10), (20,10), (21,10),
            (2,11), (3,11), (7,11), (8,11), (9,11), (10,11), (11,11), (16,11), (17,11), (20,11), (21,11),
            (13,13), (14,13),
            (13,14), (14,14),
            (2,16), (3,16), (4,16), (5,16), (8,16), (9,16), (10,16), (11,16), (16,16), (17,16), (18,16), (19,16), (20,16), (21,16),
            (3,17), (4,17), (5,17), (8,17), (9,17), (10,17), (11,17), (16,17), (18,17), (20,17), (21,17),
            (2,18), (3,18), (4,18), (5,18), (8,18), (9,18), (10,18), (11,18),
            (2,19), (3,19), (4,19), (5,19), (8,19), (9,19), (10,19), (11,19),
            (2,20), (3,20), (4,20), (9,20), (10,20), (11,20), (16,20), (17,20), (18,20), (20,20), (21,20),
            (2,21), (3,21), (4,21), (5,21), (8,21), (9,21), (10,21), (11,21), (16,21), (17,21), (18,21), (19,21), (20,21), (21,21)
        ]
        self.parking_spot_dict = {
            1:[(9,2), (2,3), (11,4), (6,5)],
            2:[(4,10)],
            3:[(8,8), (11,10)],
            4:[(2,17), (5,20)],
            5:[(8,20)],
            6:[(17,3)],
            7:[(20,4)],
            8:[(16,10)],
            9:[(21,9)],
            10:[(17,17), (19,17)],
            11:[(19,20)]
        }
        self.semaphore_arr = [
            [[(17, 0), (17, 1)], True],
            [[(2,6), (2,7)], True],
            [[(7,6), (7,7)], True],
            [[(21,6), (21,7)], True],
            [[(16, 19), (16, 20)], True],
            [[(1,8), (0,8)], False],
            [[(6,8), (5,8)], False],
            [[(15,17), (14,17)], False],
            [[(19,2), (18,2)], False],
            [[(23,5), (22,5)], False]
        ]
        global_steps = 0
        self.structure_layer = mesa.space.PropertyLayer("structure", self.width, self.height, 0)
        self.parking_spot_layer = mesa.space.PropertyLayer("parking_spot", self.width, self.height, 0)
        self.semaphore_layer = mesa.space.PropertyLayer("semaphore", self.width, self.height, 0)
        self.grid = mesa.space.MultiGrid(self.width, self.height, False, (self.structure_layer, self.parking_spot_layer, self.semaphore_layer))
        self.running = True
        self.datacollector = mesa.DataCollector()

        # Create building grid
        for x, y in self.structure_arr:
            self.grid.properties["structure"].set_cell((x, y), 1)

        # Create parking spot grid
        for key, value in self.parking_spot_dict.items():
            for x, y in value:
                self.grid.properties["parking_spot"].set_cell((x, y), key)

        # Create semaphore agents
        for values in self.semaphore_arr:
            SemaphoreAgent(self, values[0], values[1])
        
        def step(self):
            self.datacollector.collect(self)
            global_steps += 1
            semaphore_agents = model.agents_by_type(SemaphoreAgent)
            for agent in semaphore_agents:
                agent.shuffle_do("toggle_state")