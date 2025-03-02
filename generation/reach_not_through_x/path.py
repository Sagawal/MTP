import networkx as nx
import os
import random

# Define the number of graphs and the range of sizes
num_graphs = 10  # Number of graphs to create
min_nodes = 13    # Minimum number of nodes in a graph
max_nodes = 22   # Maximum number of nodes in a graph


# Directory to save the edge files
output_dir = "D:\\IITDelhi\\Sem5\\Project\\NLGraph-main\\NLGraph-main\\NLGraph\\reach_not_through_x\\graph" + "\\medium" + "\\path"
os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

# Generate graphs and save their shuffled edges to files
for graph_id in range(max_nodes+1-min_nodes):
    for i in range(2):
        # Randomly determine the number of nodes for this graph
        num_nodes = min_nodes + graph_id  # Ensures variety within range
        
        # Create the path graph
        G = nx.path_graph(num_nodes)

        # Get edges and shuffle them
        edges = list(G.edges())
        random.shuffle(edges)  # Shuffle the edges in random order
        
        # File to store the edges
        file_path = os.path.join(output_dir, f"graph{graph_id*2+i}.txt")

        # Write the shuffled edges to the file
        with open(file_path, "w") as file:
            file.write(f"{len(G.nodes())} {len(G.edges())}\n")
            for edge in edges:
                file.write(f"{edge[0]} {edge[1]}\n")

            # query-1
            no_of_nodes = list(range(0,len(G.nodes)))
            selected_values = random.sample(no_of_nodes, 3)
            selected_values.sort()
            file.write(f"{selected_values[0]} {selected_values[2]} {selected_values[1]}\n")

            # query-2
            selected_values = random.sample(no_of_nodes, 3)
            selected_values.sort()
            file.write(f"{selected_values[0]} {selected_values[1]} {selected_values[2]}\n")
        