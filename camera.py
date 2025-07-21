import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import solidos
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D

from mundo import matriz_translacao, aplicar_transformacao, compor_cena

def matriz_visao(posicao_camera, ponto_alvo, vetor_up_mundo):
    """
    Calcula a Matriz de Visualização (View Matrix) 4x4 para transformar
    coordenadas do mundo para as coordenadas da câmera.

    Args:
        posicao_camera (np.array): Posição da câmera no mundo.
        ponto_alvo (np.array): Ponto para o qual a câmera está olhando.
        vetor_up_mundo (np.array): Vetor que indica a direção "para cima" no mundo (ex: [0,0,1]).

    Returns:
        np.array: A matriz de visualização 4x4.
    """
    # Passo 1: Calcular a base de vetores do sistema de coordenadas da câmera (u, v, n)
    # O eixo n (eixo Z da câmera) aponta do alvo para a câmera.
    n = posicao_camera - ponto_alvo
    n = n / np.linalg.norm(n)

    # O eixo u (eixo X da câmera) é perpendicular a 'n' e ao vetor 'up' do mundo.
    u = np.cross(vetor_up_mundo, n)
    u = u / np.linalg.norm(u)

    # O eixo v (eixo Y da câmera) é o verdadeiro "up" da câmera, perpendicular a 'n' e 'u'.
    v = np.cross(n, u)

    # Passo 2: Construir a matriz de rotação que alinha os eixos do mundo com (u,v,n)
    # Esta é a transposta da matriz formada pelos vetores da base.
    mat_rot = np.array([
        [u[0], u[1], u[2], 0],
        [v[0], v[1], v[2], 0],
        [n[0], n[1], n[2], 0],
        [0,    0,    0,    1]
    ])

    # Passo 3: Construir a matriz de translação que move a câmera para a origem
    mat_trans = matriz_translacao(-posicao_camera[0], -posicao_camera[1], -posicao_camera[2])

    # A Matriz de Visão final é a combinação da translação e da rotação
    return mat_rot @ mat_trans

if __name__ == '__main__':

    vertices_cena, faces_cena, cores_faces, vertices_linha, arestas_linha = compor_cena()
    fig = plt.figure(figsize=(15, 12))
    ax: Axes3D = fig.add_subplot(projection='3d')

    # Transformação para o Sistema de Coordenadas da Câmera ---

    # Definir os parâmetros da câmera
    posicao_camera = np.array([8, 3, 5])
    ponto_alvo = np.array([0, 0, 0])
    vetor_up_mundo = np.array([0, 0, 1])

    # Calcular a Matriz de Visualização
    mat_view = matriz_visao(posicao_camera, ponto_alvo, vetor_up_mundo)

    # 3. Transformar TODOS os vértices da cena (sólidos e linhas) para o SCC
    vertices_cena_scc = aplicar_transformacao(vertices_cena, mat_view)
    vertices_linha_scc = aplicar_transformacao(vertices_linha, mat_view)

    # Renderizar os sólidos com faces, usando os vértices transformados
    poly3d = [vertices_cena_scc[list(face)] for face in faces_cena]
    colecao_poligonos = Poly3DCollection(poly3d, alpha=1.0)
    colecao_poligonos.set_facecolor(cores_faces)
    ax.add_collection3d(colecao_poligonos)

    # Renderizar as arestas da linha reta, usando os vértices transformados
    for aresta in arestas_linha:
        p_inicio, p_fim = vertices_linha_scc[aresta[0]], vertices_linha_scc[aresta[1]]
        ax.plot([p_inicio[0], p_fim[0]], [p_inicio[1], p_fim[1]], [p_inicio[2], p_fim[2]], color='red', linewidth=3)

    origem_mundo = np.array([[0, 0, 0]])
    # 2. Transformar a origem para o Sistema de Coordenadas da Câmera
    origem_scc = aplicar_transformacao(origem_mundo, mat_view)
    # 3. Plotar o ponto transformado com um marcador distinto (uma esfera roxa)
    ax.scatter(origem_scc[0, 0], origem_scc[0, 1], origem_scc[0, 2],
               color='purple', s=150, label='Origem do Mundo (0,0,0)', depthshade=True)
    # Adicionar uma legenda para identificar o ponto
    ax.legend()

    # Definimos os rótulos dos eixos para refletir o SCC
    ax.set_xlabel('Eixo U (Câmera)')
    ax.set_ylabel('Eixo V (Câmera)')
    ax.set_zlabel('Eixo N (Câmera)')
    ax.set_title('Cena 3D no Sistema de Coordendas da Câmera')

    ax.set_xlim(-20, 10)
    ax.set_ylim(-20, 10)
    ax.set_zlim(-20, 10)

    # ax.view_init(elev=30, azim=-75)
    ax.set_aspect('equal', adjustable='box')
    plt.grid(True)
    plt.show()