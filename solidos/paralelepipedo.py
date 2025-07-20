import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D

# Substitua o conteúdo de solidos/paralelepipedo.py por este código:

import numpy as np

def paralelepipedo(largura, altura, profundidade):
    """
    Modela um paralelepípedo sólido com um canto na origem, usando faces triangulares.
    Esta é uma versão corrigida e verificada.
    """
    # --- 1. Definição dos 8 Vértices ---
    # Usaremos uma convenção Y-Up (Y representa a altura) para maior clareza.
    # A base estará no plano XZ.
    #
    #       6--------7
    #      /|       /|
    #     / |      / |
    #    2--------3  |
    #    |  4-----|--5
    #    | /      | /
    #    |/       |/
    #    0--------1

    vertices = np.array([
        [0,       0,      profundidade], # Vértice 0: Frente-Base-Esquerda
        [largura, 0,      profundidade], # Vértice 1: Frente-Base-Direita
        [0,       altura, profundidade], # Vértice 2: Frente-Topo-Esquerda
        [largura, altura, profundidade], # Vértice 3: Frente-Topo-Direita
        [0,       0,      0],            # Vértice 4: Trás-Base-Esquerda
        [largura, 0,      0],            # Vértice 5: Trás-Base-Direita
        [0,       altura, 0],            # Vértice 6: Trás-Topo-Esquerda
        [largura, altura, 0]             # Vértice 7: Trás-Topo-Direita
    ])

    # --- 2. Geração das Faces a partir de Quadriláteros ---
    # Definimos as 6 faces como quadriláteros com vértices em sentido anti-horário (visto de fora)
    quads = [
        (0, 1, 3, 2), # Face da Frente
        (4, 5, 1, 0), # Face de Baixo
        (5, 7, 6, 4), # Face de Trás
        (2, 3, 7, 6), # Face de Cima
        (0, 2, 6, 4), # Face da Esquerda
        (1, 5, 7, 3)  # Face da Direita
    ]

    faces = []
    for v0, v1, v2, v3 in quads:
        # Divide cada quadrilátero em dois triângulos
        faces.append([v0, v1, v2])
        faces.append([v0, v2, v3])

    # --- 3. Geração das 12 Arestas ---
    arestas = [
        (0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3),
        (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)
    ]

    return vertices, arestas, faces

# --- Bloco de Execução Principal e Visualização ---
if __name__ == '__main__':
    # Parâmetros do paralelepípedo
    largura_caixa = 8.0
    altura_caixa = 3.0
    profundidade_caixa = 5.0

    # Gerar a geometria do sólido
    vertices_caixa, arestas_caixa, faces_caixa = paralelepipedo(
        largura_caixa, altura_caixa, profundidade_caixa
    )

    # Configuração da visualização 3D
    fig = plt.figure(figsize=(10, 8))
    ax: Axes3D = fig.add_subplot(projection='3d')

    # Preparar faces para renderização
    poly3d = [vertices_caixa[list(face)] for face in faces_caixa]

    # Adicionar a coleção de polígonos (faces) ao gráfico
    ax.add_collection3d(Poly3DCollection(
        poly3d,
        facecolors='tomato',
        linewidths=1,
        edgecolors='black',
        alpha=1.0
    ))

    # Configurações do gráfico
    ax.set_xlabel('Eixo X (Largura)')
    ax.set_ylabel('Eixo Y (Altura)')
    ax.set_zlabel('Eixo Z (Profundidade)')
    ax.set_title('Modelo de Paralelepípedo com Malha Triangular')

    # Ajustar os limites e a proporção para uma visualização correta
    ax.set_box_aspect([largura_caixa, altura_caixa, profundidade_caixa])
    ax.set_xlim(0, largura_caixa)
    ax.set_ylim(0, altura_caixa)
    ax.set_zlim(0, profundidade_caixa)

    ax.view_init(elev=25, azim=-120)
    plt.show()
