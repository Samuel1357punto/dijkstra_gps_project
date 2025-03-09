import heapq

def dijkstra(grafo, inicio):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    cola_prioridad = [(0, inicio)]
    nodos_previos = {nodo: None for nodo in grafo}

    while cola_prioridad:
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)

        if distancia_actual > distancias[nodo_actual]:
            continue

        for vecino, peso in grafo[nodo_actual]:
            nueva_distancia = distancia_actual + peso

            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                nodos_previos[vecino] = nodo_actual
                heapq.heappush(cola_prioridad, (nueva_distancia, vecino))

    return distancias, nodos_previos

def camino_mas_corto(nodos_previos, inicio, destino):
    camino = []
    actual = destino
    while actual is not None:
        camino.append(actual)
        actual = nodos_previos[actual]
    return camino[::-1] if camino[-1] == inicio else []

