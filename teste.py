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
    # Garante que os vértices sejam um array 2D antes de adicionar a coordenada homogênea
    vertices_2d = np.atleast_2d(vertices)
    vertices_homogeneos = np.hstack((vertices_2d, np.ones((vertices_2d.shape[0], 1))))
    vertices_transformados = (matriz @ vertices_homogeneos.T).T
    return vertices_transformados[:, :3]

# --- NOVA FUNÇÃO: Matriz de Visualização (Câmera) ---
def matriz_visualizacao(eye, at, up):
    """
    Calcula a Matriz de Visualização (View Matrix) usando o algoritmo Look-At.
    """
    # Passo 1: Calcular a base vetorial do novo sistema (eixos da câmera)
    # Eixo Z da câmera (aponta do alvo para a câmera)
    z_cam = eye - at
    z_cam = z_cam / np.linalg.norm(z_cam)

    # Eixo X da câmera (perpendicular ao Z da câmera e ao 'up' do mundo)
    x_cam = np.cross(up, z_cam)
    x_cam = x_cam / np.linalg.norm(x_cam)

    # Eixo Y da câmera (perpendicular aos eixos X e Z da câmera)
    y_cam = np.cross(z_cam, x_cam)

    # Passo 2: Construir a matriz de transformação
    # A matriz é composta por uma rotação e uma translação
    # A rotação alinha os eixos do mundo com os da câmera
    rotacao = np.array([
        [x_cam[0], x_cam[1], x_cam[2], 0],
        [y_cam[0], y_cam[1], y_cam[2], 0],
        [z_cam[0], z_cam[1], z_cam[2], 0],
        [0, 0, 0, 1]
    ])

    # A translação move o mundo para que a posição 'eye' da câmera fique na origem
    translacao = matriz_translacao(-eye[0], -eye[1], -eye[2])

    # A matriz de visualização final é a combinação das duas
    return rotacao @ translacao

# --- SESSÃO 3: Composição da Cena (Inalterada) ---


# --- SESSÃO 4: Bloco de Execução Principal e Visualização ---

if __name__ == '__main__':

    posicao_camera_eye = np.array([8.0, 20.0, 1.0])
    ponto_alvo_at = np.array([0.0, 12.0, 0.0])
    vetor_up_mundo = np.array([0.0, 0.0, 1.0])

    # --- Parte 1: Visualização no Sistema do Mundo (como antes) ---
    vertices_mundo, faces_mundo, cores_faces, vertices_linha_mundo, arestas_linha_mundo = compor_cena()

    fig_mundo = plt.figure(figsize=(12, 10))
    ax_mundo = fig_mundo.add_subplot(projection='3d')

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
    ax_mundo.set_xlim(-10, 10);
    ax_mundo.set_ylim(0, 20);
    ax_mundo.set_zlim(-10, 10)
    ax_mundo.view_init(elev=100, azim=270)

    plt.grid(True)

    # --- Parte 2: Transformação e Visualização no Sistema da Câmera ---

    # Passo 1: Escolha a origem e o alvo da câmera no sistema do mundo
     # Y é "para cima" no nosso mundo

    # Passo 2: Calcule a matriz de visualização
    matriz_view = matriz_visualizacao(posicao_camera_eye, ponto_alvo_at, vetor_up_mundo)

    # Passo 3: Transforme TODOS os vértices da cena para o sistema da câmera
    vertices_camera = aplicar_transformacao(vertices_mundo, matriz_view)
    vertices_linha_camera = aplicar_transformacao(vertices_linha_mundo, matriz_view)

    # Passo Extra: Transforme a origem do mundo (0,0,0) para saber onde ela aparece na visão da câmera
    origem_mundo_transformada = aplicar_transformacao(np.array([0.0, 0.0, 0.0]), matriz_view)
    # Onde a camera olha
    ponto_alvo_at_camera =  aplicar_transformacao(ponto_alvo_at, matriz_view)

    # Passo 4: Mostre os sólidos no novo sistema de coordenadas
    fig_camera = plt.figure(figsize=(12, 10))
    ax_camera : Axes3D = fig_camera.add_subplot(projection='3d')

    poly3d_camera = [vertices_camera[list(face)] for face in faces_mundo]
    colecao_camera = Poly3DCollection(poly3d_camera, alpha=1.0)
    colecao_camera.set_facecolor(cores_faces)
    ax_camera.add_collection3d(colecao_camera)

    for aresta in arestas_linha_mundo:
        p_inicio, p_fim = vertices_linha_camera[aresta[0]], vertices_linha_camera[aresta[1]]
        ax_camera.plot([p_inicio[0], p_fim[0]], [p_inicio[1], p_fim[1]], [p_inicio[2], p_fim[2]], color='red', linewidth=3)

    # Adicionar marcadores para a origem da câmera e a antiga origem do mundo
    ax_camera.scatter(0, 0, 0, color='magenta', s=150, label='Origem da Câmera (Eye)', depthshade=False)
    ax_camera.scatter(origem_mundo_transformada[0,0], origem_mundo_transformada[0,1], origem_mundo_transformada[0,2],
                      color='black', s=150, marker='X', label='Origem do Mundo (0,0,0)', depthshade=False)
    ax_camera.scatter(ponto_alvo_at_camera[0,0], ponto_alvo_at_camera[0,1], ponto_alvo_at_camera[0,2],
                    color='purple', s=150, marker='*', label='Ponto at', depthshade=False)

    ax_camera.set_title('Cena no Sistema de Coordenadas da Câmera')
    ax_camera.set_xlabel('X Câmera'); ax_camera.set_ylabel('Y Câmera'); ax_camera.set_zlabel('Z Câmera')
    ax_camera.legend()
    #ax_camera.set_xlim(-10, 10);
    #ax_camera.set_ylim(0,-20);
    #ax_camera.set_zlim(-10, 10)
    #ax_mundo.view_init(elev=100, azim=270)

    #ax_camera.view_init(elev=100, azim=270)
    plt.grid(True)

    # Mostra as duas figuras
    plt.show()
