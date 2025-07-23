import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D

def cano_reto(raio, comprimento, espessura, num_divisoes=20):

    if espessura >= raio:
        raise ValueError("A espessura deve ser menor que o raio.")

    vertices = []
    faces = []
    arestas = []

    raio_interno = raio - espessura
    angulos = np.linspace(0, 2 * np.pi, num_divisoes, endpoint=False)

    for angulo in angulos:
        x_ext = raio * np.cos(angulo)
        y_ext = raio * np.sin(angulo)
        vertices.append([x_ext, y_ext, 0])
        vertices.append([x_ext, y_ext, comprimento])

    for angulo in angulos:
        x_int = raio_interno * np.cos(angulo)
        y_int = raio_interno * np.sin(angulo)
        vertices.append([x_int, y_int, 0])
        vertices.append([x_int, y_int, comprimento])

    vertices = np.array(vertices)

    num_vertices_externos = num_divisoes * 2

    for i in range(num_divisoes):
        j = (i + 1) % num_divisoes

        idx_ext_inicio_i = i * 2
        idx_ext_fim_i = i * 2 + 1
        idx_ext_inicio_j = j * 2
        idx_ext_fim_j = j * 2 + 1

        idx_int_inicio_i = num_vertices_externos + i * 2
        idx_int_fim_i = num_vertices_externos + i * 2 + 1
        idx_int_inicio_j = num_vertices_externos + j * 2
        idx_int_fim_j = num_vertices_externos + j * 2 + 1

        faces.append((idx_ext_inicio_i, idx_ext_fim_j, idx_ext_fim_i))
        faces.append((idx_ext_inicio_i, idx_ext_inicio_j, idx_ext_fim_j))

        faces.append((idx_int_inicio_i, idx_int_fim_i, idx_int_fim_j))
        faces.append((idx_int_inicio_i, idx_int_fim_j, idx_int_inicio_j))

        faces.append((idx_ext_inicio_i, idx_int_inicio_j, idx_int_inicio_i))
        faces.append((idx_ext_inicio_i, idx_ext_inicio_j, idx_int_inicio_j))

        faces.append((idx_ext_fim_i, idx_int_fim_i, idx_int_fim_j))
        faces.append((idx_ext_fim_i, idx_int_fim_j, idx_ext_fim_j))

        arestas.append((idx_ext_inicio_i, idx_ext_inicio_j))
        arestas.append((idx_ext_fim_i, idx_ext_fim_j))
        arestas.append((idx_int_inicio_i, idx_int_inicio_j))
        arestas.append((idx_int_fim_i, idx_int_fim_j))
        arestas.append((idx_ext_inicio_i, idx_ext_fim_i))
        arestas.append((idx_int_inicio_i, idx_int_fim_i))

    return vertices, arestas, faces

if __name__ == '__main__':

    raio_cano = 2.5
    comprimento_cano = 8.0
    espessura_cano = 0.5

    vertices_cano, arestas_cano, faces_cano = cano_reto(
        raio_cano, comprimento_cano, espessura_cano, num_divisoes=24
    )

    fig = plt.figure(figsize=(10, 8))
    ax: Axes3D = fig.add_subplot(projection='3d')

    poly3d = [vertices_cano[list(face)] for face in faces_cano]

    ax.add_collection3d(Poly3DCollection(
        poly3d,
        facecolors='lightgreen',
        linewidths=0.5,
        edgecolors='darkgreen',
        alpha=1.0
    ))

    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')
    ax.set_title('Modelo de Cano Reto')

    ax.set_xlim([-raio_cano*1.5, raio_cano*1.5])
    ax.set_ylim([-raio_cano*1.5, raio_cano*1.5])
    ax.set_zlim([-1, comprimento_cano + 1])
    ax.view_init(elev=25, azim=45)

    plt.show()
