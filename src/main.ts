/**
 * @gftd:main-entry
 * Main entry point for TypeGPU-based topology visualization
 */
import { TopologyVisualizer } from "./visualization/typegpu-renderer";

async function main() {
  console.log("Initializing topology visualizer...");
  
  const canvas = document.getElementById("topology-canvas") as HTMLCanvasElement;
  if (!canvas) {
    throw new Error("Canvas element not found");
  }

  try {
    const visualizer = new TopologyVisualizer(canvas);
    await visualizer.initialize();
    console.log("Visualizer initialized successfully");

    // Load initial topology
    const topologySelect = document.getElementById("topology-select") as HTMLSelectElement;
    if (!topologySelect) {
      throw new Error("Topology select element not found");
    }
    
    console.log(`Loading initial topology: ${topologySelect.value}`);
    await visualizer.loadTopology(topologySelect.value);
    console.log("Initial topology loaded");

    // Handle topology switching
    topologySelect.addEventListener("change", async (e) => {
      const target = e.target as HTMLSelectElement;
      console.log(`Switching to topology: ${target.value}`);
      await visualizer.loadTopology(target.value);
    });

    // Handle camera reset
    const resetButton = document.getElementById("reset-camera");
    resetButton?.addEventListener("click", () => {
      visualizer.resetCamera();
    });

    // Start render loop
    console.log("Starting render loop...");
    visualizer.start();
  } catch (error) {
    console.error("Failed to initialize visualizer:", error);
    const errorDiv = document.createElement("div");
    errorDiv.style.cssText = "position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: red; background: rgba(0,0,0,0.8); padding: 20px; border-radius: 8px;";
    errorDiv.textContent = `Error: ${error instanceof Error ? error.message : String(error)}`;
    document.body.appendChild(errorDiv);
  }
}

main().catch((error) => {
  console.error("Unhandled error:", error);
});

