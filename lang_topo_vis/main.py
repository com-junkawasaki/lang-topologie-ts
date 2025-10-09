import matplotlib.pyplot as plt
from topologies import RingTopology, TreeTopology, LatticeTopology, LayeredTopology, LinearTopology

def main():
    """
    Main function to build and visualize language topologies.
    """
    # Instantiate the different topology models
    topologies = [
        RingTopology(),
        TreeTopology(),
        LatticeTopology(),
        LayeredTopology(),
        LinearTopology()
    ]

    # Build the graph for each topology
    for topo in topologies:
        topo.build_graph()

    # Create a figure to display the visualizations
    # Arrange plots in a 2x3 grid for better layout
    fig, axes = plt.subplots(2, 3, figsize=(22, 14))
    axes = axes.flatten() # Flatten the 2D array of axes for easy iteration

    # Visualize each topology
    for i, topo in enumerate(topologies):
        topo.visualize(axes[i])

    # Hide any unused subplots
    for i in range(len(topologies), len(axes)):
        fig.delaxes(axes[i])


    plt.tight_layout()
    
    # Save the figure to a file
    output_filename = "language_topologies_extended.png"
    plt.savefig(output_filename)
    print(f"Visualization saved to {output_filename}")

    # To display the plot in an interactive environment, you might use:
    # plt.show()

if __name__ == "__main__":
    main()
