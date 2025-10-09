import matplotlib.pyplot as plt
import sys
import os

# Add the abstractions directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from abstractions.topologies import LinearTopology

def main():
    """
    Builds and visualizes the Turkish Linear Topology.
    """
    topo = LinearTopology()
    topo.build_graph()

    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    topo.visualize(ax)

    plt.tight_layout()
    
    output_filename = "turkish_linear_topology.png"
    plt.savefig(output_filename)
    print(f"Visualization saved to {output_filename}")

if __name__ == "__main__":
    main()
