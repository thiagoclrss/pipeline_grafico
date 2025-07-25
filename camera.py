import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D
from solidos.paralelepipedo import paralelepipedo
from solidos.cilindro import cilindro
from solidos.cano_reto import cano_reto
from solidos.cano_curvo import cano_curvado, curva_hermite
from solidos.reta import linha_reta
from mundo import compor_cena
from matrizes_transformacao import matriz_translacao, aplicar_transformacao

def matriz_visualizacao(eye, at, up):

    z_cam = eye - at
    z_cam = z_cam / np.linalg.norm(z_cam)

    x_cam = np.cross(up, z_cam)
    x_cam = x_cam / np.linalg.norm(x_cam)

    y_cam = np.cross(z_cam, x_cam)


    rotacao = np.array([
        [x_cam[0], x_cam[1], x_cam[2], 0],
        [y_cam[0], y_cam[1], y_cam[2], 0],
        [z_cam[0], z_cam[1], z_cam[2], 0],
        [0, 0, 0, 1]
    ])

    translacao = matriz_translacao(-eye[0], -eye[1], -eye[2])

    return rotacao @ translacao

if __name__ == '__main__':

    vertices_mundo, faces_mundo, cores_faces, vertices_linha_mundo, arestas_linha_mundo = compor_cena()

    posicao_camera_eye = np.array([15.0, 13.0, 12.0])
    ponto_alvo_at = np.array([0.0, 2.0, 10.0])
    vetor_up_mundo = np.array([0.0, 1.0, 0.0])

    fig_mundo = plt.figure(figsize=(12, 10))
    ax_mundo: Axes3D = fig_mundo.add_subplot(projection='3d')

    poly3d_mundo = [vertices_mundo[list(face)] for face in faces_mundo]
    colecao_mundo = Poly3DCollection(poly3d_mundo, alpha=1.0)
    colecao_mundo.set_facecolor(cores_faces)
    ax_mundo.add_collection3d(colecao_mundo)


    for aresta in arestas_linha_mundo:
        p_inicio, p_fim = vertices_linha_mundo[aresta[0]], vertices_linha_mundo[aresta[1]]
        ax_mundo.plot([p_inicio[0], p_fim[0]], [p_inicio[1], p_fim[1]], [p_inicio[2], p_fim[2]], color='red', linewidth=3)

    ax_mundo.scatter(posicao_camera_eye[0], posicao_camera_eye[1], posicao_camera_eye[2], color='magenta', s=150, label=f"Origem da Câmera Eye: ({posicao_camera_eye[0]:.1f}, {posicao_camera_eye[1]:.1f}, {posicao_camera_eye[2]:.1f})", depthshade=False)
    ax_mundo.scatter(0,0,0, color='black', s=150, marker='X', label='Origem do Mundo: (0,0,0)', depthshade=False)
    ax_mundo.scatter(ponto_alvo_at[0], ponto_alvo_at[1], ponto_alvo_at[2],
                    color='purple', s=150, marker='*', label=f"Ponto at: ({ponto_alvo_at[0]:.1f}, {ponto_alvo_at[1]:.1f}, {ponto_alvo_at[2]:.1f})", depthshade=False)

    ax_mundo.set_title('Cena no Sistema de Coordenadas do Mundo')
    ax_mundo.set_xlabel('X Mundo'); ax_mundo.set_ylabel('Y Mundo'); ax_mundo.set_zlabel('Z Mundo')
    ax_mundo.view_init(elev=30, azim=-75)
    ax_mundo.legend()
    plt.grid(True)

    matriz_view = matriz_visualizacao(posicao_camera_eye, ponto_alvo_at, vetor_up_mundo)

    vertices_camera = aplicar_transformacao(vertices_mundo, matriz_view)
    vertices_linha_camera = aplicar_transformacao(vertices_linha_mundo, matriz_view)
    origem_mundo_transformada = aplicar_transformacao(np.array([0.0, 0.0, 0.0]), matriz_view)
    ponto_alvo_at_camera = aplicar_transformacao(ponto_alvo_at, matriz_view)

    fig_camera = plt.figure(figsize=(12, 10))
    ax_camera: Axes3D = fig_camera.add_subplot(projection='3d')

    poly3d_camera = [vertices_camera[list(face)] for face in faces_mundo]
    colecao_camera = Poly3DCollection(poly3d_camera, alpha=1.0)
    colecao_camera.set_facecolor(cores_faces)
    ax_camera.add_collection3d(colecao_camera)

    for aresta in arestas_linha_mundo:
        p_inicio, p_fim = vertices_linha_camera[aresta[0]], vertices_linha_camera[aresta[1]]
        ax_camera.plot([p_inicio[0], p_fim[0]], [p_inicio[1], p_fim[1]], [p_inicio[2], p_fim[2]], color='red', linewidth=3)

    ax_camera.scatter(0, 0, 0, color='magenta', s=150, label='Origem da Câmera Eye: (0,0,0)', depthshade=False)
    ax_camera.scatter(origem_mundo_transformada[0,0], origem_mundo_transformada[0,1], origem_mundo_transformada[0,2],
                        color='black', s=150, marker='X', label=f"Origem do mundo: ({origem_mundo_transformada[0,1]:.1f}, {origem_mundo_transformada[0,1]:.1f}, {origem_mundo_transformada[0,2]:.1f})", depthshade=False)
    ax_camera.scatter(ponto_alvo_at_camera[0,0], ponto_alvo_at_camera[0,1], ponto_alvo_at_camera[0,2],
                    color='purple', s=150, marker='*', label=f"Ponto at: ({ponto_alvo_at_camera[0,1]:.1f}, {ponto_alvo_at_camera[0,1]:.1f}, {ponto_alvo_at_camera[0,2]:.1f})", depthshade=False)

    ax_camera.set_title('Cena no Sistema de Coordenadas da Câmera')
    ax_camera.set_xlabel('X Câmera'); ax_camera.set_ylabel('Y Câmera'); ax_camera.set_zlabel('Z Câmera')
    ax_camera.view_init(elev=30, azim=-70)
    ax_camera.legend()
    plt.grid(True)

    plt.show()
