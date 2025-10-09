import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from pyvis.network import Network
import webbrowser
import os
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3D

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

    def visualize_interactive(self, filename="interactive_topology.html"):
        """
        Generates an interactive HTML visualization of the graph using pyvis.
        """
        is_directed = isinstance(self.graph, nx.DiGraph)
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", notebook=True, directed=is_directed)
        net.from_nx(self.graph)

        # Customize node appearance based on 'type' attribute
        for node in net.nodes:
            node_type = self.graph.nodes[node['id']].get('type', 'default')
            if node_type == 'vowel' or node_type == 'final' or node_type == 'vowel_pattern':
                node['color'] = 'skyblue'
                node['size'] = 25
            elif node_type == 'consonant' or node_type == 'initial' or node_type == 'root' or node_type == 'stem':
                node['color'] = 'lightcoral'
                node['size'] = 30
            else: # syllable, derivation, word
                node['color'] = 'lightgreen'
                node['size'] = 20
        
        # For directed graphs, customize arrows
        if is_directed:
            net.set_options("""
            var options = {
              "edges": {
                "arrows": {
                  "to": {
                    "enabled": true,
                    "scaleFactor": 0.5
                  }
                }
              }
            }
            """)
        
        # Show the interactive plot in a new browser tab
        try:
            path = os.path.abspath(filename)
            net.save_graph(filename)
            webbrowser.open(f"file://{path}")
        except Exception as e:
            print(f"Could not open browser: {e}")


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

class LayeredTopology(LanguageTopology):
    """
    Represents a Semitic-like layered topology.
    - Vowels (Phase Space): A set of vowel patterns.
    - Consonants (Operators): A tri-consonantal root that acts as a higher-order
      operator, taking a vowel pattern to produce a word.
    """
    def __init__(self):
        super().__init__()
        self.graph = nx.DiGraph()
        self.title = "Layered Topology (Semitic-like)"
        self.root = 'K-T-B'
        self.vowel_patterns = ['a-a-a', 'u-i-a', 'i-aa']
        self.words = {
            'a-a-a': 'kataba',
            'u-i-a': 'kutiba',
            'i-aa': 'kitaab'
        }

    def build_graph(self):
        # Add root and vowel pattern nodes
        self.graph.add_node(self.root, type='root')
        for pattern in self.vowel_patterns:
            self.graph.add_node(pattern, type='vowel_pattern')

        # Add word nodes and connect them
        for pattern, word in self.words.items():
            self.graph.add_node(word, type='word')
            # Edges show the generation process from root and pattern
            self.graph.add_edge(self.root, word)
            self.graph.add_edge(pattern, word)
    
    def visualize(self, ax):
        pos = {}
        # Manually create a layered layout
        pos[self.root] = (0, 1)
        
        pattern_x_coords = np.linspace(-1, 1, len(self.vowel_patterns))
        for i, pattern in enumerate(self.vowel_patterns):
            pos[pattern] = (pattern_x_coords[i], -1)

        word_x_coords = np.linspace(-1, 1, len(self.words))
        for i, (pattern, word) in enumerate(self.words.items()):
            pos[word] = (word_x_coords[i], 0)

        node_colors = []
        for node, data in self.graph.nodes(data=True):
            if data['type'] == 'root':
                node_colors.append('lightcoral')
            elif data['type'] == 'vowel_pattern':
                node_colors.append('skyblue')
            else: # word
                node_colors.append('lightgreen')

        nx.draw(self.graph, ax=ax, pos=pos, with_labels=True, node_color=node_colors, arrows=True, node_size=1500, font_size=10)
        ax.set_title(self.title, fontsize=15)

    def visualize_3d_pyramid(self, fig):
        """
        Visualizes the layered topology as a 3D pyramid.
        """
        ax = fig.add_subplot(111, projection='3d')
        ax.set_title(self.title, fontsize=15)

        # 1. Define 3D coordinates for nodes
        pos = {
            # Apex of the pyramid
            self.root: (0, 0, 1),
            # Base of the pyramid (a triangle)
            self.vowel_patterns[0]: (0, 1, 0),
            self.vowel_patterns[1]: (-0.866, -0.5, 0),
            self.vowel_patterns[2]: (0.866, -0.5, 0),
        }
        # Place words on the edges between the root and vowel patterns
        for pattern, word in self.words.items():
            root_pos = np.array(pos[self.root])
            pattern_pos = np.array(pos[pattern])
            # Position the word halfway along the edge
            pos[word] = tuple(root_pos + 0.5 * (pattern_pos - root_pos))

        # 2. Plot nodes
        for node, (x, y, z) in pos.items():
            node_type = self.graph.nodes[node]['type']
            if node_type == 'root':
                color = 'lightcoral'
            elif node_type == 'vowel_pattern':
                color = 'skyblue'
            else: # word
                color = 'lightgreen'
            ax.scatter(x, y, z, c=color, s=1500, edgecolors='black')
            ax.text(x, y, z, f'  {node}', size=10, zorder=1, color='k')
            
        # 3. Plot edges
        for edge in self.graph.edges():
            start_pos = pos[edge[0]]
            end_pos = pos[edge[1]]
            line = Line3D(*zip(start_pos, end_pos), color="black", linestyle='--')
            ax.add_line(line)
            
        # 4. Draw the base of the pyramid
        base_points = [pos[p] for p in self.vowel_patterns]
        base_points.append(base_points[0]) # close the loop
        xs, ys, zs = zip(*base_points)
        ax.plot(xs, ys, zs, color="gray")

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        
        # Make the panes transparent
        ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        # Make the grid lines transparent
        ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
        ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
        ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)
        # Remove axes
        ax.set_axis_off()



class LinearTopology(LanguageTopology):
    """
    Represents a Turkish-like linear (DAG) topology.
    - Vowels (Phase Space): The state of the word, subject to vowel harmony.
    - Consonants/Suffixes (Operators): Sequential operators that transition
      the state (word) to a new one.
    """
    def __init__(self):
        super().__init__()
        self.graph = nx.DiGraph()
        self.title = "Linear (DAG) Topology (Turkish-like)"
        self.derivations = ["göz", "gözlük", "gözlükçü", "gözlükçüler"]

    def build_graph(self):
        # Add nodes for each step in the derivation
        for i, word in enumerate(self.derivations):
            self.graph.add_node(word, type='stem' if i == 0 else 'derivation')
        
        # Add edges to show the linear sequence
        for i in range(len(self.derivations) - 1):
            self.graph.add_edge(self.derivations[i], self.derivations[i+1])

    def visualize(self, ax):
        try:
            pos = nx.nx_agraph.graphviz_layout(self.graph, prog='dot', args='-Grankdir=LR')
        except ImportError:
            print("Graphviz not found, using a spring layout as a fallback for the linear topology.")
            pos = nx.spring_layout(self.graph, seed=42)

        node_colors = ['lightcoral' if d['type'] == 'stem' else 'lightgreen' for n, d in self.graph.nodes(data=True)]
        nx.draw(self.graph, ax=ax, pos=pos, with_labels=True, node_color=node_colors, arrows=True, node_size=1800, font_size=10)
        ax.set_title(self.title, fontsize=15)
