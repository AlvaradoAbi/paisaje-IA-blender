import bpy
import numpy as np
from sklearn.cluster import KMeans
import random
import math

# --- Limpieza ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# --- Crear plano subdividido ---
size = 30
subdivs = 70
bpy.ops.mesh.primitive_grid_add(x_subdivisions=subdivs, y_subdivisions=subdivs, size=size)
terrain = bpy.context.object
mesh = terrain.data

# --- Extraer posiciones XY ---
points = np.array([v.co.xy for v in mesh.vertices])

# --- KMeans clustering para 4 zonas: pradera, montaña, lago, bosque ---
n_clusters = 3 #cantidad de regionres 
kmeans = KMeans(n_clusters=n_clusters, n_init='auto')
labels = kmeans.fit_predict(points)

# --- Función para ruido Perlin simple (simulado con sin/cos para evitar librerías extra) ---
def perlin_noise(x, y, scale=1.0):
    return (math.sin(x * scale) * math.cos(y * scale))

# --- Aplicar alturas según cluster con variaciones ---
for i, v in enumerate(mesh.vertices):
    label = labels[i]
    noise = perlin_noise(v.co.x, v.co.y, scale=0.3) * 0.3
    base_height = 0
    if label == 0:  # Pradera - suave y ligeramente ondulado
        base_height = 0.2 + noise
    elif label == 1:  # Montaña - alta, con picos
        base_height = 2.0 + noise * 2 + random.uniform(-0.3, 0.3)
    elif label == 2:  # Lago - plano y ligeramente hundido
        base_height = -0.2 + noise * 0.05
    elif label == 3:  # Bosque - mediana altura con algo de irregularidad
        base_height = 0.7 + noise + random.uniform(-0.1, 0.1)
    v.co.z = base_height

# --- Materiales ---
material_data = [
    ("Pradera", (0.2, 0.6, 0.2, 1), False),
    ("Montaña", (0.5, 0.3, 0.1, 1), False),
    ("Lago", (0.1, 0.3, 0.6, 0.6), True),  # semi-transparente
    ("Bosque", (0.1, 0.4, 0.1, 1), False),
]

materials = []
for name, color, transparent in material_data:
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = color
    if transparent:
        mat.blend_method = 'BLEND'
        mat.shadow_method = 'NONE'
    materials.append(mat)

terrain.data.materials.clear()
for mat in materials:
    terrain.data.materials.append(mat)

# --- Asignar materiales a caras ---
for poly in mesh.polygons:
    face_labels = [labels[v] for v in poly.vertices]
    main_label = max(set(face_labels), key=face_labels.count)
    poly.material_index = main_label

# --- Funciones para elementos naturales ---
def create_tree(location):
    # Tronco
    bpy.ops.mesh.primitive_cylinder_add(radius=0.07, depth=0.6, location=location)
    trunk = bpy.context.object
    trunk_mat = bpy.data.materials.new("TrunkMat")
    trunk_mat.diffuse_color = (0.3, 0.2, 0.1, 1)
    trunk.data.materials.append(trunk_mat)

    # Hojas (conos apilados)
    base_x, base_y, base_z = location
    for i in range(3):
        bpy.ops.mesh.primitive_cone_add(radius1=0.25 - 0.07*i, depth=0.5,
                                        location=(base_x, base_y, base_z + 0.5 + i*0.3))
        leaves = bpy.context.object
        leaves_mat = bpy.data.materials.new("LeavesMat")
        leaves_mat.diffuse_color = (0.05, 0.4 + 0.1*i, 0.05, 1)
        leaves.data.materials.append(leaves_mat)

def create_rock(location):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.15, location=location)
    rock = bpy.context.object
    rock_mat = bpy.data.materials.new("RockMat")
    rock_mat.diffuse_color = (0.4, 0.4, 0.4, 1)
    rock.data.materials.append(rock_mat)

# --- Distribuir árboles en bosque y pradera ---
tree_indices = [i for i, label in enumerate(labels) if label in [0, 3]]  # pradera y bosque
for _ in range(50):
    idx = random.choice(tree_indices)
    v = mesh.vertices[idx]
    loc = (v.co.x + random.uniform(-0.1, 0.1),
           v.co.y + random.uniform(-0.1, 0.1),
           v.co.z)
    create_tree(loc)

# --- Distribuir rocas en montañas ---
montana_indices = [i for i, label in enumerate(labels) if label == 1]
for _ in range(20):
    idx = random.choice(montana_indices)
    v = mesh.vertices[idx]
    loc = (v.co.x + random.uniform(-0.3, 0.3),
           v.co.y + random.uniform(-0.3, 0.3),
           v.co.z)
    create_rock(loc)

# --- Añadir plano de agua para lago ---
bpy.ops.mesh.primitive_plane_add(size=size*0.9, location=(0, 0, 0))
water = bpy.context.object
water_mat = bpy.data.materials.new("WaterMat")
water_mat.diffuse_color = (0.05, 0.25, 0.7, 0.5)
water_mat.blend_method = 'BLEND'
water.data.materials.append(water_mat)

# Ajustar agua para que quede sólo sobre lago (simple aproximación)
water.location.z = -0.15

# --- Configurar cámara y luz para presentación ---
bpy.ops.object.camera_add(location=(size, -size, size*0.8), rotation=(math.radians(60), 0, math.radians(45)))
camera = bpy.context.object
bpy.context.scene.camera = camera

bpy.ops.object.light_add(type='SUN', location=(size, -size, size))
sun = bpy.context.object
sun.data.energy = 4

print("Paisaje generado con clustering y elementos naturales.")
