import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from graph import Graph
from dijkstra import dijkstra, shortest_path


class DijkstraGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Algoritmo de Dijkstra - GPS")

        self.graph = Graph()
        self.G = nx.Graph()
        self.load_predefined_graph()

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack()

        tk.Label(frame, text="Nodo 1:").grid(row=0, column=0)
        self.entry_node1 = tk.Entry(frame)
        self.entry_node1.grid(row=0, column=1)

        tk.Label(frame, text="Nodo 2:").grid(row=1, column=0)
        self.entry_node2 = tk.Entry(frame)
        self.entry_node2.grid(row=1, column=1)

        tk.Label(frame, text="Peso:").grid(row=2, column=0)
        self.entry_weight = tk.Entry(frame)
        self.entry_weight.grid(row=2, column=1)

        self.add_edge_button = tk.Button(frame, text="Agregar Arista", command=self.add_edge)
        self.add_edge_button.grid(row=3, columnspan=2)

        tk.Label(frame, text="Origen:").grid(row=4, column=0)
        self.entry_start = tk.Entry(frame)
        self.entry_start.grid(row=4, column=1)

        tk.Label(frame, text="Destino:").grid(row=5, column=0)
        self.entry_end = tk.Entry(frame)
        self.entry_end.grid(row=5, column=1)

        self.run_button = tk.Button(frame, text="Ejecutar Dijkstra", command=self.run_dijkstra)
        self.run_button.grid(row=6, columnspan=2)

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack()

        self.draw_graph()

    def add_edge(self):
        node1 = self.entry_node1.get()
        node2 = self.entry_node2.get()
        weight = self.entry_weight.get()

        if not (node1 and node2 and weight.isdigit()):
            messagebox.showerror("Error", "Ingrese valores válidos")
            return

        weight = int(weight)
        self.graph.add_edge(node1, node2, weight)
        self.G.add_edge(node1, node2, weight=weight)
        self.draw_graph()

    def load_predefined_graph(self):
        """Carga el grafo predefinido en NetworkX."""
        for node, edges in self.graph.graph.items():
            for neighbor, weight in edges:
                self.G.add_edge(node, neighbor, weight=weight)

    def run_dijkstra(self):
        start = self.entry_start.get()
        end = self.entry_end.get()

        if start not in self.graph.graph or end not in self.graph.graph:
            messagebox.showerror("Error", "Los nodos ingresados no existen en el grafo")
            return

        distances, previous_nodes = dijkstra(self.graph.graph, start)
        path = shortest_path(previous_nodes, start, end)

        if not path:
            messagebox.showerror("Error", "No existe un camino entre los nodos seleccionados")
            return

        self.draw_graph(path)

    def draw_graph(self, path=None):
        plt.clf()
        pos = nx.spring_layout(self.G)
        labels = nx.get_edge_attributes(self.G, "weight")

        nx.draw(self.G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels)  # Muestra los pesos de las aristas

        if path:
            path_edges = list(zip(path, path[1:]))
            nx.draw_networkx_nodes(self.G, pos, nodelist=path, node_color='red')
            nx.draw_networkx_edges(self.G, pos, edgelist=path_edges, edge_color='red', width=2)

        fig = plt.gcf()
        fig.set_size_inches(5, 5)

        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = DijkstraGUI(root)
    root.mainloop()