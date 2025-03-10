import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
from grafo import Grafo
from dijkstra import dijkstra, camino_mas_corto
from bellman_ford import bellman_ford
import random

class InterfazDijkstra:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Comparación de Algoritmos de Rutas")

        self.grafo = Grafo()
        self.G = nx.Graph()
        self.cargar_grafo_predefinido()

        self.crear_interfaz()

    def crear_interfaz(self):
        marco = tk.Frame(self.raiz)
        marco.pack()

        tk.Label(marco, text="Nodo 1:").grid(row=0, column=0)
        self.entrada_nodo1 = tk.Entry(marco)
        self.entrada_nodo1.grid(row=0, column=1)

        tk.Label(marco, text="Nodo 2:").grid(row=1, column=0)
        self.entrada_nodo2 = tk.Entry(marco)
        self.entrada_nodo2.grid(row=1, column=1)

        tk.Label(marco, text="Peso:").grid(row=2, column=0)
        self.entrada_peso = tk.Entry(marco)
        self.entrada_peso.grid(row=2, column=1)

        self.boton_agregar_arista = tk.Button(marco, text="Agregar Arista", command=self.agregar_arista)
        self.boton_agregar_arista.grid(row=3, columnspan=2)

        tk.Label(marco, text="Origen:").grid(row=4, column=0)
        self.entrada_origen = tk.Entry(marco)
        self.entrada_origen.grid(row=4, column=1)

        tk.Label(marco, text="Destino:").grid(row=5, column=0)
        self.entrada_destino = tk.Entry(marco)
        self.entrada_destino.grid(row=5, column=1)

        self.boton_ejecutar = tk.Button(marco, text="Ejecutar Dijkstra", command=self.ejecutar_dijkstra)
        self.boton_ejecutar.grid(row=6, columnspan=2)

        self.boton_comparar = tk.Button(marco, text="Comparar Algoritmos", command=self.comparar_algoritmos)
        self.boton_comparar.grid(row=7, columnspan=2)

        self.marco_canvas = tk.Frame(self.raiz)
        self.marco_canvas.pack()

        self.dibujar_grafo()

    def agregar_arista(self):
        nodo1 = self.entrada_nodo1.get()
        nodo2 = self.entrada_nodo2.get()
        peso = self.entrada_peso.get()

        if not (nodo1 and nodo2 and peso.isdigit()):
            messagebox.showerror("Error", "Ingrese valores válidos")
            return

        peso = int(peso)
        self.grafo.agregar_arista(nodo1, nodo2, peso)
        self.G.add_edge(nodo1, nodo2, weight=peso)
        self.dibujar_grafo()

    def cargar_grafo_predefinido(self):
        for nodo, aristas in self.grafo.grafo.items():
            for vecino, peso in aristas:
                self.G.add_edge(nodo, vecino, weight=peso)

    def ejecutar_dijkstra(self):
        origen = self.entrada_origen.get()
        destino = self.entrada_destino.get()

        if origen not in self.grafo.grafo or destino not in self.grafo.grafo:
            messagebox.showerror("Error", "Los nodos ingresados no existen en el grafo")
            return

        distancias, nodos_previos = dijkstra(self.grafo.grafo, origen)
        camino = camino_mas_corto(nodos_previos, origen, destino)

        if not camino:
            messagebox.showerror("Error", "No existe un camino entre los nodos seleccionados")
            return

        self.dibujar_grafo(camino)

    def dibujar_grafo(self, camino=None):
        plt.clf()
        pos = nx.spring_layout(self.G)
        etiquetas = nx.get_edge_attributes(self.G, "weight")

        nx.draw(self.G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=etiquetas)

        if camino:
            aristas_camino = list(zip(camino, camino[1:]))
            nx.draw_networkx_nodes(self.G, pos, nodelist=camino, node_color='red')
            nx.draw_networkx_edges(self.G, pos, edgelist=aristas_camino, edge_color='red', width=2)

        fig = plt.gcf()
        fig.set_size_inches(5, 5)

        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(fig, master=self.marco_canvas)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def comparar_algoritmos(self):
        num_nodos = 1000
        num_aristas = 3000
        grafo = Grafo()
        nodos = [str(i) for i in range(num_nodos)]

        for nodo in nodos:
            grafo.agregar_nodo(nodo)

        for _ in range(num_aristas):
            nodo1, nodo2 = random.sample(nodos, 2)
            peso = random.randint(1, 100)
            grafo.agregar_arista(nodo1, nodo2, peso)

        nodo_inicio = "0"

        tiempo_inicio = time.time()
        dijkstra(grafo.grafo, nodo_inicio)
        tiempo_dijkstra = time.time() - tiempo_inicio

        tiempo_inicio = time.time()
        try:
            bellman_ford(grafo.grafo, nodo_inicio)
            tiempo_bellman_ford = time.time() - tiempo_inicio
        except ValueError:
            tiempo_bellman_ford = "Ciclo negativo detectado"

        messagebox.showinfo("Comparación de Algoritmos", f"Dijkstra: {tiempo_dijkstra:.5f} segundos\nBellman-Ford: {tiempo_bellman_ford:.5f} segundos")

if __name__ == "__main__":
    raiz = tk.Tk()
    app = InterfazDijkstra(raiz)
    raiz.mainloop()
