import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def linha_reta(comprimento):

    vertices = np.array([
        [0, 0, 0],
        [comprimento, 0, 0]
    ])

    arestas = [
        (0, 1)
    ]

    faces = []

    return vertices, arestas, faces


if __name__ == '__main__':
    tamanho_linha = 4
    vertices_linha, arestas_linha, faces_linha = linha_reta(tamanho_linha)

    fig = plt.figure(figsize=(10, 8))
    ax: Axes3D = fig.add_subplot(projection='3d')

    ax.scatter(vertices_linha[:, 0], vertices_linha[:, 1], vertices_linha[:, 2], color='red', s=100, label='Vértices')

    for aresta in arestas_linha:
        ponto_inicio = vertices_linha[aresta[0]]
        ponto_fim = vertices_linha[aresta[1]]
        xs = [ponto_inicio[0], ponto_fim[0]]
        ys = [ponto_inicio[1], ponto_fim[1]]
        zs = [ponto_inicio[2], ponto_fim[2]]
        ax.plot(xs, ys, zs, color='blue', linewidth=3, label='Aresta' if aresta == arestas_linha[0] else "")

    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')
    ax.set_title('Modelo de Linha Reta')
    ax.legend()

    ax.set_xlim([-1, tamanho_linha + 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_box_aspect((tamanho_linha + 2, 2, 2))

    ax.view_init(elev=20, azim=30)
    plt.show()
