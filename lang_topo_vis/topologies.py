import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class LanguageTopology:
    """
    A base class for representing and visualizing language topologies.
    """
    def __init__(self):
        self.graph = nx.Graph()
        self.vowels = []
        self.consonants = []
        self.title = "Abstract Language Topology"

    def build_graph(self):
        """
        This method should be overridden by subclasses to construct the specific topology.
        """
        raise NotImplementedError

    def visualize(self, ax):
        """
        Visualizes the graph using a specified layout.
        Subclasses can override this to provide a more specific layout.
        """
        pos = nx.spring_layout(self.graph, seed=42)
        nx.draw(self.graph, ax=ax, pos=pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=800, font_size=10)
        ax.set_title(self.title, fontsize=15)

class RingTopology(LanguageTopology):
    """
    Represents a Japanese-like ring topology.
    - Vowels (Phase Space): A cyclic space of 5 vowels.
    - Consonants (Operators): Act on vowels to produce syllables.
    """
    def __init__(self):
        super().__init__()
        self.title = "Ring Topology (Japanese-like)"
        self.vowels = ['a', 'i', 'u', 'e', 'o']
        self.consonants = ['k', 's', 't']

    def build_graph(self):
        # Add vowel nodes (the phase space)
        for vowel in self.vowels:
            self.graph.add_node(vowel, type='vowel')

        # Create the ring structure for vowels
        for i in range(len(self.vowels)):
            self.graph.add_edge(self.vowels[i], self.vowels[(i + 1) % len(self.vowels)])
        
        # Add consonant operators and syllable nodes
        for consonant in self.consonants:
            # The consonant itself can be a node representing the operator
            self.graph.add_node(consonant, type='consonant')
            for vowel in self.vowels:
                syllable = f"{consonant}{vowel}"
                self.graph.add_node(syllable, type='syllable')
                # Edge from operator and vowel to the resulting syllable
                self.graph.add_edge(consonant, syllable)
                self.graph.add_edge(vowel, syllable)

    def visualize(self, ax):
        pos = {}
        # Circular layout for vowels (the phase space)
        vowel_nodes = [n for n, d in self.graph.nodes(data=True) if d['type'] == 'vowel']
        num_vowels = len(vowel_nodes)
        angles = np.linspace(0, 2 * np.pi, num_vowels, endpoint=False)
        for i, node in enumerate(vowel_nodes):
            pos[node] = (np.cos(angles[i]), np.sin(angles[i]))

        # Place consonants outside the vowel ring
        consonant_nodes = [n for n, d in self.graph.nodes(data=True) if d['type'] == 'consonant']
        num_consonants = len(consonant_nodes)
        angles = np.linspace(0, 2 * np.pi, num_consonants, endpoint=False)
        for i, node in enumerate(consonant_nodes):
             pos[node] = (2 * np.cos(angles[i]), 2 * np.sin(angles[i]))

        # Place syllables around their vowel and consonant
        syllable_nodes = [n for n, d in self.graph.nodes(data=True) if d['type'] == 'syllable']
        for node in syllable_nodes:
            consonant = node[0]
            vowel = node[1]
            if consonant in pos and vowel in pos:
                 # Position syllable halfway between its consonant and vowel
                pos[node] = ((pos[consonant][0] + pos[vowel][0]) / 2, (pos[consonant][1] + pos[vowel][1]) / 2)


        node_colors = []
        for node in self.graph.nodes():
            node_type = self.graph.nodes[node]['type']
            if node_type == 'vowel':
                node_colors.append('skyblue')
            elif node_type == 'consonant':
                node_colors.append('lightcoral')
            else: # syllable
                node_colors.append('lightgreen')

        nx.draw(self.graph, ax=ax, pos=pos, with_labels=True, node_color=node_colors, edge_color='gray', node_size=800, font_size=10)
        ax.set_title(self.title, fontsize=15)

class TreeTopology(LanguageTopology):
    """
    Represents an English-like tree topology.
    - Vowels (Phase Space): Parameters for branching.
    - Consonants (Operators): Consonant clusters as roots that generate branches.
    """
    def __init__(self):
        super().__init__()
        self.graph = nx.DiGraph() # Tree is a directed graph
        self.title = "Tree Topology (English/German-like)"
        self.roots = ['str', 'cl']
        self.derivations = {
            'str': ['strong', 'strength', 'structure', 'string'],
            'cl': ['clean', 'cluster', 'climb']
        }

    def build_graph(self):
        for root in self.roots:
            self.graph.add_node(root, type='root')
            for derivation in self.derivations[root]:
                self.graph.add_node(derivation, type='derivation')
                self.graph.add_edge(root, derivation)

    def visualize(self, ax):
        try:
            # Use graphviz layout for a hierarchical tree structure
            pos = nx.nx_agraph.graphviz_layout(self.graph, prog='dot')
        except ImportError:
            # Fallback if graphviz is not installed
            print("Graphviz not found, using a spring layout as a fallback for the tree.")
            pos = nx.spring_layout(self.graph, seed=42)
            
        node_colors = ['lightcoral' if d['type'] == 'root' else 'lightgreen' for n, d in self.graph.nodes(data=True)]
        nx.draw(self.graph, ax=ax, pos=pos, with_labels=True, node_color=node_colors, arrows=True, node_size=1200, font_size=10)
        ax.set_title(self.title, fontsize=15)

class LatticeTopology(LanguageTopology):
    """
    Represents a Chinese-like lattice topology.
    - Vowels (Phase Space): Finals/rimes form one axis.
    - Consonants (Operators): Initials form the other axis.
    - Tones: An additional property of the syllable nodes.
    """
    def __init__(self):
        super().__init__()
        self.title = "Lattice Topology (Chinese-like)"
        # Initials (Consonants)
        self.initials = ['b', 'p', 'm']
        # Finals (Vowels/Rimes)
        self.finals = ['a', 'o', 'i']
        # Valid syllables with tones
        self.syllables = {
            ('b', 'a'): [1, 4], ('b', 'o'): [1], ('p', 'o'): [1, 2],
            ('m', 'a'): [1], ('m', 'o'): [1, 2]
        }

    def build_graph(self):
        pos = {}
        for i, initial in enumerate(self.initials):
            self.graph.add_node(initial, type='initial')
            pos[initial] = (i, 1)
        for j, final in enumerate(self.finals):
            self.graph.add_node(final, type='final')
            pos[final] = (j, 0)
        
        for (initial, final), tones in self.syllables.items():
            syllable_base = f"{initial}{final}"
            self.graph.add_node(syllable_base, type='syllable')
            pos[syllable_base] = (self.initials.index(initial), 0.5)
            self.graph.add_edge(initial, syllable_base)
            self.graph.add_edge(final, syllable_base)
            # Add tones as attributes, could also be separate nodes
            self.graph.nodes[syllable_base]['tones'] = tones
        
        # Store position for visualization
        self.pos = pos


    def visualize(self, ax):
        node_colors = []
        labels = {}
        for node, data in self.graph.nodes(data=True):
            labels[node] = node
            if data['type'] == 'initial':
                node_colors.append('lightcoral')
            elif data['type'] == 'final':
                node_colors.append('skyblue')
            else: # syllable
                node_colors.append('lightgreen')
                # Add tone information to the label
                labels[node] = f"{node}\n{data['tones']}"


        nx.draw(self.graph, ax=ax, pos=self.pos, with_labels=False, node_color=node_colors, node_size=1500)
        nx.draw_networkx_labels(self.graph, self.pos, labels, font_size=9, ax=ax)
        ax.set_title(self.title, fontsize=15)
        ax.set_aspect('equal', adjustable='box')
