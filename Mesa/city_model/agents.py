import mesa
from collections import deque

class CarAgent(mesa.Agent):
    def __init__(self, model):
        super().__init__(model)
        self.steps = 0
        self.path = []
        self.path_pointer = 1
        self.active_route = False
        self.building = 0

    def get_neighbor_data(self, point):
        direction = None
        command = None
        
        for (start, end), dir_val in self.model.directions_dict.items():
            if (min(start[0], end[0]) <= point[0] <= max(start[0], end[0]) and
                min(start[1], end[1]) <= point[1] <= max(start[1], end[1])):
                direction = dir_val
                break
        
        for (start, end), cmd_val in self.model.commands_dict.items():
            if (min(start[0], end[0]) <= point[0] <= max(start[0], end[0]) and
                min(start[1], end[1]) <= point[1] <= max(start[1], end[1])):
                command = cmd_val
                break

        return direction, command

    def get_building_by_coodinate(self, coordinate):
        for key, value in self.model.parking_spot_dict.items():
            for element in value:
                if element == coordinate:
                    return key
        return None

    def get_neighbors(self, coordinate):
        base_patterns = {
            1: [(-1, 0)],
            2: [(-1, 0), (0, 1)],                  
            3: [(-1, 0), (-1, 1)],
            4: [(-1, 0), (0, 1), (-1, 1), (-1, -1)],
            5: [(-1, 0), (-1, -1)],
            6: [(-1, 0), (0, -1), (-1, 1), (-1, -1)]
        }

        def transform(direction, pattern):
            if direction == 'up':
                return [(dx, dy) for dx, dy in pattern]
            elif direction == 'down':
                return [(-dx, -dy) for dx, dy in pattern]
            elif direction == 'left':
                return [(-dy, dx) for dx, dy in pattern]
            elif direction == 'right':
                return [(dy, -dx) for dx, dy in pattern]
            
        direction, command = self.get_neighbor_data(coordinate)
            
        base_pattern = base_patterns[command]

        transformed_pattern = transform(direction, base_pattern)
    
        filtered_neighbors = [(coordinate[0] + dx, coordinate[1] + dy) for dx, dy in transformed_pattern]

        neighbors = [coord for coord in filtered_neighbors if coord not in self.model.structure_arr]
        
        return neighbors

    def bfs(self, start, target_nodes):
        queue = deque([start])
        visited = set([start])
        prev_node = {start: None}
        
        # Perform BFS
        while queue:
            current_node = queue.popleft()
            
            if current_node in target_nodes:
                path = []
                while current_node is not None:
                    path.append(current_node)
                    current_node = prev_node[current_node]
                return path[::-1]
            
            neighbors = self.get_neighbors(current_node)
            
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    prev_node[neighbor] = current_node
                    queue.append(neighbor)
        
        return []
    
    def move(self):
        if(self.active_route == False):
            self.building = self.get_building_by_coodinate(self.pos)

            if (self.building):
                possible_parking_spots = [coord for key, spots in self.model.parking_spot_dict.items() if key != self.building for coord in spots]
            else:
                possible_parking_spots = [coord for spots in self.model.parking_spot_dict.values() for coord in spots]

            self.path = self.bfs(self.pos, possible_parking_spots)

            self.active_route = True

            agents_neighborhood = self.model.grid.get_neighbors(
                self.pos, moore=True, include_center=False
            )

            neighbor_agents = [agent.pos for agent in agents_neighborhood]

            if (self.path[self.path_pointer] not in neighbor_agents):
                self.model.grid.move_agent(self, self.path[self.path_pointer])
                self.path_pointer += 1
                self.steps += 1
        else:
            if (self.path_pointer == len(self.path) - 1):
                if (not any(self.path[self.path_pointer] in spots for spots in self.model.parking_spot_dict.values())):
                    self.path_pointer = 1

                    if (self.building):
                        possible_parking_spots = [coord for key, spots in self.model.parking_spot_dict.items() if key != self.building for coord in spots]
                    else:
                        possible_parking_spots = [coord for spots in self.model.parking_spot_dict.values() for coord in spots]

                    self.path = self.bfs(self.pos, possible_parking_spots)

                    agents_neighborhood = self.model.grid.get_neighbors(
                        self.pos, moore=True, include_center=False
                    )

                    neighbor_agents = [agent.pos for agent in agents_neighborhood]

                    if (self.path[self.path_pointer] not in neighbor_agents):
                        self.model.grid.move_agent(self, self.path[self.path_pointer])
                        self.path_pointer += 1
                else:
                    filtered_neighborhood = self.get_neighbors(self.pos)

                    move = True

                    for coord in filtered_neighborhood:
                        if (self.model.grid.properties["semaphore"].data[coord] == 1):
                            move = False
                            break

                    agents_neighborhood = self.model.grid.get_neighbors(
                        self.pos, moore=True, include_center=False
                    )

                    neighbor_agents = [agent.pos for agent in agents_neighborhood]

                    if (self.path[self.path_pointer] in neighbor_agents):
                        move = False
                    
                    if(move):
                        self.model.grid.move_agent(self, self.path[self.path_pointer])
                        self.path_pointer += 1
                        self.model.grid.properties["parking_spot"].set_cell(self.pos, 0)
                        for key in list(self.model.parking_spot_dict.keys()):
                            if self.pos in self.model.parking_spot_dict[key]:
                                self.model.parking_spot_dict[key].remove(self.pos)
                                if not self.model.parking_spot_dict[key]:
                                    del self.model.parking_spot_dict[key]
            elif (self.path_pointer < len(self.path)):
                filtered_neighborhood = self.get_neighbors(self.pos)

                move = True

                for coord in filtered_neighborhood:
                    if (self.model.grid.properties["semaphore"].data[coord] == 1):
                        move = False
                        break

                agents_neighborhood = self.model.grid.get_neighbors(
                    self.pos, moore=True, include_center=False
                )

                neighbor_agents = [agent.pos for agent in agents_neighborhood]

                if (self.path[self.path_pointer] in neighbor_agents):
                    move = False
                
                if(move):
                    self.model.grid.move_agent(self, self.path[self.path_pointer])
                    self.path_pointer += 1
            
            if (self.path_pointer != len(self.path)):
                self.steps += 1

class SemaphoreAgent(mesa.Agent):
    def __init__(self, model, id, controlled_cells, state):
        super().__init__(model)
        # A state equal to False means green
        self.id = id
        self.state = state
        self.controlled_cells = controlled_cells
        for cell in self.controlled_cells:
            self.model.grid.properties["semaphore"].set_cell(cell, self.state)

    def toggle_state(self):
        if self.model.global_steps % 5 == 0:
            self.state = not self.state
            for cell in self.controlled_cells:
                self.model.grid.properties["semaphore"].set_cell(cell, self.state)