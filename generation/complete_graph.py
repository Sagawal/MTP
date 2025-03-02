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

def save_graph(graph, name, output_dir="generation\\complete_graphs\\hard"):
    """Save graph in multiple formats."""
    os.makedirs(output_dir, exist_ok=True)

    num_nodes = len(graph.nodes())
    num_edges = len(graph.edges())

    # Save adjacency list
    # nx.write_adjlist(graph, os.path.join(output_dir, f"{name}.adjlist"))

    # Save edge list
    # nx.write_edgelist(graph, os.path.join(output_dir, f"{name}.edgelist"), data=False)

    # # Save edge list
    edgelist_path = os.path.join(output_dir, f"{name}.txt")
    # nx.write_edgelist(graph, edgelist_path, data= False)
    with open(edgelist_path, "w") as f:
        f.write(f"{num_nodes} {num_edges}\n")
        for u, v in graph.edges():
            f.write(f"{u} {v}\n")  # Writing edge as "node1 node2"
        for i in range(10):
            a, b, c = sorted(random.sample(range(num_nodes), 3))
            f.write(f"{a} {b} {c}\n")


    # Save visualization
    # plt.figure(figsize=(6, 6))
    # nx.draw(graph, with_labels=True, node_color="lightblue", edge_color="gray")
    # plt.title(f"Complete Graph with {len(graph.nodes())} nodes")
    # plt.savefig(os.path.join(output_dir, f"{name}.png"))
    # plt.close()

def generate_complete_graphs(node_counts):
    """Generate complete graphs for given node counts and save them."""
    ind = 0
    for n in node_counts:
        G = nx.complete_graph(n)  # Create a complete graph with n nodes
        save_graph(G, f"complete_graph_{ind}")
        ind += 1

if __name__ == "__main__":
    node_counts = []
    for i in range(30):
        node_counts.append(random.choice(range(16,22)))   # easy- range(4-10)   med- (10-16)   hard- (16-22)
    generate_complete_graphs(node_counts)
    print(node_counts)
    # node_counts = [5, 10, 20, 50, 100]  # Define different node sizes

