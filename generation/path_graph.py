import networkx as nx
import matplotlib.pyplot as plt
import os
import random

def select_numbers(n):
    # Select a and b such that 0 ≤ a < b ≤ n-1
    a, b = sorted(random.sample(range(n), 2))

    # Select the third number from range [b+1, n-1], if possible
    if b + 1 <= n:
        c = random.choice(range(b + 1, n+1))
    else:
        raise ValueError("No valid c can be chosen. Increase n.")

    return a, b, c

def save_graph(graph, name, output_dir="generation\\path_graphs\\hard"):
    """Save graph in multiple formats."""
    os.makedirs(output_dir, exist_ok=True)

    num_nodes = len(graph.nodes())
    num_edges = len(graph.edges())

    # Save adjacency list
    # nx.write_adjlist(graph, os.path.join(output_dir, f"{name}.adjlist"), comments="")

    # # Save edge list
    edgelist_path = os.path.join(output_dir, f"{name}.txt")
    # nx.write_edgelist(graph, edgelist_path, data= False)
    with open(edgelist_path, "w") as f:
        f.write(f"{num_nodes} {num_edges}\n")
        for u, v in graph.edges():
            f.write(f"{u} {v}\n")  # Writing edge as "node1 node2"
        for i in range(5):
            a, b, c = sorted(random.sample(range(num_nodes), 3))
            f.write(f"{a} {b} {c}\n")
        
        for i in range(5):
            a, b, c = sorted(random.sample(range(num_nodes), 3))
            f.write(f"{a} {c} {b}\n")


    # Save visualization
    # plt.figure(figsize=(6, 6))
    # nx.draw(graph, with_labels=True, node_color="lightblue", edge_color="gray")
    # plt.title(f"Path Graph with {len(graph.nodes())} nodes")
    # plt.savefig(os.path.join(output_dir, f"{name}.png"))
    # plt.close()

def generate_path_graphs(node_counts):
    """Generate path graphs for given node counts and save them."""
    ind = 0
    for n in node_counts:
        G = nx.path_graph(n)  # Create a path graph with n nodes
        save_graph(G, f"path_graph_{ind}")
        ind += 1

if __name__ == "__main__":
    node_counts = []
    for i in range(50):
        node_counts.append(random.choice(range(28,40)))   # easy- range(4,14)   med- (14,28)   hard- (28,40)
    generate_path_graphs(node_counts)
    print(node_counts)
    # node_counts = [5, 10, 20, 50, 100, 200]  # Define different node sizes







































# import networkx as nx
# import matplotlib.pyplot as plt
# import random
# import os

# def save_graph(graph, name, output_dir="graphs"):
#     """Save graph in multiple formats."""
#     os.makedirs(output_dir, exist_ok=True)
    
#     # Save adjacency list
#     nx.write_adjlist(graph, os.path.join(output_dir, f"{name}.adjlist"))
    
#     # Save edge list
#     nx.write_edgelist(graph, os.path.join(output_dir, f"{name}.edgelist"))
    
#     # Save visualization
#     plt.figure(figsize=(6, 6))
#     nx.draw(graph, with_labels=True, node_color="lightblue", edge_color="gray")
#     plt.savefig(os.path.join(output_dir, f"{name}.png"))
#     plt.close()

# def generate_graphs():
#     """Generate diverse graphs and save them."""
    
#     num_nodes = [5, 10, 20, 50]  # Different node counts
#     edge_probs = [0.2, 0.5, 0.8]  # Sparse to dense graphs
    
#     for n in num_nodes:
#         # Path Graph
#         G_path = nx.path_graph(n)
#         save_graph(G_path, f"path_graph_{n}")

#         # Complete Graph
#         G_complete = nx.complete_graph(n)
#         save_graph(G_complete, f"complete_graph_{n}")

#         for p in edge_probs:
#             # Erdős–Rényi Random Graph
#             G_er = nx.erdos_renyi_graph(n, p)
#             save_graph(G_er, f"erdos_renyi_{n}_p{int(p*10)}")

#         # Barabási-Albert Graph (Scale-free)
#         if n > 2:
#             G_ba = nx.barabasi_albert_graph(n, max(1, n//10))
#             save_graph(G_ba, f"barabasi_albert_{n}")

#         # Custom Graph with a blocked node
#         G_custom = nx.erdos_renyi_graph(n, 0.4)
#         if n > 4:
#             blocked_node = random.choice(list(G_custom.nodes))
#             G_custom.remove_node(blocked_node)
#             save_graph(G_custom, f"custom_graph_no_{blocked_node}")

# if __name__ == "__main__":
#     generate_graphs()
