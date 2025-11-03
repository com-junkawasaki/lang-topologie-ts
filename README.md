# Phonosematic Computational Topologies

A research project analyzing phonological structures of natural languages as network topologies, with GPU-accelerated interactive visualizations.

## Project Structure

- `abstractions/` - Python topology models (Ring, Tree, Lattice, Layered, Linear)
- `src/visualization/` - TypeScript/WebGPU visualization application
- `data/topologies/` - Exported topology data in JSON format
- `scripts/` - Data export utilities
- `language_visualizations/` - Original Python-based visualizations

## Setup

### Python Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### TypeScript/Node.js Environment

```bash
pnpm install
```

## Usage

### Export Topology Data

```bash
source venv/bin/activate
python3 scripts/export-topologies.py
```

This generates JSON files in `data/topologies/` for each topology type.

### Run Visualization

```bash
pnpm dev
```

This starts a Vite development server at `http://localhost:3000` with the interactive TypeGPU visualization.

### Build for Production

```bash
pnpm build
```

## Topology Types

1. **Ring** (Japanese) - Cyclic vowel hub with tree-like consonant branches
2. **Tree** (English) - Consonant cluster roots with hierarchical vowel branches
3. **Lattice** (Chinese) - Grid structure with tonal cyclic loops
4. **Layered** (Semitic) - Consonant root layers with vowel pattern projections
5. **Linear** (Turkish) - Sequential DAG with vowel harmony branching

## Paper

See `phonosematic_computational_topologies_paper.md` for the complete research paper.

## License

Apache License 2.0
