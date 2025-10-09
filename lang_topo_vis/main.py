import matplotlib.pyplot as plt
from topologies import RingTopology, TreeTopology, LatticeTopology

def main():
    """
    Main function to build and visualize language topologies.
    """
    # Instantiate the different topology models
    topologies = [
        RingTopology(),
        TreeTopology(),
        LatticeTopology()
    ]

    # Build the graph for each topology
    for topo in topologies:
        topo.build_graph()

    # Create a figure to display the visualizations
    fig, axes = plt.subplots(1, len(topologies), figsize=(20, 7))
    if len(topologies) == 1:
        axes = [axes] # Make it iterable if there is only one plot

    # Visualize each topology
    for ax, topo in zip(axes, topologies):
        topo.visualize(ax)

    plt.tight_layout()
    
    # Save the figure to a file
    output_filename = "language_topologies.png"
    plt.savefig(output_filename)
    print(f"Visualization saved to {output_filename}")

    # To display the plot in an interactive environment, you might use:
    # plt.show()

if __name__ == "__main__":
    main()
