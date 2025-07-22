import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def linha_reta(comprimento):
    """
    Modela uma linha reta ao longo do eixo X.

    Args:
        comprimento (float): O comprimento total da linha.

    Returns:
        tuple: Uma tupla contendo (vértices, arestas, faces).
               - vertices: um array NumPy de 2 pontos [x, y, z].
               - arestas: uma lista de 1 tupla conectando os dois vértices.
               - faces: uma lista vazia, pois uma linha não tem faces.
    """
    # --- 1. Definição dos 2 Vértices (início e fim) ---
    # A origem é fixa em (0, 0, 0) e a linha se estende pelo eixo X.
    vertices = np.array([
        [0, 0, 0],           # Vértice 0: Ponto de início
        [comprimento, 0, 0]  # Vértice 1: Ponto final
    ])

    # --- 2. Definição da Aresta ---
    # Apenas uma aresta que conecta o vértice 0 ao vértice 1.
    arestas = [
        (0, 1)
    ]

    # --- 3. Faces ---
    # Uma linha não tem área, portanto, não tem faces.
    faces = []

    return vertices, arestas, faces

# --- Bloco de Execução Principal e Visualização ---
if __name__ == '__main__':
    # Parâmetro da linha
    tamanho_linha = 4

    # Gerar a geometria do sólido
    vertices_linha, arestas_linha, faces_linha = linha_reta(tamanho_linha)

    # Configuração da visualização 3D
    fig = plt.figure(figsize=(10, 8))
    ax: Axes3D = fig.add_subplot(projection='3d')

    # --- Lógica de Visualização para Arestas e Vértices ---

    # Desenhar os vértices como pontos vermelhos
    ax.scatter(vertices_linha[:, 0], vertices_linha[:, 1], vertices_linha[:, 2], color='red', s=100, label='Vértices')

    # Desenhar as arestas como linhas azuis
    for aresta in arestas_linha:
        # Pega os pontos de início e fim da aresta
        ponto_inicio = vertices_linha[aresta[0]]
        ponto_fim = vertices_linha[aresta[1]]
        # ax.plot precisa de listas separadas para coordenadas x, y, e z
        xs = [ponto_inicio[0], ponto_fim[0]]
        ys = [ponto_inicio[1], ponto_fim[1]]
        zs = [ponto_inicio[2], ponto_fim[2]]
        ax.plot(xs, ys, zs, color='blue', linewidth=3, label='Aresta' if aresta == arestas_linha[0] else "")

    # Configurações do gráfico
    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')
    ax.set_title('Modelo de Linha Reta')
    ax.legend()

    # Ajustar os limites para visualização adequada
    ax.set_xlim([-1, tamanho_linha + 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])

    # Forçar aspecto igual para evitar distorções
    ax.set_box_aspect((tamanho_linha + 2, 2, 2))

    ax.view_init(elev=100, azim=270)
    plt.show()
