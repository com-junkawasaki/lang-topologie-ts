/**
 * @gftd:typegpu-renderer
 * Core WebGPU renderer using TypeGPU for topology visualization
 */
import { TopologyData, loadTopologyData, TopologyNode, TopologyEdge } from "./topology-data";
import { createShaderModule, createUniformBuffer, createVertexBuffer } from "./shader-utils";

export class TopologyVisualizer {
  private canvas: HTMLCanvasElement;
  private device: GPUDevice | null = null;
  private context: GPUCanvasContext | null = null;
  private currentTopology: TopologyData | null = null;
  private camera = {
    x: 0,
    y: 0,
    zoom: 1.0,
  };
  private shaderModule: GPUShaderModule | null = null;
  private nodePipeline: GPURenderPipeline | null = null;
  private edgePipeline: GPURenderPipeline | null = null;
  private uniformBuffer: GPUBuffer | null = null;
  private nodeBuffers: {
    vertex: GPUBuffer | null;
    index: GPUBuffer | null;
    count: number;
  } = { vertex: null, index: null, count: 0 };
  private edgeBuffers: {
    vertex: GPUBuffer | null;
    count: number;
  } = { vertex: null, count: 0 };

  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas;
  }

  async initialize(): Promise<void> {
    // Initialize WebGPU context
    if (!navigator.gpu) {
      throw new Error("WebGPU is not supported in this browser");
    }

    const adapter = await navigator.gpu.requestAdapter();
    if (!adapter) {
      throw new Error("Failed to get GPU adapter");
    }

    const device = await adapter.requestDevice();
    this.device = device as unknown as GPUDevice;

    // Setup canvas context
    this.context = this.canvas.getContext("webgpu");
    if (!this.context) {
      throw new Error("Failed to get WebGPU context");
    }

    const format = navigator.gpu.getPreferredCanvasFormat();
    this.context.configure({
      device: this.device,
      format,
      alphaMode: "premultiplied",
    });

    // Setup canvas resize handler
    this.resizeCanvas();
    window.addEventListener("resize", () => this.resizeCanvas());

    // Setup mouse controls
    this.setupControls();

    // Load and compile shaders
    await this.loadShaders();
  }

  private async loadShaders(): Promise<void> {
    if (!this.device) return;

    // Inline shader code (WGSL)
    const shaderCode = `
struct VertexInput {
  @location(0) position: vec2<f32>,
  @location(1) color: vec3<f32>,
  @location(2) size: f32,
};

struct VertexOutput {
  @builtin(position) position: vec4<f32>,
  @location(0) color: vec3<f32>,
};

struct Uniforms {
  viewMatrix: mat3x3<f32>,
  cameraPos: vec2<f32>,
  zoom: f32,
}

@group(0) @binding(0) var<uniform> uniforms: Uniforms;

@vertex
fn vs_main(input: VertexInput) -> VertexOutput {
  var output: VertexOutput;
  
  // Apply camera transformation
  // Transform from world space to NDC
  let worldPos = input.position - uniforms.cameraPos;
  let transformedPos = vec3<f32>(worldPos, 1.0);
  let viewPos = uniforms.viewMatrix * transformedPos;
  
  output.position = vec4<f32>(viewPos.xy, 0.0, 1.0);
  output.color = input.color;
  
  return output;
}

@fragment
fn fs_main(input: VertexOutput) -> @location(0) vec4<f32> {
  return vec4<f32>(input.color, 1.0);
}
`;

    this.shaderModule = this.device.createShaderModule({
      label: "Graph Shader",
      code: shaderCode,
    });

    // Create uniform buffer
    // mat3x3 = 12 floats (48 bytes), vec2 = 2 floats (8 bytes), f32 = 1 float (4 bytes)
    // Total: 60 bytes, but must be aligned to 16 bytes = 64 bytes
    this.uniformBuffer = createUniformBuffer(this.device, 64);

    const vertexBufferLayout: GPUVertexBufferLayout = {
      arrayStride: 6 * 4, // position (2) + color (3) + size (1) = 6 floats
      attributes: [
        { shaderLocation: 0, offset: 0, format: "float32x2" }, // position
        { shaderLocation: 1, offset: 8, format: "float32x3" }, // color
        { shaderLocation: 2, offset: 20, format: "float32" }, // size
      ],
    };

    // Create node render pipeline (triangles for circles)
    this.nodePipeline = this.device.createRenderPipeline({
      label: "Node Render Pipeline",
      layout: "auto",
      vertex: {
        module: this.shaderModule,
        entryPoint: "vs_main",
        buffers: [vertexBufferLayout],
      },
      fragment: {
        module: this.shaderModule,
        entryPoint: "fs_main",
        targets: [{ format: navigator.gpu.getPreferredCanvasFormat() }],
      },
      primitive: {
        topology: "triangle-list",
      },
    });

    // Create edge render pipeline (lines)
    this.edgePipeline = this.device.createRenderPipeline({
      label: "Edge Render Pipeline",
      layout: "auto",
      vertex: {
        module: this.shaderModule,
        entryPoint: "vs_main",
        buffers: [vertexBufferLayout],
      },
      fragment: {
        module: this.shaderModule,
        entryPoint: "fs_main",
        targets: [{ format: navigator.gpu.getPreferredCanvasFormat() }],
      },
      primitive: {
        topology: "line-list",
      },
    });
  }

  private resizeCanvas(): void {
    const dpr = window.devicePixelRatio || 1;
    const rect = this.canvas.getBoundingClientRect();
    this.canvas.width = rect.width * dpr;
    this.canvas.height = rect.height * dpr;
  }

  private setupControls(): void {
    let isDragging = false;
    let lastX = 0;
    let lastY = 0;

    this.canvas.addEventListener("mousedown", (e) => {
      isDragging = true;
      lastX = e.clientX;
      lastY = e.clientY;
    });

    this.canvas.addEventListener("mousemove", (e) => {
      if (isDragging) {
        const dx = e.clientX - lastX;
        const dy = e.clientY - lastY;
        this.camera.x += dx * 0.01;
        this.camera.y += dy * 0.01;
        lastX = e.clientX;
        lastY = e.clientY;
      }
    });

    this.canvas.addEventListener("mouseup", () => {
      isDragging = false;
    });

    this.canvas.addEventListener("wheel", (e) => {
      e.preventDefault();
      this.camera.zoom += e.deltaY * -0.001;
      this.camera.zoom = Math.max(0.1, Math.min(5.0, this.camera.zoom));
    });
  }

  async loadTopology(name: string): Promise<void> {
    this.currentTopology = await loadTopologyData(name);
    this.updateInfo();
    await this.updateBuffers();
  }

  private async updateBuffers(): Promise<void> {
    if (!this.device || !this.currentTopology) return;

    // Compute layout for nodes
    const nodes = this.computeLayout(this.currentTopology.nodes);

    // Create node vertex data (instanced rendering as circles)
    const nodeVertices: number[] = [];
    const nodeIndices: number[] = [];
    let indexOffset = 0;

    for (const node of nodes) {
      const color = this.getNodeColor(node.type);
      const size = this.getNodeSize(node.type);
      const x = node.x ?? 0;
      const y = node.y ?? 0;

      // Create a circle with 12 vertices
      const segments = 12;
      const centerIndex = indexOffset;
      nodeVertices.push(x, y, ...color, size); // Center vertex

      for (let i = 0; i <= segments; i++) {
        const angle = (i / segments) * Math.PI * 2;
        const vx = x + Math.cos(angle) * size;
        const vy = y + Math.sin(angle) * size;
        nodeVertices.push(vx, vy, ...color, size);

        if (i > 0) {
          nodeIndices.push(centerIndex, indexOffset + i - 1, indexOffset + i);
        }
      }
      indexOffset += segments + 2;
    }

    // Create edge vertex data
    const edgeVertices: number[] = [];
    for (const edge of this.currentTopology.edges) {
      const sourceNode = nodes.find((n) => n.id === edge.source);
      const targetNode = nodes.find((n) => n.id === edge.target);

      if (sourceNode && targetNode) {
        const sx = sourceNode.x ?? 0;
        const sy = sourceNode.y ?? 0;
        const tx = targetNode.x ?? 0;
        const ty = targetNode.y ?? 0;
        const color = [0.5, 0.5, 0.5]; // Gray for edges

        edgeVertices.push(sx, sy, ...color, 1.0);
        edgeVertices.push(tx, ty, ...color, 1.0);
      }
    }

    // Create GPU buffers
    if (nodeVertices.length > 0) {
      this.nodeBuffers.vertex = createVertexBuffer(
        this.device,
        new Float32Array(nodeVertices)
      );
      this.nodeBuffers.index = this.device.createBuffer({
        size: nodeIndices.length * 2,
        usage: GPUBufferUsage.INDEX | GPUBufferUsage.COPY_DST,
      });
      this.device.queue.writeBuffer(
        this.nodeBuffers.index,
        0,
        new Uint16Array(nodeIndices)
      );
      this.nodeBuffers.count = nodeIndices.length;
    }

    if (edgeVertices.length > 0) {
      this.edgeBuffers.vertex = createVertexBuffer(
        this.device,
        new Float32Array(edgeVertices)
      );
      this.edgeBuffers.count = edgeVertices.length / 6;
    }
  }

  private computeLayout(nodes: TopologyNode[]): TopologyNode[] {
    // Simple force-directed layout initialization
    // If nodes don't have positions, assign them in a circle
    const nodesWithPositions = nodes.map((node, i) => {
      if (node.x === undefined || node.y === undefined) {
        const angle = (i / nodes.length) * Math.PI * 2;
        const radius = 2.0;
        return {
          ...node,
          x: Math.cos(angle) * radius,
          y: Math.sin(angle) * radius,
        };
      }
      return node;
    });
    return nodesWithPositions;
  }

  private getNodeColor(type: string): [number, number, number] {
    switch (type) {
      case "vowel":
        return [0.5, 0.8, 1.0]; // Sky blue
      case "consonant":
        return [1.0, 0.5, 0.5]; // Light coral
      case "syllable":
      case "word":
        return [0.5, 1.0, 0.5]; // Light green
      default:
        return [0.8, 0.8, 0.8]; // Gray
    }
  }

  private getNodeSize(type: string): number {
    switch (type) {
      case "vowel":
      case "consonant":
        return 0.15;
      default:
        return 0.1;
    }
  }

  private updateInfo(): void {
    if (!this.currentTopology) return;

    const titleElement = document.getElementById("topology-title");
    const descElement = document.getElementById("topology-description");

    if (titleElement) {
      titleElement.textContent = this.currentTopology.title;
    }
    if (descElement) {
      descElement.textContent = this.currentTopology.description;
    }
  }

  resetCamera(): void {
    this.camera = { x: 0, y: 0, zoom: 1.0 };
  }

  start(): void {
    const render = () => {
      this.render();
      requestAnimationFrame(render);
    };
    render();
  }

  private render(): void {
    if (
      !this.device ||
      !this.context ||
      !this.currentTopology ||
      !this.nodePipeline ||
      !this.edgePipeline ||
      !this.uniformBuffer
    ) {
      return;
    }

    // Update uniform buffer with camera parameters
    const viewMatrix = this.createViewMatrix(this.canvas.width / this.canvas.height);
    // WGSL mat3x3 is column-major: [m00, m10, m20, m01, m11, m21, m02, m12, m22]
    const uniformData = new Float32Array([
      viewMatrix[0][0], viewMatrix[1][0], viewMatrix[2][0], 0, // Column 0 + padding
      viewMatrix[0][1], viewMatrix[1][1], viewMatrix[2][1], 0, // Column 1 + padding
      viewMatrix[0][2], viewMatrix[1][2], viewMatrix[2][2], 0, // Column 2 + padding
      this.camera.x, this.camera.y, this.camera.zoom, 0, // Camera + padding
    ]);
    this.device.queue.writeBuffer(this.uniformBuffer, 0, uniformData);

    const encoder = this.device.createCommandEncoder();
    const pass = encoder.beginRenderPass({
      colorAttachments: [
        {
          view: this.context.getCurrentTexture().createView(),
          clearValue: { r: 0.1, g: 0.1, b: 0.1, a: 1.0 },
          loadOp: "clear",
          storeOp: "store",
        },
      ],
    });

    const bindGroup = this.device.createBindGroup({
      layout: this.nodePipeline.getBindGroupLayout(0),
      entries: [
        {
          binding: 0,
          resource: { buffer: this.uniformBuffer },
        },
      ],
    });

    // Render edges first (so they appear behind nodes)
    if (this.edgeBuffers.vertex && this.edgeBuffers.count > 0) {
      pass.setPipeline(this.edgePipeline);
      pass.setBindGroup(0, bindGroup);
      pass.setVertexBuffer(0, this.edgeBuffers.vertex);
      pass.draw(this.edgeBuffers.count * 2, 1, 0, 0);
    }

    // Render nodes
    if (this.nodeBuffers.vertex && this.nodeBuffers.index && this.nodeBuffers.count > 0) {
      pass.setPipeline(this.nodePipeline);
      pass.setBindGroup(0, bindGroup);
      pass.setVertexBuffer(0, this.nodeBuffers.vertex);
      pass.setIndexBuffer(this.nodeBuffers.index, "uint16");
      pass.drawIndexed(this.nodeBuffers.count, 1, 0, 0);
    }

    pass.end();
    this.device.queue.submit([encoder.finish()]);
  }

  private createViewMatrix(aspect: number): [[number, number, number], [number, number, number], [number, number, number]] {
    // Orthographic projection matrix: scale to NDC and apply zoom
    // NDC ranges from -1 to 1, so we scale by 2/width and 2/height
    const scaleX = (2.0 / this.canvas.width) * this.camera.zoom;
    const scaleY = (2.0 / this.canvas.height) * this.camera.zoom;
    return [
      [scaleX, 0, 0],
      [0, scaleY, 0],
      [0, 0, 1],
    ];
  }
}

