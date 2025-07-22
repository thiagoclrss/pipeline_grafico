import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D

# --- SESSÃO 1: Importando os Sólidos dos Módulos ---
from solidos.paralelepipedo import paralelepipedo
from solidos.cilindro import cilindro
from solidos.cano_reto import cano_reto
from solidos.cano_curvo import cano_curvado, curva_hermite
from solidos.reta import linha_reta
from mundo import compor_cena

# --- SESSÃO 2: Funções de Transformação ---

def matriz_escala(sx, sy, sz):
    return np.array([[sx,0,0,0],[0,sy,0,0],[0,0,sz,0],[0,0,0,1]])

def matriz_rotacao_y(angulo):
    rad = np.radians(angulo)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c,0,s,0],[0,1,0,0],[-s,0,c,0],[0,0,0,1]])

def matriz_rotacao_z(angulo):
    rad = np.radians(angulo)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([[c,-s,0,0],[s,c,0,0],[0,0,1,0],[0,0,0,1]])

def matriz_translacao(tx, ty, tz):
    return np.array([[1,0,0,tx],[0,1,0,ty],[0,0,1,tz],[0,0,0,1]])

def aplicar_transformacao(vertices, matriz):
    vertices_2d = np.atleast_2d(vertices)
    vertices_homogeneos = np.hstack((vertices_2d, np.ones((vertices_2d.shape[0], 1))))
    vertices_transformados = (matriz @ vertices_homogeneos.T).T
    return vertices_transformados[:, :3]

# --- FUNÇÃO 'matriz_visualizacao' CORRIGIDA ---
def matriz_visualizacao(eye, at, up):
    """
    Calcula a Matriz de Visualização (View Matrix) de forma robusta e matematicamente correta.
    """
    # Eixo Z da Câmera (aponta para a frente, do olho para o alvo)
    forward = at - eye
    if np.linalg.norm(forward) < 1e-6: # Evita divisão por zero se eye e at forem iguais
        return np.eye(4)
    forward = forward / np.linalg.norm(forward)

    # Eixo X da Câmera (vetor "direita")
    right = np.cross(up, -forward) # Usamos -forward para o produto vetorial
    if np.linalg.norm(right) < 1e-6: # Evita gimbal lock
        right = np.array([1., 0., 0.])
    right = right / np.linalg.norm(right)

    # Eixo Y da Câmera (vetor "para cima" da câmera)
    camera_up = np.cross(-forward, right)

    # A matriz de visualização é a inversa da matriz de transformação da câmera.
    # Montamos a matriz de rotação inversa (cujos eixos são as linhas)
    # e a matriz de translação inversa.

    rot_inv = np.array([
        [right[0], right[1], right[2]],
        [camera_up[0], camera_up[1], camera_up[2]],
        [-forward[0], -forward[1], -forward[2]]
    ])

    trans_inv = -rot_inv @ eye

    # Combina em uma matriz 4x4 final
    matriz_view = np.eye(4)
    matriz_view[:3, :3] = rot_inv
    matriz_view[:3, 3] = trans_inv

    return matriz_view

# --- SESSÃO 3 e 4 (permanecem inalteradas) ---

if __name__ == '__main__':
    # --- Parte 1: Visualização no Sistema do Mundo (como antes) ---
    vertices_mundo, faces_mundo, cores_faces, vertices_linha_mundo, arestas_linha_mundo = compor_cena()

    posicao_camera_eye = np.array([10.0, 8.0, 15.0])
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

    ax_mundo.scatter(posicao_camera_eye[0], posicao_camera_eye[1], posicao_camera_eye[2], color='magenta', s=150, label='Origem da Câmera (Eye)', depthshade=False)
    ax_mundo.scatter(0,0,0, color='black', s=150, marker='X', label='Origem do Mundo (0,0,0)', depthshade=False)
    ax_mundo.scatter(ponto_alvo_at[0], ponto_alvo_at[1], ponto_alvo_at[2],
                    color='purple', s=150, marker='*', label='Ponto at', depthshade=False)

    ax_mundo.set_title('Cena no Sistema de Coordenadas do Mundo')
    ax_mundo.set_xlabel('X Mundo'); ax_mundo.set_ylabel('Y Mundo'); ax_mundo.set_zlabel('Z Mundo')
    ax_mundo.set_xlim(-10, 10); ax_mundo.set_ylim(-10, 10); ax_mundo.set_zlim(-10, 10)
    ax_mundo.view_init(elev=30, azim=-75)
    plt.grid(True)

    # --- Parte 2: Transformação e Visualização no Sistema da Câmera ---
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

    ax_camera.scatter(0, 0, 0, color='magenta', s=150, label='Origem da Câmera (Eye)', depthshade=False)
    ax_camera.scatter(origem_mundo_transformada[0,0], origem_mundo_transformada[0,1], origem_mundo_transformada[0,2],
                        color='black', s=150, marker='X', label='Origem do Mundo (0,0,0)', depthshade=False)
    ax_camera.scatter(ponto_alvo_at_camera[0,0], ponto_alvo_at_camera[0,1], ponto_alvo_at_camera[0,2],
                    color='purple', s=150, marker='*', label='Ponto at', depthshade=False)

    ax_camera.set_title('Cena no Sistema de Coordenadas da Câmera')
    ax_camera.set_xlabel('X Câmera'); ax_camera.set_ylabel('Y Câmera'); ax_camera.set_zlabel('Z Câmera')
    ax_camera.set_xlim(-10, 10); ax_camera.set_ylim(-10, 10); ax_camera.set_zlim(-20, 0)
    ax_camera.view_init(elev=30, azim=-75)
    ax_camera.legend()
    plt.grid(True)

    plt.show()
