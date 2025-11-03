/**
 * @gftd:topology-data
 * Data structures and loaders for topology visualization
 */

export interface TopologyNode {
  id: string;
  label: string;
  type: "vowel" | "consonant" | "syllable" | "word" | "root" | "pattern";
  x?: number;
  y?: number;
  z?: number;
  color?: [number, number, number];
}

export interface TopologyEdge {
  source: string;
  target: string;
  directed?: boolean;
  weight?: number;
}

export interface TopologyData {
  name: string;
  title: string;
  description: string;
  nodes: TopologyNode[];
  edges: TopologyEdge[];
  metadata?: {
    topologyType: "ring" | "tree" | "lattice" | "layered" | "linear";
    layout?: "circular" | "hierarchical" | "grid" | "multilayer" | "sequential";
  };
}

export async function loadTopologyData(name: string): Promise<TopologyData> {
  try {
    const response = await fetch(`/data/topologies/${name}.json`);
    if (!response.ok) {
      throw new Error(`Failed to load topology: ${name}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Error loading topology ${name}:`, error);
    // Return empty topology as fallback
    return {
      name,
      title: `${name} Topology`,
      description: "Topology data not available",
      nodes: [],
      edges: [],
    };
  }
}

