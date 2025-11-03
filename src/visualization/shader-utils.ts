/**
 * @gftd:shader-utils
 * Utility functions for shader compilation and management
 */

export async function createShaderModule(
  device: GPUDevice,
  code: string,
  label?: string
): Promise<GPUShaderModule> {
  return device.createShaderModule({
    label,
    code,
  });
}

export function createUniformBuffer(device: GPUDevice, size: number): GPUBuffer {
  // Ensure size is a multiple of 16 (WGSL uniform buffer alignment requirement)
  const alignedSize = Math.ceil(size / 16) * 16;
  return device.createBuffer({
    size: alignedSize,
    usage: GPUBufferUsage.UNIFORM | GPUBufferUsage.COPY_DST,
  });
}

export function createVertexBuffer(
  device: GPUDevice,
  data: Float32Array
): GPUBuffer {
  const buffer = device.createBuffer({
    size: data.byteLength,
    usage: GPUBufferUsage.VERTEX | GPUBufferUsage.COPY_DST,
  });
  device.queue.writeBuffer(buffer, 0, data);
  return buffer;
}

export function createIndexBuffer(
  device: GPUDevice,
  data: Uint16Array
): GPUBuffer {
  const buffer = device.createBuffer({
    size: data.byteLength,
    usage: GPUBufferUsage.INDEX | GPUBufferUsage.COPY_DST,
  });
  device.queue.writeBuffer(buffer, 0, data);
  return buffer;
}

