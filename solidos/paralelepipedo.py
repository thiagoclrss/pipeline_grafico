import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D

def paralelepipedo(largura, profundidade, altura):
    """
    Modela um paralelepípedo sólido com um canto na origem, usando faces triangulares.
    Convenção Z-Up: A altura está no eixo Z e a base no plano XY.
    """
    # --- 1. Definição dos 8 Vértices (LÓGICA Z-UP) ---
    # A 'altura' agora afeta a coordenada Z.
    # A 'profundidade' agora afeta a coordenada Y.
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
        [0,       0,           0],      # Vértice 0: Base-Frente-Esquerda
        [largura, 0,           0],      # Vértice 1: Base-Frente-Direita
        [0,       profundidade, 0],      # Vértice 2: Base-Trás-Esquerda
        [largura, profundidade, 0],      # Vértice 3: Base-Trás-Direita
        [0,       0,           altura], # Vértice 4: Topo-Frente-Esquerda
        [largura, 0,           altura], # Vértice 5: Topo-Frente-Direita
        [0,       profundidade, altura], # Vértice 6: Topo-Trás-Esquerda
        [largura, profundidade, altura]  # Vértice 7: Topo-Trás-Direita
    ])

    # --- 2. Geração das Faces a partir de Quadriláteros ---
    # A lógica de conexão dos vértices não muda.
    quads = [
        (0, 1, 3, 2), # Face de Baixo
        (4, 5, 7, 6), # Face de Cima
        (0, 1, 5, 4), # Face da Frente
        (2, 3, 7, 6), # Face de Trás
        (0, 2, 6, 4), # Face da Esquerda
        (1, 3, 7, 5)  # Face da Direita
    ]

    faces = []
    for v0, v1, v2, v3 in quads:
        faces.append([v0, v1, v2])
        faces.append([v0, v2, v3])

    # --- 3. Geração das 12 Arestas ---
    # A lógica de conexão também não muda.
    arestas = [
        (0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3),
        (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)
    ]

    return vertices, arestas, faces

# --- Bloco de Execução Principal e Visualização (Z-UP) ---
if __name__ == '__main__':
    # Parâmetros do paralelepípedo
    largura_caixa = 8.0
    profundidade_caixa = 5.0
    altura_caixa = 3.0

    # Gerar a geometria do sólido
    vertices_caixa, arestas_caixa, faces_caixa = paralelepipedo(
        largura_caixa, profundidade_caixa, altura_caixa
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

    # --- MUDANÇAS PARA VISUALIZAÇÃO Z-UP ---

    # Configurações do gráfico
    ax.set_xlabel('Eixo X (Largura)')
    ax.set_ylabel('Eixo Y (Profundidade)')
    ax.set_zlabel('Eixo Z (Altura)')
    ax.set_title('Modelo de Paralelepípedo com Malha Triangular (Z-Up)')

    # Ajustar os limites e a proporção para uma visualização correta
    ax.set_box_aspect([largura_caixa, profundidade_caixa, altura_caixa])
    ax.set_xlim(0, largura_caixa)
    ax.set_ylim(0, profundidade_caixa)
    ax.set_zlim(0, altura_caixa)

    # Um bom ângulo de câmera para visualização Z-Up
    ax.view_init(elev=30, azim=-60)
    plt.show()
