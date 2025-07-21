import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import solidos
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D


# --- SESSÃO 1: Importando os Sólidos dos Módulos ---
# O código dos sólidos agora vive em arquivos separados dentro da pasta 'solidos'.
from solidos.paralelepipedo import paralelepipedo
from solidos.cilindro import cilindro # Supondo que a função esteja em cilindro.py
from solidos.cano_reto import cano_reto
from solidos.cano_curvo import cano_curvado, curva_hermite # Importar a função auxiliar também
from solidos.reta import linha_reta

# --- SESSÃO 2: Funções de Transformação (Podem continuar aqui ou ir para um módulo 'utils.py') ---

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
    vertices_homogeneos = np.hstack((vertices, np.ones((vertices.shape[0], 1))))
    vertices_transformados = (matriz @ vertices_homogeneos.T).T
    return vertices_transformados[:, :3]

# --- SESSÃO 3: Composição da Cena (Permanece igual) ---

def compor_cena():
    todos_vertices = []
    todas_faces = []
    todas_cores = []

    # --- Objeto 1: Paralelepípedo como base/chão ---
    # A função paralelepipedo() agora é importada do seu próprio arquivo.
    v_caixa, _, f_caixa = paralelepipedo(largura=8, altura=3, profundidade=5)
    mat_caixa = matriz_translacao(-6, -6, -6)
    v_caixa = aplicar_transformacao(v_caixa, mat_caixa)

    offset = len(todos_vertices)
    todos_vertices.extend(v_caixa)
    todas_faces.extend(np.array(f_caixa) + offset)
    todas_cores.extend(['gray'] * len(f_caixa))

    # --- Objeto 2: Cilindro em pé ---
    v_cil, _, f_cil = cilindro(raio=2, altura=6)
    mat_cil = matriz_translacao(5, 0, 5)
    v_cil = aplicar_transformacao(v_cil, mat_cil)

    offset = len(todos_vertices)
    todos_vertices.extend(v_cil)
    todas_faces.extend(np.array(f_cil) + offset)
    todas_cores.extend(['cornflowerblue'] * len(f_cil))

    # --- Objeto 3: Cano Reto deitado ---
    v_cano_r, _, f_cano_r = cano_reto(raio=1.5, comprimento=8, espessura=0.3)
    mat_rot_cano_r = matriz_rotacao_y(90)
    mat_trans_cano_r = matriz_translacao(-8, 1.5, 0)
    v_cano_r = aplicar_transformacao(v_cano_r, mat_rot_cano_r)
    v_cano_r = aplicar_transformacao(v_cano_r, mat_trans_cano_r)

    offset = len(todos_vertices)
    todos_vertices.extend(v_cano_r)
    todas_faces.extend(np.array(f_cano_r) + offset)
    todas_cores.extend(['lightgreen'] * len(f_cano_r))

    # --- Objeto 4: Cano Curvado ---
    P0, P1 = np.array([-5,1, -8]), np.array([0,6,-4])
    T0, T1 = np.array([10,15,5]), np.array([5,0,10])
    v_cano_c, _, f_cano_c = cano_curvado(1, 0.2, P0, P1, T0, T1, 30, 12)

    offset = len(todos_vertices)
    todos_vertices.extend(v_cano_c)
    todas_faces.extend(np.array(f_cano_c) + offset)
    todas_cores.extend(['deepskyblue'] * len(f_cano_c))

    # --- Objeto 5: Linha Reta no ar ---
    v_linha, a_linha, _ = linha_reta(7)
    mat_rot1 = matriz_rotacao_y(45)
    mat_rot2 = matriz_rotacao_z(30)
    mat_trans = matriz_translacao(0, 7, -8)
    v_linha = aplicar_transformacao(v_linha, mat_rot1 @ mat_rot2 @ mat_trans)

    return np.array(todos_vertices), todas_faces, todas_cores, v_linha, a_linha

# --- SESSÃO 4: Bloco de Execução Principal e Visualização (Permanece igual) ---

if __name__ == '__main__':

    vertices_cena, faces_cena, cores_faces, vertices_linha, arestas_linha = compor_cena()
    fig = plt.figure(figsize=(15, 12))
    ax: Axes3D = fig.add_subplot(projection='3d')

    # Renderizar os sólidos com faces
    poly3d = [vertices_cena[list(face)] for face in faces_cena]
    colecao_poligonos = Poly3DCollection(poly3d, alpha=1.0)
    colecao_poligonos.set_facecolor(cores_faces)
    ax.add_collection3d(colecao_poligonos)

    #Renderizar as arestas da linha reta
    for aresta in arestas_linha:
        p_inicio, p_fim = vertices_linha[aresta[0]], vertices_linha[aresta[1]]
        ax.plot([p_inicio[0], p_fim[0]], [p_inicio[1], p_fim[1]], [p_inicio[2], p_fim[2]], color='red', linewidth=3)

    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')
    ax.set_title('Cena 3D com Sólidos Modulares')

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_zlim(-10, 10)

    ax.view_init(elev=30, azim=-75)
    plt.grid(True)
    plt.show()
