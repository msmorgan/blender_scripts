import bmesh
import bpy
import math
import mathutils

ring_count = 16
segments = ring_count * 2
size = 1.0

scene = bpy.context.scene

mesh = bpy.data.meshes.new('SpiralSphere')
spiral_sphere = bpy.data.objects.new('SpiralSphere', mesh)

scene.objects.link(spiral_sphere)
scene.objects.active = spiral_sphere
spiral_sphere.select = True

bm = bmesh.new()

prev_ring = None
ring = []
prev_prev_last = None

for r in range(ring_count):
    ring = []

    for s in range(segments):
        xy_theta = s * 2 * math.pi / segments
        z_theta = (r + (s / segments)) * math.pi / ring_count

        x = math.cos(xy_theta) * math.sin(z_theta)
        y = math.sin(xy_theta) * math.sin(z_theta)
        z = math.cos(z_theta)

        vert = bm.verts.new((x, y, z))
        ring.append(vert)

    if r == 1:
        bm.faces.new([prev_ring[segments - 1], ring[0], prev_ring[0]])
    elif r > 1:
        bm.faces.new([prev_ring[segments - 1], ring[0], prev_ring[0], prev_prev_last])

    for s in range(segments - 1):
        if r == 0:
            if s != 0:
                bm.faces.new([ring[s], ring[s+1], ring[0]])
        else:
            bm.faces.new([ring[s], ring[s+1], prev_ring[s+1], prev_ring[s]])

    if prev_ring is not None:
        prev_prev_last = prev_ring[segments - 1]
    prev_ring = ring

bottom = bm.verts.new((0.0, 0.0, -1.0))

bm.faces.new([bottom, prev_ring[0], prev_prev_last])

for s in range(segments - 1):
    bm.faces.new([bottom, prev_ring[s+1], prev_ring[s]])

bm.verts.ensure_lookup_table()
bm.verts.index_update()

uv_layer = bm.loops.layers.uv.new()
for face in bm.faces:
    safe = False
    for l in range(len(face.loops)):
        loop = face.loops[l]
        x, y, z = loop.vert.co

        u = math.atan2(y, x) / (2 * math.pi)
        if u < 0.0:
            u += 1.0

        v = -math.acos(z) / math.pi

        if l == 0 and u == 0:
            safe = True
        if u == 0.0 and not safe:
            u = 1.0

        loop[uv_layer].uv = mathutils.Vector((u, v))

for v in bm.verts:
    v.co *= size

bm.to_mesh(mesh)
bm.free()
