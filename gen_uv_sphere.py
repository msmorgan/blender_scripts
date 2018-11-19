import bmesh
import bpy
import math
import mathutils

segments = 32
ring_count = 16
size = 1.0

scene = bpy.context.scene

mesh = bpy.data.meshes.new('UVSphere')
spiral_sphere = bpy.data.objects.new('UVSphere', mesh)

scene.objects.link(spiral_sphere)
scene.objects.active = spiral_sphere
spiral_sphere.select = True

bm = bmesh.new()

top = bm.verts.new((0.0, 0.0, 1.0))

prev_ring = None
ring = []

for r in range(ring_count):
    ring = []

    for s in range(segments):
        xy_theta = s * 2 * math.pi / segments
        z_theta = r * math.pi / ring_count

        x = math.sin(xy_theta) * math.sin(z_theta)
        y = math.cos(xy_theta) * math.sin(z_theta)
        z = math.cos(z_theta)

        vert = bm.verts.new((x, y, z))
        ring.append(vert)

    for s in range(segments):
        next_s = (s + 1) % segments
        if r == 0:
            bm.faces.new([ring[next_s], ring[s], top])
        else:
            bm.faces.new([ring[next_s], ring[s], prev_ring[s], prev_ring[next_s]])

    prev_ring = ring

bottom = bm.verts.new((0.0, 0.0, -1.0))

for s in range(segments):
    next_s = (s + 1) % segments
    bm.faces.new([bottom, prev_ring[s], prev_ring[next_s]])

bm.to_mesh(mesh)
bm.free()
