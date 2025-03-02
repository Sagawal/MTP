import networkx as nx
import matplotlib.pyplot as plt
import os
import random

def can_reach_without_x(graph, node_a, node_b, node_c):
    """Check if node_a can reach node_b without passing through node_c."""
    if node_c in graph:
        G_modified = graph.copy()
        G_modified.remove_node(node_c)  # Remove node_c to block paths through it
        return nx.has_path(G_modified, node_a, node_b)
    return nx.has_path(graph, node_a, node_b)

def save_graph(graph, name, output_dir="generation\\random_graphs\\hard"):
    """Save graph in multiple formats."""
    os.makedirs(output_dir, exist_ok=True)

    num_nodes = len(graph.nodes())
    num_edges = len(graph.edges())

    # Save adjacency list
    # nx.write_adjlist(graph, os.path.join(output_dir, f"{name}.adjlist"))

    # Save edge list
    edgelist_path = os.path.join(output_dir, f"{name}.txt")
    # nx.write_edgelist(graph, edgelist_path, data=False)
    with open(edgelist_path, "w") as f:
        f.write(f"{num_nodes} {num_edges}\n")
        for u, v in graph.edges():
            f.write(f"{u} {v}\n")  # Writing edge as "node1 node2"
        for i in range(10):
            a, b, c = random.sample(range(num_nodes), 3)
            check_nodes = (a,b,c)
            result1 = can_reach_without_x(graph, *check_nodes)
            result = 1
            if result1 == False:
                result = 0
            f.write(f"{a} {b} {c} {result}\n")

        

    # # Save visualization
    # plt.figure(figsize=(6, 6))
    # nx.draw(graph, with_labels=True, node_color="lightblue", edge_color="gray")
    # plt.title(f"Random Graph with {len(graph.nodes())} nodes")
    # plt.savefig(os.path.join(output_dir, f"{name}.png"))
    # plt.close()

def generate_random_graphs(node_counts, edge_probs=[0.2]):
    """Generate random graphs and check if A can reach B without C."""

    ind = 0
    for n in node_counts:
        for p in edge_probs:
            # Erdős–Rényi Graph G(n, p)
            G_er = nx.erdos_renyi_graph(n, p)
            
            save_graph(G_er, f"random_graph_{ind}")
            ind += 1

        # if n > 2:
        #     # Barabási-Albert Graph (Scale-Free)
        #     G_ba = nx.barabasi_albert_graph(n, max(1, n//10))
        #     save_graph(G_ba, f"barabasi_albert_{n}")
        #     result = can_reach_without_x(G_ba, *check_nodes)
        #     results.append((f"barabasi_albert_{n}", result))


if __name__ == "__main__":
    # node_counts = [4,5,6]  # Different graph sizes
    # check_nodes = (0, 3, 2)  # Check if node 0 can reach node 5 without passing through node 2
    node_counts = []
    for i in range(40):
        node_counts.append(random.choice(range(28,40)))   # easy- range(4,14)   med- (14,28)   hard- (28,40)

    generate_random_graphs(node_counts)

