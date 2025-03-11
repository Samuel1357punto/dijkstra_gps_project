import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import random
from dijkstra import dijkstra, camino_mas_corto
from bellman_ford import bellman_ford, shortest_path


def obtener_mapa_ciudad_victoria():
    grafo = {}

    #Creación de nodos
    #"nodo": (ubicacionX, ubicacionY)
    nodos = {
        "Centro": (0, 0), "UAT": (2, 3), "Estadio": (5, 4), "Hospital": (-3, 2),
        "Aeropuerto": (8, -2), "Terminal": (4, -3), "Plaza": (1, -4),
        "Puente de Tamatán": (6, -3), "Monumento Niños Héroes": (3, 2.5), "Catedral": (-1, -2)
    }

    #Creación de aristas
    #"nodo1", "nodo2", ponderacion
    aristas = [
        ("Centro", "UAT", 3), ("Centro", "Estadio", 5), ("Centro", "Hospital", 4),
        ("Centro", "Terminal", 4.5), ("UAT", "Estadio", 2.5), ("Terminal", "Aeropuerto", 4.3),
        ("Terminal", "Plaza", 2), ("Plaza", "Puente de Tamatán", 5), ("Hospital", "Catedral", 3.5),
        ("UAT", "Monumento Niños Héroes", 3), ("Monumento Niños Héroes", "Catedral", 2),
        ("Estadio", "Aeropuerto", 6), ("Puente de Tamatán", "Aeropuerto", 3)
    ]

    for nodo in nodos:
        grafo[nodo] = []
    for nodo1, nodo2, peso in aristas:
        grafo[nodo1].append((nodo2, peso))
        grafo[nodo2].append((nodo1, peso))

    return grafo, nodos


class InterfazMapa:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Mapa de Ciudad Victoria - Intersecciones y Calles")
        self.G, self.pos = obtener_mapa_ciudad_victoria()
        self.crear_interfaz()

    def crear_interfaz(self):
        marco = tk.Frame(self.raiz)
        marco.pack()

        tk.Label(marco, text="Origen:").grid(row=0, column=0)
        self.entrada_origen = tk.Entry(marco)
        self.entrada_origen.grid(row=0, column=1)

        tk.Label(marco, text="Destino:").grid(row=1, column=0)
        self.entrada_destino = tk.Entry(marco)
        self.entrada_destino.grid(row=1, column=1)

        tk.Button(marco, text="Ejecutar Dijkstra", command=self.ejecutar_dijkstra).grid(row=2, column=0)
        tk.Button(marco, text="Comparar Algoritmos", command=self.comparar_algoritmos).grid(row=2, column=1)
        self.resultado_tiempo = tk.Label(marco, text="")
        self.resultado_tiempo.grid(row=3, columnspan=2)

        self.marco_canvas = tk.Frame(self.raiz)
        self.marco_canvas.pack()
        self.dibujar_mapa()

    def ejecutar_dijkstra(self):
        self.calcular_ruta(dijkstra, camino_mas_corto, "Dijkstra")

    def comparar_algoritmos(self):
        num_nodos = 500
        num_aristas = 1500
        grafo = {str(i): [] for i in range(num_nodos)}
        nodos = list(grafo.keys())

        for _ in range(num_aristas):
            nodo1, nodo2 = random.sample(nodos, 2)
            peso = random.randint(1, 100)
            grafo[nodo1].append((nodo2, peso))
            grafo[nodo2].append((nodo1, peso))

        nodo_inicio, nodo_fin = "0", str(num_nodos - 1)

        inicio = time.time()
        try:
            dijkstra(grafo, nodo_inicio)
            tiempo_dijkstra = (time.time() - inicio) * 1000
        except:
            tiempo_dijkstra = "Error"

        inicio = time.time()
        try:
            bellman_ford(grafo, nodo_inicio)
            tiempo_bellman_ford = (time.time() - inicio) * 1000
        except:
            tiempo_bellman_ford = "Error"

        messagebox.showinfo("Comparación de Algoritmos",
                            f"Dijkstra: {tiempo_dijkstra:.2f} ms\nBellman-Ford: {tiempo_bellman_ford:.2f} ms")

    def calcular_ruta(self, algoritmo, obtener_camino, nombre):
        origen, destino = self.entrada_origen.get().strip(), self.entrada_destino.get().strip()
        if origen not in self.G or destino not in self.G:
            messagebox.showerror("Error", "Nodos inválidos")
            return

        inicio = time.time()
        distancias, previos = algoritmo(self.G, origen)
        camino = obtener_camino(previos, origen, destino)
        tiempo_total = (time.time() - inicio) * 1000
        self.resultado_tiempo.config(text=f"{nombre} tomó {tiempo_total:.2f} ms")
        self.dibujar_mapa(camino)

    def dibujar_mapa(self, camino=None):
        plt.figure(figsize=(12, 8))
        plt.clf()
        G_nx = nx.Graph()
        for nodo, vecinos in self.G.items():
            G_nx.add_node(nodo, pos=self.pos[nodo])
            for vecino, peso in vecinos:
                G_nx.add_edge(nodo, vecino, weight=peso)

        nx.draw(G_nx, nx.get_node_attributes(G_nx, 'pos'), with_labels=True, node_color='lightblue')
        labels = nx.get_edge_attributes(G_nx, 'weight')
        nx.draw_networkx_edge_labels(G_nx, nx.get_node_attributes(G_nx, 'pos'), edge_labels=labels)

        if camino:
            nx.draw_networkx_nodes(G_nx, nx.get_node_attributes(G_nx, 'pos'), nodelist=camino, node_color='red')

        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.marco_canvas)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()


if __name__ == "__main__":
    raiz = tk.Tk()
    InterfazMapa(raiz)
    raiz.mainloop()


# Ahora el grafo se ve más grande con figsize ajustado a 12x8. 🚀