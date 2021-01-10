class Graph:
    def __init__(self):
        self.connected = {}
        self.devices = {}
        self.strength = {}

    @staticmethod
    def bfs(connected, start, end):
        explored = []
        queue = [[start]]

        if start == end:
            return [start, end]

        while queue:
            path = queue.pop(0)
            node = path[-1]

            if node not in explored:
                neighbours = connected[node]
                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)

                    if neighbour == end:
                        return new_path
                explored.append(node)

    def add_node(self, node, type):
        if type != "COMPUTER" and type != "REPEATER":
            return 400, f"type '{type}' is not supported"

        if node in (self.connected or self.devices or self.strength):
            return 400, f"Device '{node}' already exists"

        self.connected[node] = []
        self.devices[node] = type
        if type == 'COMPUTER':
            self.strength[node] = 5

        return 200, f"Successfully added {node}"

    def change_strength(self, element, value):
        if element not in self.devices:
            return 404, 'Device Not Found'

        if self.devices[element] == 'REPEATER':
            return 400, "Repeater strength can't be defined"

        if not isinstance(value, int):
            return 400, "value should be an integer"

        self.strength[element] = value

        return 200, "Successfully defined strength"

    def add_connection(self, source, targets):
        if source not in self.devices:
            return 400, f"Node '{source}' not found"

        if source in targets:
            return 400, "Cannot connect device to itself"

        set_targets = set(targets)
        set_connected = set(self.connected[source])

        if set_targets & set_connected:
            return 400, "Devices are already connected"

        self.connected[source] += targets
        for i in targets:
            self.connected[i].append(source)
        return 200, "Successfully connected"

    def find_path(self, start, end):
        if start not in self.devices:
            return 400, f"Node '{start}' not found"

        if end not in self.devices:
            return 400, f"Node '{end}' not found"

        if self.devices[start] == 'REPEATER' or self.devices[end] == 'REPEATER':
            return 400, "Route cannot be calculated with repeater"

        route = Graph.bfs(self.connected, start, end)

        if route:
            result = "Route is " + "->".join(route)
            return 200, result
        return 404, "Route not found"

    def fetch_devices(self):
        return [{"type": v, "name": k} for k, v in self.devices.items()]

    def __str__(self):
        return f"{self.devices}\n{self.connected}\n{self.strength}"


#
# graph = Graph()
# graph.add_node("A1", "COMPUTER")
# graph.add_node("A2", "COMPUTER")
# graph.add_node("A3", "COMPUTER")
# graph.add_node("A3", "PHONE")
# graph.add_node("A1", "COMPUTER")
# graph.add_node("A4", "COMPUTER")
# graph.add_node("A5", "COMPUTER")
# graph.add_node("A6", "COMPUTER")
# graph.add_node("R1", "REPEATER")
# graph.change_strength("A1", "Helloworld")
# graph.change_strength("A10", "Helloworld")
# graph.change_strength("A1", 2)
# graph.add_connection("A1", ["A2", "A3"])
# graph.add_connection("A1", ["A1"])
# graph.add_connection("A1", ["A2"])
# graph.add_connection("A5", ["A4"])
# graph.add_connection("R1", ["A2"])
# graph.add_connection("R1", ["A5"])
# graph.add_connection("A8", ["A1"])
# graph.add_connection("A2", ["A4"])
# print(graph.fetch_devices())
# graph.find_path("A1", "A4")
# graph.find_path("A1", "A5")
# graph.find_path("A4", "A3")
# graph.find_path("A1", "A1")
# graph.find_path("A1", "A6")
# graph.find_path("A2", "R1")
# graph.find_path("A1", "A10")
# #
# "\n" * 5)
# graph)
