import networkx as nx
import matplotlib.pyplot as plt


class DisjointSet:
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}
        self.rank = {node: 0 for node in nodes}

    def find(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, node1, node2):
        root1 = self.find(node1)
        root2 = self.find(node2)

        if root1 != root2:
            if self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            elif self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1


def kruskal(graph):
    minimum_spanning_tree = nx.Graph()
    sorted_edges = sorted(graph.edges(data=True), key=lambda x: x[2]["weight"])
    nodes = list(graph.nodes)
    disjoint_set = DisjointSet(nodes)
    total_weight = 0  # Variable para almacenar la suma de las aristas utilizadas

    for u, v, data in sorted_edges:
        if disjoint_set.find(u) != disjoint_set.find(v):
            minimum_spanning_tree.add_edge(u, v, weight=data["weight"])
            disjoint_set.union(u, v)
            total_weight += data["weight"]  # Agregar el peso de la arista utilizada

    return minimum_spanning_tree, total_weight


# Crear grafo de ejemplo
G = nx.Graph()
G.add_edge("A", "B", weight=4)
G.add_edge("A", "F", weight=2)
G.add_edge("B", "C", weight=3)
G.add_edge("B", "G", weight=5)
G.add_edge("C", "D", weight=8)
G.add_edge("C", "H", weight=10)
G.add_edge("D", "E", weight=2)
G.add_edge("D", "I", weight=6)
G.add_edge("E", "J", weight=3)

G.add_edge("F", "G", weight=7)
G.add_edge("F", "K", weight=10)
G.add_edge("G", "H", weight=12)
G.add_edge("G", "L", weight=4)
G.add_edge("H", "I", weight=3)
G.add_edge("H", "M", weight=2)
G.add_edge("I", "J", weight=4)
G.add_edge("I", "N", weight=9)
G.add_edge("J", "O", weight=2)

G.add_edge("K", "L", weight=7)
G.add_edge("K", "P", weight=6)
G.add_edge("L", "M", weight=8)
G.add_edge("L", "Q", weight=1)
G.add_edge("M", "N", weight=9)
G.add_edge("M", "R", weight=9)
G.add_edge("N", "O", weight=10)
G.add_edge("N", "S", weight=7)
G.add_edge("O", "T", weight=10)

G.add_edge("P", "Q", weight=2)
G.add_edge("Q", "R", weight=3)
G.add_edge("R", "S", weight=4)
G.add_edge("S", "T", weight=5)


if len(G.nodes) == 0:
    print("El grafo no tiene nodos.")
    exit()

# Ejecutar el algoritmo de Prim
minimum_spanning_tree_prim = nx.minimum_spanning_tree(G)

# Ejecutar el algoritmo de Kruskal
minimum_spanning_tree_kruskal, total_weight_kruskal = kruskal(G)

# Calcular la suma de las aristas utilizadas en el algoritmo de Prim
total_weight_prim = sum(
    data["weight"] for _, _, data in minimum_spanning_tree_prim.edges(data=True)
)

# Imprimir la suma de las aristas utilizadas en cada algoritmo
print("Suma de las aristas utilizadas en el algoritmo de Prim:", total_weight_prim)
print(
    "Suma de las aristas utilizadas en el algoritmo de Kruskal:", total_weight_kruskal
)

# Crear ventana y mostrar los cuadros
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

# Dibujar el grafo original en el primer cuadro
axes[0].set_title("Grafo original")
pos = nx.spring_layout(G)
nx.draw_networkx(G, pos=pos, with_labels=True, ax=axes[0])
edge_labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels, ax=axes[0])
nx.draw_networkx_edges(G, pos=pos, ax=axes[0])

# Dibujar el árbol de Prim en el segundo cuadro
axes[1].set_title("Árbol de Prim")
pos = nx.spring_layout(minimum_spanning_tree_prim)
nx.draw_networkx(minimum_spanning_tree_prim, pos=pos, with_labels=True, ax=axes[1])
edge_labels = nx.get_edge_attributes(minimum_spanning_tree_prim, "weight")
nx.draw_networkx_edge_labels(
    minimum_spanning_tree_prim, pos=pos, edge_labels=edge_labels, ax=axes[1]
)
nx.draw_networkx_edges(minimum_spanning_tree_prim, pos=pos, ax=axes[1])

# Resaltar el vértice padre en el árbol de Prim
root_prim = max(minimum_spanning_tree_prim.degree, key=lambda x: x[1])[0]
node_colors_prim = [
    "r" if node == root_prim else "b" for node in minimum_spanning_tree_prim.nodes
]
node_sizes_prim = [
    200 if node == root_prim else 100 for node in minimum_spanning_tree_prim.nodes
]
nx.draw_networkx_nodes(
    minimum_spanning_tree_prim,
    pos=pos,
    node_color=node_colors_prim,
    node_size=node_sizes_prim,
    ax=axes[1],
)

# Dibujar el árbol de Kruskal en el tercer cuadro
axes[2].set_title("Árbol de Kruskal")
pos = nx.spring_layout(minimum_spanning_tree_kruskal)
nx.draw_networkx(minimum_spanning_tree_kruskal, pos=pos, with_labels=True, ax=axes[2])
edge_labels = nx.get_edge_attributes(minimum_spanning_tree_kruskal, "weight")
nx.draw_networkx_edge_labels(
    minimum_spanning_tree_kruskal, pos=pos, edge_labels=edge_labels, ax=axes[2]
)
nx.draw_networkx_edges(minimum_spanning_tree_kruskal, pos=pos, ax=axes[2])

# Resaltar el vértice padre en el árbol de Kruskal
root_kruskal = max(minimum_spanning_tree_kruskal.degree, key=lambda x: x[1])[0]
node_colors_kruskal = [
    "r" if node == root_kruskal else "b" for node in minimum_spanning_tree_kruskal.nodes
]
node_sizes_kruskal = [
    200 if node == root_kruskal else 100 for node in minimum_spanning_tree_kruskal.nodes
]
nx.draw_networkx_nodes(
    minimum_spanning_tree_kruskal,
    pos=pos,
    node_color=node_colors_kruskal,
    node_size=node_sizes_kruskal,
    ax=axes[2],
)

# Mostrar la ventana con los cuadros
plt.tight_layout()
plt.show()
