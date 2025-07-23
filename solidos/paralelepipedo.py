import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D

def paralelepipedo(largura, profundidade, altura):

    vertices = np.array([
        [0,       0,           0],
        [largura, 0,           0],
        [0,       profundidade, 0],
        [largura, profundidade, 0],
        [0,       0,           altura],
        [largura, 0,           altura],
        [0,       profundidade, altura],
        [largura, profundidade, altura]
    ])

    quads = [
        (0, 1, 3, 2),
        (4, 5, 7, 6),
        (0, 1, 5, 4),
        (2, 3, 7, 6),
        (0, 2, 6, 4),
        (1, 3, 7, 5)
    ]

    faces = []
    for v0, v1, v2, v3 in quads:
        faces.append([v0, v1, v2])
        faces.append([v0, v2, v3])

    arestas = [
        (0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3),
        (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)
    ]

    return vertices, arestas, faces


if __name__ == '__main__':
    largura_caixa = 8.0
    profundidade_caixa = 5.0
    altura_caixa = 3.0

    vertices_caixa, arestas_caixa, faces_caixa = paralelepipedo(
        largura_caixa, profundidade_caixa, altura_caixa
    )

    fig = plt.figure(figsize=(10, 8))
    ax: Axes3D = fig.add_subplot(projection='3d')

    poly3d = [vertices_caixa[list(face)] for face in faces_caixa]

    ax.add_collection3d(Poly3DCollection(
        poly3d,
        facecolors='tomato',
        linewidths=1,
        edgecolors='black',
        alpha=1.0
    ))

    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')
    ax.set_title('Modelo de Paralelepípedo')

    ax.set_box_aspect([largura_caixa, profundidade_caixa, altura_caixa])
    ax.set_xlim(0, largura_caixa + 2)
    ax.set_ylim(0, profundidade_caixa)
    ax.set_zlim(0, altura_caixa + 2)

    ax.view_init(elev=30, azim=-60)
    plt.show()
