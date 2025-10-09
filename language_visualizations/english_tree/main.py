import matplotlib.pyplot as plt
import sys
import os

# Add the abstractions directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from abstractions.topologies import TreeTopology

def main():
    """
    Builds and visualizes the English Tree Topology interactively.
    """
    topo = TreeTopology()
    topo.build_graph()

    # Interactive visualization
    output_filename_html = "english_tree_topology.html"
    topo.visualize_interactive(output_filename_html)
    print(f"Interactive visualization saved to {output_filename_html}")

if __name__ == "__main__":
    main()
