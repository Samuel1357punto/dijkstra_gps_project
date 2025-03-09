import heapq

class Graph:
    def __init__(self):
        self.graph = {
            "A": [("B", 4), ("C", 2)],
            "B": [("A", 4), ("C", 5), ("D", 10)],
            "C": [("A", 2), ("B", 5), ("D", 3), ("E", 7)],
            "D": [("B", 10), ("C", 3), ("E", 8)],
            "E": [("C", 7), ("D", 8)]
        }

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, node1, node2, weight):
        self.add_node(node1)
        self.add_node(node2)
        self.graph[node1].append((node2, weight))
        self.graph[node2].append((node1, weight))  # Para grafos no dirigidos

    def get_neighbors(self, node):
        return self.graph.get(node, [])

    def show_graph(self):
        """Muestra las conexiones del grafo con sus pesos."""
        for node, edges in self.graph.items():
            connections = ", ".join(f"{neighbor}({weight})" for neighbor, weight in edges)
            print(f"{node}: {connections}")

if __name__ == "__main__":
    g = Graph()
    g.show_graph()
