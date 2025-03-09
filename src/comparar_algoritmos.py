import time
import random
from graph import Graph
from dijkstra import dijkstra
from bellman_ford import bellman_ford

def generate_large_graph(num_nodes, num_edges):
    graph = Graph()
    nodes = [str(i) for i in range(num_nodes)]

    for node in nodes:
        graph.add_node(node)

    for _ in range(num_edges):
        node1, node2 = random.sample(nodes, 2)
        weight = random.randint(1, 100)
        graph.add_edge(node1, node2, weight)

    return graph

def compare_algorithms(num_nodes=1500, num_edges=5500):
    graph = generate_large_graph(num_nodes, num_edges)

    start_node = "0"

    # Medir tiempo de Dijkstra
    start_time = time.time()
    dijkstra(graph.graph, start_node)
    dijkstra_time = time.time() - start_time

    # Medir tiempo de Bellman-Ford
    start_time = time.time()
    try:
        bellman_ford(graph.graph, start_node)
        bellman_ford_time = time.time() - start_time
    except ValueError:
        bellman_ford_time = "Ciclo negativo detectado"

    print(f"Dijkstra: {dijkstra_time:.5f} segundos")
    print(f"Bellman-Ford: {bellman_ford_time:.5f} segundos" if isinstance(bellman_ford_time, float) else bellman_ford_time)


if __name__ == "__main__":
    compare_algorithms()
