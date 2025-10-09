import matplotlib.pyplot as plt
import sys
import os

# Add the abstractions directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from abstractions.topologies import RingTopology

def main():
    """
    Builds and visualizes the Japanese Ring Topology interactively.
    """
    topo = RingTopology()
    topo.build_graph()

    # # Static visualization (optional)
    # fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    # topo.visualize(ax)
    # plt.tight_layout()
    # output_filename_png = "japanese_ring_topology.png"
    # plt.savefig(output_filename_png)
    # print(f"Static visualization saved to {output_filename_png}")

    # Interactive visualization
    output_filename_html = "japanese_ring_topology.html"
    topo.visualize_interactive(output_filename_html)
    print(f"Interactive visualization saved to {output_filename_html}")

if __name__ == "__main__":
    main()
