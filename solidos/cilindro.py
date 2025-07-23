import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D

def cilindro(raio, altura, num_divisoes=20):

    vertices = []
    faces = []
    arestas = []

    centro_base = [0, 0, 0]
    centro_topo = [0, 0, altura]
    vertices.append(centro_base)
    vertices.append(centro_topo)

    angulos = np.linspace(0, 2 * np.pi, num_divisoes, endpoint=False)
    for angulo in angulos:
        x = raio * np.cos(angulo)
        y = raio * np.sin(angulo)
        vertices.append([x, y, 0])
        vertices.append([x, y, altura])

    vertices = np.array(vertices)

    idx_centro_base = 0
    idx_centro_topo = 1

    for i in range(num_divisoes):
        j = (i + 1) % num_divisoes

        idx_base_i = 2 + i * 2
        idx_topo_i = 2 + i * 2 + 1
        idx_base_j = 2 + j * 2
        idx_topo_j = 2 + j * 2 + 1

        faces.append((idx_base_i, idx_topo_j, idx_topo_i))
        faces.append((idx_base_i, idx_base_j, idx_topo_j))

        faces.append((idx_centro_base, idx_base_j, idx_base_i))

        faces.append((idx_centro_topo, idx_topo_i, idx_topo_j))

        arestas.append((idx_base_i, idx_base_j))
        arestas.append((idx_topo_i, idx_topo_j))
        arestas.append((idx_base_i, idx_topo_i))
        arestas.append((idx_centro_base, idx_base_i))
        arestas.append((idx_centro_topo, idx_topo_i))

    return vertices, arestas, faces

if __name__ == '__main__':
    raio_cilindro = 3.0
    altura_cilindro = 7.0

    vertices_cilindro, arestas_cilindro, faces_cilindro = cilindro(
        raio_cilindro, altura_cilindro, num_divisoes=32
    )

    fig = plt.figure(figsize=(10, 8))
    ax: Axes3D = fig.add_subplot(projection='3d')

    poly3d = [vertices_cilindro[list(face)] for face in faces_cilindro]

    ax.add_collection3d(Poly3DCollection(
        poly3d,
        facecolors='cornflowerblue',
        linewidths=0.5,
        edgecolors='black',
        alpha=1.0
    ))

    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')
    ax.set_title('Modelo de Cilindro')

    ax.set_box_aspect([raio_cilindro*2, raio_cilindro*2, altura_cilindro]) # Proporções mais realistas
    ax.set_xlim(-raio_cilindro*1.2, raio_cilindro*1.2)
    ax.set_ylim(-raio_cilindro*1.2, raio_cilindro*1.2)
    ax.set_zlim(0, altura_cilindro)

    ax.view_init(elev=20, azim=30)
    plt.show()
