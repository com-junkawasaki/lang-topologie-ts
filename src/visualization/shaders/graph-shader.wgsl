// Graph visualization shader for WebGPU
// Renders nodes as circles and edges as lines

struct VertexInput {
  @location(0) position: vec2<f32>,
  @location(1) color: vec3<f32>,
  @location(2) size: f32,
};

struct VertexOutput {
  @builtin(position) position: vec4<f32>,
  @location(0) color: vec3<f32>,
  @location(1) worldPos: vec2<f32>,
  @location(2) size: f32,
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
  let worldPos = input.position - uniforms.cameraPos;
  let scaledPos = worldPos * uniforms.zoom;
  let transformedPos = vec3<f32>(scaledPos, 1.0);
  let viewPos = uniforms.viewMatrix * transformedPos;
  
  output.position = vec4<f32>(viewPos.xy, 0.0, 1.0);
  output.color = input.color;
  output.worldPos = input.position;
  output.size = input.size;
  
  return output;
}

@fragment
fn fs_main(input: VertexOutput) -> @location(0) vec4<f32> {
  // For nodes: render as filled circles
  // For edges: render as lines (handled by geometry shader or instancing)
  return vec4<f32>(input.color, 1.0);
}

