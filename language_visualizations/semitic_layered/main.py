import matplotlib.pyplot as plt
import sys
import os

# Add the abstractions directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from abstractions.topologies import LayeredTopology

def main():
    """
    Builds and visualizes the Semitic Layered Topology in 3D.
    """
    topo = LayeredTopology()
    topo.build_graph()

    # 3D Static visualization
    fig = plt.figure(figsize=(10, 10))
    topo.visualize_3d_pyramid(fig)
    output_filename_png = "semitic_pyramid_topology.png"
    plt.savefig(output_filename_png)
    print(f"3D visualization saved to {output_filename_png}")

    # # Interactive visualization (2D)
    # output_filename_html = "semitic_layered_topology.html"
    # topo.visualize_interactive(output_filename_html)
    # print(f"Interactive visualization saved to {output_filename_html}")

if __name__ == "__main__":
    main()
