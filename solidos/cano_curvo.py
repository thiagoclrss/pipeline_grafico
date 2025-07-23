import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D

def curva_hermite(P0, P1, T0, T1, num_pontos=50):
    t = np.linspace(0, 1, num_pontos)
    h00 = 2*t**3 - 3*t**2 + 1
    h10 = t**3 - 2*t**2 + t
    h01 = -2*t**3 + 3*t**2
    h11 = t**3 - t**2

    curva = np.outer(h00, P0) + np.outer(h10, T0) + np.outer(h01, P1) + np.outer(h11, T1)
    return curva

def cano_curvado(raio, espessura, P0, P1, T0, T1, num_segmentos_curva=50, num_divisoes_circulo=20):

    if espessura >= raio:
        raise ValueError("A espessura deve ser menor que o raio.")

    pontos_curva = curva_hermite(P0, P1, T0, T1, num_segmentos_curva)
    raio_interno = raio - espessura
    vertices = []
    faces = []
    arestas = []
    angulos_circulo = np.linspace(0, 2 * np.pi, num_divisoes_circulo, endpoint=False)

    up = np.array([0, 1, 0])

    for i in range(num_segmentos_curva):
        if i < num_segmentos_curva - 1:
            tangente = pontos_curva[i+1] - pontos_curva[i]
        else:
            tangente = pontos_curva[i] - pontos_curva[i-1]

        tangente = tangente / np.linalg.norm(tangente)

        if np.allclose(np.abs(np.dot(tangente, up)), 1.0):
            up = np.array([1, 0, 0])

        normal = up - np.dot(up, tangente) * tangente
        normal = normal / np.linalg.norm(normal)
        binormal = np.cross(tangente, normal)

        centro_anel = pontos_curva[i]
        for angulo in angulos_circulo:
            offset_vetor = (normal * np.cos(angulo) + binormal * np.sin(angulo))
            vertices.append(centro_anel + raio * offset_vetor)
            vertices.append(centro_anel + raio_interno * offset_vetor)

    vertices = np.array(vertices)

    for i in range(num_segmentos_curva - 1):
        for j in range(num_divisoes_circulo):
            k = (j + 1) % num_divisoes_circulo

            idx_v1_ext = (i * num_divisoes_circulo + j) * 2
            idx_v1_int = idx_v1_ext + 1
            idx_v2_ext = (i * num_divisoes_circulo + k) * 2
            idx_v2_int = idx_v2_ext + 1

            idx_v3_ext = ((i + 1) * num_divisoes_circulo + k) * 2
            idx_v3_int = idx_v3_ext + 1
            idx_v4_ext = ((i + 1) * num_divisoes_circulo + j) * 2
            idx_v4_int = idx_v4_ext + 1

            faces.append((idx_v1_ext, idx_v4_ext, idx_v3_ext))
            faces.append((idx_v1_ext, idx_v3_ext, idx_v2_ext))

            faces.append((idx_v1_int, idx_v3_int, idx_v4_int))
            faces.append((idx_v1_int, idx_v2_int, idx_v3_int))

            arestas.append((idx_v1_ext, idx_v2_ext))
            arestas.append((idx_v1_int, idx_v2_int))
            arestas.append((idx_v1_ext, idx_v4_ext))

    for j in range(num_divisoes_circulo):
        k = (j + 1) % num_divisoes_circulo

        idx_i_v1_ext = (0 * num_divisoes_circulo + j) * 2
        idx_i_v1_int = idx_i_v1_ext + 1
        idx_i_v2_ext = (0 * num_divisoes_circulo + k) * 2
        idx_i_v2_int = idx_i_v2_ext + 1
        faces.append((idx_i_v1_int, idx_i_v2_ext, idx_i_v1_ext))
        faces.append((idx_i_v1_int, idx_i_v2_int, idx_i_v2_ext))

        idx_f_v1_ext = ((num_segmentos_curva - 1) * num_divisoes_circulo + j) * 2
        idx_f_v1_int = idx_f_v1_ext + 1
        idx_f_v2_ext = ((num_segmentos_curva - 1) * num_divisoes_circulo + k) * 2
        idx_f_v2_int = idx_f_v2_ext + 1
        faces.append((idx_f_v1_int, idx_f_v1_ext, idx_f_v2_ext))
        faces.append((idx_f_v1_int, idx_f_v2_ext, idx_f_v2_int))

    return vertices, arestas, faces

if __name__ == '__main__':

    P0 = np.array([0, 0, 0])
    P1 = np.array([10, 0, 10])
    T0 = np.array([15, 0, 0])
    T1 = np.array([0, 15, 0])

    raio_cano = 1.0
    espessura_cano = 0.2

    vertices_cano, arestas_cano, faces_cano = cano_curvado(
        raio=raio_cano,
        espessura=espessura_cano,
        P0=P0, P1=P1, T0=T0, T1=T1,
        num_segmentos_curva=40,
        num_divisoes_circulo=16
    )

    fig = plt.figure(figsize=(12, 10))
    ax: Axes3D = fig.add_subplot(projection='3d')

    poly3d = [vertices_cano[list(face)] for face in faces_cano]

    ax.add_collection3d(Poly3DCollection(
        poly3d,
        facecolors='deepskyblue',
        linewidths=0.5,
        edgecolors='black',
        alpha=1.0
    ))

    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')
    ax.set_title('Modelo de Cano Curvado')

    max_range = np.array([vertices_cano[:,0].max()-vertices_cano[:,0].min(),
                          vertices_cano[:,1].max()-vertices_cano[:,1].min(),
                          vertices_cano[:,2].max()-vertices_cano[:,2].min()]).max() / 2.0

    mid_x = (vertices_cano[:,0].max()+vertices_cano[:,0].min()) * 0.5
    mid_y = (vertices_cano[:,1].max()+vertices_cano[:,1].min()) * 0.5
    mid_z = (vertices_cano[:,2].max()+vertices_cano[:,2].min()) * 0.5

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    ax.view_init(elev=30, azim=-60)
    plt.show()
