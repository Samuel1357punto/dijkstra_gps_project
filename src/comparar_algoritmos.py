import time
import random
from grafo import Grafo
from dijkstra import dijkstra
from bellman_ford import bellman_ford

def generar_grafo_grande(num_nodos, num_aristas):
    grafo = Grafo()
    nodos = [str(i) for i in range(num_nodos)]

    for nodo in nodos:
        grafo.agregar_nodo(nodo)

    for _ in range(num_aristas):
        nodo1, nodo2 = random.sample(nodos, 2)
        peso = random.randint(1, 100)
        grafo.agregar_arista(nodo1, nodo2, peso)

    return grafo

def comparar_algoritmos(num_nodos=1500, num_aristas=5500):
    grafo = generar_grafo_grande(num_nodos, num_aristas)

    nodo_inicio = "0"

    # Medir tiempo de Dijkstra
    tiempo_inicio = time.time()
    dijkstra(grafo.grafo, nodo_inicio)
    tiempo_dijkstra = time.time() - tiempo_inicio

    # Medir tiempo de Bellman-Ford
    tiempo_inicio = time.time()
    try:
        bellman_ford(grafo.grafo, nodo_inicio)
        tiempo_bellman_ford = time.time() - tiempo_inicio
    except ValueError:
        tiempo_bellman_ford = "Ciclo negativo detectado"

    print(f"Dijkstra: {tiempo_dijkstra:.5f} segundos")
    print(f"Bellman-Ford: {tiempo_bellman_ford:.5f} segundos" if isinstance(tiempo_bellman_ford, float) else tiempo_bellman_ford)

if __name__ == "__main__":
    comparar_algoritmos()
