import mesa
import numpy as np
from .agents import SemaphoreAgent, CarAgent

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
            (2,11), (3,11), (4,11), (7,11), (8,11), (9,11), (10,11), (11,11), (16,11), (17,11), (20,11), (21,11),
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
            [[(17,0), (17,1)], False],
            [[(2,6), (2,7)], False],
            [[(7,6), (7,7)], False],
            [[(21,6), (21,7)], False],
            [[(16,18), (16,19)], False],
            [[(1,8), (0,8)], True],
            [[(6,8), (5,8)], True],
            [[(15,17), (14,17)], True],
            [[(19,2), (18,2)], True],
            [[(23,5), (22,5)], True]
        ]
        self.commands_dict = {
            #Up
            ((2,6), (2,6)): 1,
            ((3,6), (5,6)): 3,
            ((6,6), (6,6)): 6,
            ((7,6), (11,6)): 3,
            ((2,7), (7,7)): 5,
            ((8,7), (8,7)): 4,
            ((9,7), (11,7)): 5,
            ((2,14), (2,14)): 1,
            ((3,14), (11,14)): 3,
            ((2,15), (11,15)): 5,
            ((13,15), (13,15)): 1,
            ((14,15), (14,15)): 2,
            ((15,15), (15,15)): 4,
            ((16,14), (21,14)): 3,
            ((16,15), (16,15)): 1,
            ((17, 15), (21,15)): 5,
            ((16,18), (16,18)): 3,
            ((16,19), (16,19)): 1,
            ((17,18), (17,18)): 6,
            ((18,18), (18,18)): 3,
            ((19,18), (19,18)): 6,
            ((20,18), (21,18)): 3,
            ((17,19), (18,19)): 5,
            ((19,19), (19,19)): 4,
            ((20,19), (21,19)): 5,
            ((2,22), (2,22)): 1,
            ((3,22), (5,22)): 3,
            ((6,22), (7,22)): 6,
            ((8,22), (11,22)): 3,
            ((12,22), (13,22)): 6,
            ((14,22), (23,22)): 3,
            ((2,23), (22,23)): 5,
            ((23,23), (23,23)): 1,

            ((2,3), (2,3)): 1,
            ((2,17), (2,17)): 1,
            ((8,20), (8,20)): 1,
            ((16,10), (16,10)): 1,
            ((20,4), (20,4)): 1,
            #Left
            ((0,2), (0,22)): 5,
            ((0,23), (0,23)): 1,
            ((1,2), (1,2)): 1,
            ((1,3), (1,3)): 6,
            ((1,4), (1,11)): 3,
            ((1,12), (1,13)): 6,
            ((1,14), (1,16)): 3,
            ((1,17), (1,17)): 6,
            ((1,18), (1,23)): 3,
            ((5,8), (5,8)): 1,
            ((5,9), (5,9)): 5,
            ((5,10), (5,10)): 4,
            ((5,11), (5,11)): 5,
            ((6,8), (6,11)): 3,
            ((6,16), (6,16)): 1,
            ((6,17), (6,19)): 5,
            ((6,20), (6,20)): 4,
            ((6,21), (6,21)): 5,
            ((7,16), (7,19)): 3,
            ((7,20), (7,20)): 6,
            ((7,21), (7,21)): 3,
            ((12,2), (12,3)): 5,
            ((12,4), (12,4)): 4,
            ((12,5), (12,5)): 5,
            ((12,6), (12,7)): 4,
            ((12,8), (12,9)): 5,
            ((12,10), (12,10)): 4,
            ((12,11), (12,11)): 5,
            ((13,2), (13,2)): 1,
            ((13,3), (13,11)): 3,
            ((12,13), (12,13)): 1,
            ((12,14), (12,14)): 2,
            ((12,15), (12,15)): 4,
            ((12,16), (12,16)): 1,
            ((12,17), (12,21)): 5,
            ((13,16), (13,21)): 3,
            ((18,2), (18, 2)): 5,
            ((18,3), (18,3)): 4,
            ((18,4), (18,5)): 5,
            ((19,2), (19,2)): 1,
            ((19,3), (19,3)): 3,
            ((19,4), (19,4)): 6,
            ((19,5), (19,5)): 3,
            ((9,2), (9,2)): 1,
            ((8,8), (8,8)): 1,
            ((19,20), (19,20)): 1,
            #Down
            ((0,0), (0,0)): 1,
            ((1,0), (21,0)): 5,
            ((0,1), (8,1)): 3,
            ((9,1), (9,1)): 6,
            ((10,1), (13,1)): 3,
            ((14,1), (15,1)): 6,
            ((16,1), (20,1)): 3,
            ((21,1), (21,1)): 1,
            ((16,6), (17,6)): 5,
            ((18,6), (19,6)): 4,
            ((20,6), (21,6)): 5,
            ((16,7), (17,7)): 3,
            ((18,7), (19,7)): 6,
            ((20,7), (20,7)): 3,
            ((21,7), (21,7)): 1,
            ((2,12), (4,12)): 5,
            ((5,12), (6,12)): 4,
            ((7,12), (10,12)): 5,
            ((11,12), (11,12)): 1,
            ((12,12), (12,12)): 4,
            ((13,12), (13,12)): 2,
            ((14,12), (14,12)): 1,
            ((2,13), (11,13)): 3,
            ((16,12), (21,12)): 5,
            ((16,13), (20,13)): 3,
            ((21,13), (21,13)): 1,
            ((11,4), (11,4)): 1,
            ((11,10), (11,10)): 1,
            ((4,10), (4,10)): 1,
            ((5,20), (5,20)): 1,
            ((17,3), (17,3)): 1,
            ((21,9), (21,9)): 1,
            #Right
            ((14,2), (14,11)): 3,
            ((15,2), (15,5)): 5,
            ((15,6), (15,7)): 4,
            ((15,8), (15,9)): 5,
            ((15,10), (15,10)): 4,
            ((15,11), (15,11)): 1,
            ((15,12), (15,12)): 4,
            ((15,13), (15,13)): 2,
            ((15,14), (15,14)): 1,
            ((14,16), (14,20)): 3,
            ((14,21), (14,21)): 1,
            ((15,16), (15,21)): 5,
            ((18,8), (18,11)): 3,
            ((19,8), (19,10)): 5,
            ((19,11), (19,11)): 1,
            ((22,0), (22,8)): 3,
            ((22,9), (22,9)): 6,
            ((22,10), (22,13)): 3,
            ((22,14), (22,15)): 6,
            ((22,16), (22,17)): 3,
            ((22,18), (22,19)): 6,
            ((22,20), (22,20)): 3,
            ((22,21), (22,21)): 1,
            ((23,0), (23,0)): 1,
            ((23,1), (23,21)): 5,
            ((6,5), (6,5)): 1,
            ((17,17), (17,17)): 1,
            ((19,17), (19,17)): 1
        }
        self.directions_dict = {
            #Up
            ((2,22), (23,23)): "up",
            ((16,18), (21,19)): "up",
            ((16,14), (21,15)): "up",
            ((13,15), (15,15)): "up",
            ((2,14), (11,15)): "up",
            ((2,6), (11,7)): "up",
            ((2,3), (2,3)): "up",
            ((2,17), (2,17)): "up",
            ((8,20), (8,20)): "up",
            ((16,10), (16,10)): "up",
            ((20,4), (20,4)): "up",
            #Left
            ((0,2), (1,23)): "left",
            ((5,8), (6,11)): "left",
            ((6,16), (7,21)): "left",
            ((12,2), (13,11)): "left",
            ((12,13), (12,15)): "left",
            ((12,16), (13,21)): "left",
            ((18,2), (19,5)): "left",
            ((9,2), (9,2)): "left",
            ((8,8), (8,8)): "left",
            ((19,20), (19,20)): "left",
            #Down
            ((0,0), (21,1)): "down",
            ((2,12), (11,13)): "down",
            ((12,12), (14,12)): "down",
            ((16,12), (21,13)): "down",
            ((16,6), (21,7)): "down",
            ((11,4), (11,4)): "down",
            ((11,10), (11,10)): "down",
            ((4,10), (4,10)): "down",
            ((5,20), (5,20)): "down",
            ((17,3), (17,3)): "down",
            ((21,9), (21,9)): "down",
            #Right
            ((22,0), (23,21)): "right",
            ((14,2), (15,11)): "right",
            ((15,12), (15,14)): "right",
            ((14,16), (15,21)): "right",
            ((18,8), (19,11)): "right",
            ((6,5), (6,5)): "right",
            ((17,17), (17,17)): "right",
            ((19,17), (19,17)): "right"
        }
        self.global_steps = 0
        self.structure_layer = mesa.space.PropertyLayer("structure", self.width, self.height, np.float64(0))
        self.parking_spot_layer = mesa.space.PropertyLayer("parking_spot", self.width, self.height, np.float64(0))
        self.semaphore_layer = mesa.space.PropertyLayer("semaphore", self.width, self.height, np.float64(0))
        self.grid = mesa.space.MultiGrid(self.width, self.height, False, (self.structure_layer, self.parking_spot_layer, self.semaphore_layer))
        self.running = True
        self.datacollector = mesa.DataCollector()

        # Create building grid
        for x, y in self.structure_arr:
            self.grid.properties["structure"].set_cell((x, y), 1)

        # Create parking spot grid
        for coordinates in self.parking_spot_dict.values():
            for (x, y) in coordinates:
                self.grid.properties["parking_spot"].set_cell((x, y), 1)

        # Create semaphore agents
        for values in self.semaphore_arr:
            SemaphoreAgent(self, values[0], values[1])

        all_parking_spots = [coord for spots in self.parking_spot_dict.values() for coord in spots]
        for _ in range(car_count):
            random_num = self.random.randrange(len(all_parking_spots))
            a = CarAgent(self)
            self.grid.place_agent(a, all_parking_spots[random_num])
            all_parking_spots.pop(random_num)

        #self.grid.place_agent(CarAgent(self), (6,5))
        
    def step(self):
        self.datacollector.collect(self)

        self.global_steps += 1

        self.agents_by_type[SemaphoreAgent].shuffle_do("toggle_state")
        self.agents_by_type[CarAgent].shuffle_do("move")