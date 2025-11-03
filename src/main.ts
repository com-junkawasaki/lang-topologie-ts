/**
 * @gftd:main-entry
 * Main entry point for TypeGPU-based topology visualization
 */
import { TopologyVisualizer } from "./visualization/typegpu-renderer";

async function main() {
  const canvas = document.getElementById("topology-canvas") as HTMLCanvasElement;
  if (!canvas) {
    throw new Error("Canvas element not found");
  }

  const visualizer = new TopologyVisualizer(canvas);
  await visualizer.initialize();

  // Load initial topology
  const topologySelect = document.getElementById("topology-select") as HTMLSelectElement;
  await visualizer.loadTopology(topologySelect.value);

  // Handle topology switching
  topologySelect.addEventListener("change", async (e) => {
    const target = e.target as HTMLSelectElement;
    await visualizer.loadTopology(target.value);
  });

  // Handle camera reset
  const resetButton = document.getElementById("reset-camera");
  resetButton?.addEventListener("click", () => {
    visualizer.resetCamera();
  });

  // Start render loop
  visualizer.start();
}

main().catch(console.error);

