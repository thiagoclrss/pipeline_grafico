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
from matrizes_transformacao import matriz_translacao, matriz_rotacao_z, matriz_rotacao_y, matriz_escala, aplicar_transformacao


def compor_cena():
    todos_vertices = []
    todas_faces = []
    todas_cores = []

    v_caixa, _, f_caixa = paralelepipedo(largura=8, altura=3, profundidade=5)
    mat_caixa = matriz_translacao(-2, -8, -2)
    v_caixa = aplicar_transformacao(v_caixa, mat_caixa)

    offset = len(todos_vertices)
    todos_vertices.extend(v_caixa)
    todas_faces.extend(np.array(f_caixa) + offset)
    todas_cores.extend(['gray'] * len(f_caixa))

    v_cil, _, f_cil = cilindro(raio=2, altura=6)
    mat_cil = matriz_translacao(5, 0, 2)
    v_cil = aplicar_transformacao(v_cil, mat_cil)

    offset = len(todos_vertices)
    todos_vertices.extend(v_cil)
    todas_faces.extend(np.array(f_cil) + offset)
    todas_cores.extend(['cornflowerblue'] * len(f_cil))

    v_cano_r, _, f_cano_r = cano_reto(raio=1.5, comprimento=8, espessura=0.3)
    mat_rot_cano_r = matriz_rotacao_y(45)
    mat_trans_cano_r = matriz_translacao(-8, 1.5, 2)
    v_cano_r = aplicar_transformacao(v_cano_r, mat_rot_cano_r)
    v_cano_r = aplicar_transformacao(v_cano_r, mat_trans_cano_r)

    offset = len(todos_vertices)
    todos_vertices.extend(v_cano_r)
    todas_faces.extend(np.array(f_cano_r) + offset)
    todas_cores.extend(['lightgreen'] * len(f_cano_r))

    P0, P1 = np.array([0,3, 6]), np.array([5,8,10])
    T0, T1 = np.array([10,15,5]), np.array([5,0,10])
    v_cano_c, _, f_cano_c = cano_curvado(1, 0.2, P0, P1, T0, T1, 30, 12)

    offset = len(todos_vertices)
    todos_vertices.extend(v_cano_c)
    todas_faces.extend(np.array(f_cano_c) + offset)
    todas_cores.extend(['deepskyblue'] * len(f_cano_c))

    v_linha, a_linha, _ = linha_reta(7)
    mat_rot1 = matriz_rotacao_y(45)
    mat_rot2 = matriz_rotacao_z(30)
    mat_trans = matriz_translacao(0, 7, 2)
    v_linha = aplicar_transformacao(v_linha, mat_rot1 @ mat_rot2 @ mat_trans)

    return np.array(todos_vertices), todas_faces, todas_cores, v_linha, a_linha

if __name__ == '__main__':

    vertices_cena, faces_cena, cores_faces, vertices_linha, arestas_linha = compor_cena()
    fig = plt.figure(figsize=(15, 12))
    ax: Axes3D = fig.add_subplot(projection='3d')


    poly3d = [vertices_cena[list(face)] for face in faces_cena]
    colecao_poligonos = Poly3DCollection(poly3d, alpha=1.0)
    colecao_poligonos.set_facecolor(cores_faces)
    ax.add_collection3d(colecao_poligonos)


    for aresta in arestas_linha:
        p_inicio, p_fim = vertices_linha[aresta[0]], vertices_linha[aresta[1]]
        ax.plot([p_inicio[0], p_fim[0]], [p_inicio[1], p_fim[1]], [p_inicio[2], p_fim[2]], color='red', linewidth=3)

    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')
    ax.set_title('Cena 3D com Sólidos Modulares')

    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_zlim(-5, 20)

    ax.view_init(elev=30, azim=-75)
    plt.grid(True)
    plt.show()
