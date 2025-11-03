#!/usr/bin/env python3
"""
Export topology graph data as JSON/JSON-LD from existing Python classes.
"""
import json
import sys
import os
from pathlib import Path

# Add the abstractions directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from abstractions.topologies import (
    RingTopology,
    TreeTopology,
    LatticeTopology,
    LayeredTopology,
    LinearTopology
)

def export_topology(topo, name: str, output_dir: Path):
    """Export a topology to JSON format."""
    topo.build_graph()
    
    # Extract nodes with attributes
    nodes = []
    for node_id, attrs in topo.graph.nodes(data=True):
        node = {
            "id": str(node_id),
            "label": str(node_id),
            "type": attrs.get("type", "default")
        }
        
        # Try to get position if layout has been computed
        if "pos" in attrs:
            pos = attrs["pos"]
            if isinstance(pos, (list, tuple)) and len(pos) >= 2:
                node["x"] = float(pos[0])
                node["y"] = float(pos[1])
                if len(pos) >= 3:
                    node["z"] = float(pos[2])
        
        nodes.append(node)
    
    # Extract edges
    edges = []
    for source, target, attrs in topo.graph.edges(data=True):
        edge = {
            "source": str(source),
            "target": str(target)
        }
        if topo.graph.is_directed():
            edge["directed"] = True
        if "weight" in attrs:
            edge["weight"] = float(attrs["weight"])
        edges.append(edge)
    
    # Create topology data structure
    topology_type_map = {
        RingTopology: ("ring", "Ring Topology (Japanese)", "Vowels form a cyclic hub, consonants branch tree-like.", "circular"),
        TreeTopology: ("tree", "Tree Topology (English)", "Consonant clusters form roots, vowels branch hierarchically.", "hierarchical"),
        LatticeTopology: ("lattice", "Lattice Topology (Chinese)", "Consonants and vowels form a grid, tones add cyclic loops.", "grid"),
        LayeredTopology: ("layered", "Layered Topology (Semitic)", "Consonant roots form layers, vowel patterns project as grids.", "multilayer"),
        LinearTopology: ("linear", "Linear Topology (Turkish)", "Stem to suffix DAG with vowel harmony branching.", "sequential"),
    }
    
    topo_type, title, description, layout = topology_type_map.get(type(topo), (name, f"{name} Topology", "No description", "circular"))
    
    topology_data = {
        "name": name,
        "title": title,
        "description": description,
        "nodes": nodes,
        "edges": edges,
        "metadata": {
            "topologyType": topo_type,
            "layout": layout
        }
    }
    
    # Write to JSON file
    output_file = output_dir / f"{name}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(topology_data, f, indent=2, ensure_ascii=False)
    
    print(f"Exported {name} topology to {output_file}")
    print(f"  Nodes: {len(nodes)}, Edges: {len(edges)}")

def main():
    """Export all topologies."""
    # Create output directory
    output_dir = Path(__file__).parent.parent / "data" / "topologies"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Define topologies to export
    topologies = [
        (RingTopology(), "ring"),
        (TreeTopology(), "tree"),
        (LatticeTopology(), "lattice"),
        (LayeredTopology(), "layered"),
        (LinearTopology(), "linear"),
    ]
    
    # Export each topology
    for topo, name in topologies:
        try:
            export_topology(topo, name, output_dir)
        except Exception as e:
            print(f"Error exporting {name}: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()

