import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import solidos
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D

from camera import matriz_visualizacao, aplicar_transformacao
from mundo import compor_cena

def matriz_projecao_perspectiva(fov_graus, aspect_ratio, near, far):
    """Cria a matriz de projeção em perspectiva."""
    fov_rad = np.radians(fov_graus)
    f = 1.0 / np.tan(fov_rad / 2.0)
    return np.array([
        [f / aspect_ratio, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
        [0, 0, -1, 0]
    ])

from matplotlib.patches import Polygon

def plotar_cena_2d(vertices_cena, faces_cena, cores_faces, vertices_linha, arestas_linha,
                   camera_pos, ponto_alvo, up_mundo):
    """
    Executa o pipeline de projeção e renderiza a cena em um gráfico 2D.
    """
    # --- 1. Definir Parâmetros e Matrizes de Transformação ---
    near_plane = 1.0
    far_plane = 50.0
    fov = 60.0

    mat_view = matriz_visualizacao(camera_pos, ponto_alvo, up_mundo)
    mat_persp = matriz_projecao_perspectiva(fov, 1.0, near_plane, far_plane)
    mat_transform = mat_persp @ mat_view

    # --- 2. Preparar Polígonos para o Algoritmo do Pintor ---
    render_list = []

    # Transforma os vértices para o espaço da câmera para obter a profundidade
    vertices_cena_scc = aplicar_transformacao(vertices_cena, mat_view)

    for i, face in enumerate(faces_cena):
        profundidade = np.mean(vertices_cena_scc[list(face), 2])
        # Clipping simples de profundidade
        if profundidade < -near_plane and profundidade > -far_plane:
            render_list.append({
                'vertices_mundo': vertices_cena[list(face)],
                'cor': cores_faces[i],
                'profundidade': profundidade
            })

    # Ordenar polígonos do mais distante para o mais próximo
    render_list.sort(key=lambda item: item['profundidade'])

    # --- 3. Configurar o Gráfico 2D ---
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_title("Cena Projetada em 2D")
    ax.set_xlabel("Eixo X (CN)")
    ax.set_ylabel("Eixo Y (CN)")
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True)

    # --- 4. Renderizar os Polígonos Ordenados ---
    for item in render_list:
        # Transformar os vértices do mundo para Coordenadas Normalizadas
        v_mundo = item['vertices_mundo']
        v_homogeneos = np.hstack((v_mundo, np.ones((v_mundo.shape[0], 1))))
        v_clip = (mat_transform @ v_homogeneos.T).T

        # Divisão por Perspectiva
        v_cn = v_clip[:, :2] / v_clip[:, 3, np.newaxis]

        # Desenhar o polígono 2D
        polygon = Polygon(v_cn, closed=True, facecolor=item['cor'], edgecolor='black')
        ax.add_patch(polygon)

    # --- 5. Renderizar a Linha (sobre os polígonos) ---
    v_homogeneos_linha = np.hstack((vertices_linha, np.ones((vertices_linha.shape[0], 1))))
    v_clip_linha = (mat_transform @ v_homogeneos_linha.T).T

    # Checar se a linha está dentro do frustum antes de dividir
    if np.all(v_clip_linha[:, 3] > 0):
        v_cn_linha = v_clip_linha[:, :2] / v_clip_linha[:, 3, np.newaxis]
        for aresta in arestas_linha:
            p_inicio, p_fim = v_cn_linha[aresta[0]], v_cn_linha[aresta[1]]
            ax.plot([p_inicio[0], p_fim[0]], [p_inicio[1], p_fim[1]], color='red', linewidth=3)

    plt.show()


if __name__ == '__main__':

    vertices_cena, faces_cena, cores_faces, vertices_linha, arestas_linha = compor_cena()

    posicao_camera = np.array([15, 13, 12])
    ponto_alvo = np.array([0, 0, 0])
    vetor_up_mundo = np.array([0, 0, 1])

    plotar_cena_2d(vertices_cena, faces_cena, cores_faces, vertices_linha, arestas_linha,
                   posicao_camera, ponto_alvo, vetor_up_mundo)
