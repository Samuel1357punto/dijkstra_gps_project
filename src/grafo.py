import heapq

class Grafo:
    def __init__(self):
        self.grafo = {
            """A": [("B", 4), ("C", 2)],
            "B": [("A", 4), ("C", 5), ("D", 10)],
            "C": [("A", 2), ("B", 5), ("D", 3), ("E", 7)],
            "D": [("B", 10), ("C", 3), ("E", 8)],
            "E": [("C", 7), ("D", 8)]"""
        }

    def agregar_nodo(self, nodo):
        if nodo not in self.grafo:
            self.grafo[nodo] = []

    def agregar_arista(self, nodo1, nodo2, peso):
        self.agregar_nodo(nodo1)
        self.agregar_nodo(nodo2)
        self.grafo[nodo1].append((nodo2, peso))
        self.grafo[nodo2].append((nodo1, peso))

    def obtener_vecinos(self, nodo):
        return self.grafo.get(nodo, [])

    def mostrar_grafo(self):
        for nodo, aristas in self.grafo.items():
            conexiones = ", ".join(f"{vecino}({peso})" for vecino, peso in aristas)
            print(f"{nodo}: {conexiones}")

if __name__ == "__main__":
    g = Grafo()
    g.mostrar_grafo()


