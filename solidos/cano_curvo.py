import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D

# --- Função Auxiliar para Curva de Hermite ---
def curva_hermite(P0, P1, T0, T1, num_pontos=50):
    """
    Calcula os pontos de uma curva de Hermite cúbica 3D.

    Args:
        P0 (np.array): Ponto inicial da curva.
        P1 (np.array): Ponto final da curva.
        T0 (np.array): Vetor tangente no ponto inicial.
        T1 (np.array): Vetor tangente no ponto final.
        num_pontos (int): Número de pontos para gerar na curva.

    Returns:
        np.array: Um array de pontos 3D que formam a curva.
    """
    t = np.linspace(0, 1, num_pontos)
    h00 = 2*t**3 - 3*t**2 + 1
    h10 = t**3 - 2*t**2 + t
    h01 = -2*t**3 + 3*t**2
    h11 = t**3 - t**2

    curva = np.outer(h00, P0) + np.outer(h10, T0) + np.outer(h01, P1) + np.outer(h11, T1)
    return curva

# --- Função Principal para Modelagem do Cano Curvado ---
def cano_curvado(raio, espessura, P0, P1, T0, T1, num_segmentos_curva=50, num_divisoes_circulo=20):
    """
    Modela um cano curvado ao longo de uma curva de Hermite, usando faces triangulares.

    Args:
        raio (float): O raio externo do cano.
        espessura (float): A espessura da parede do cano.
        P0, P1, T0, T1: Parâmetros da curva de Hermite (pontos e tangentes).
        num_segmentos_curva (int): Número de anéis de vértices ao longo do cano.
        num_divisoes_circulo (int): Número de vértices em cada anel circular.

    Returns:
        tuple: Uma tupla contendo (vértices, arestas, faces).
    """
    if espessura >= raio:
        raise ValueError("A espessura deve ser menor que o raio.")

    # --- 1. Gerar a "espinha" do cano ---
    pontos_curva = curva_hermite(P0, P1, T0, T1, num_segmentos_curva)

    # --- 2. Preparar para gerar a malha ---
    raio_interno = raio - espessura
    vertices = []
    faces = []
    arestas = []
    angulos_circulo = np.linspace(0, 2 * np.pi, num_divisoes_circulo, endpoint=False)

    # --- 3. Calcular os frames e gerar os vértices ---
    # Começamos com um vetor "para cima" arbitrário
    up = np.array([0, 1, 0])

    for i in range(num_segmentos_curva):
        # Vetor tangente (direção da curva)
        if i < num_segmentos_curva - 1:
            tangente = pontos_curva[i+1] - pontos_curva[i]
        else: # Reutiliza a última tangente para o último ponto
            tangente = pontos_curva[i] - pontos_curva[i-1]

        tangente = tangente / np.linalg.norm(tangente)

        # Evitar problema se a tangente for paralela ao vetor "up"
        if np.allclose(np.abs(np.dot(tangente, up)), 1.0):
            up = np.array([1, 0, 0]) # Usa um vetor "up" diferente

        # Calcula os vetores Normal e Binormal para criar o plano do anel
        # Usamos o processo de Gram-Schmidt para garantir a ortogonalidade
        normal = up - np.dot(up, tangente) * tangente
        normal = normal / np.linalg.norm(normal)
        binormal = np.cross(tangente, normal)

        # Gera os anéis de vértices (externo e interno) neste ponto da curva
        centro_anel = pontos_curva[i]
        for angulo in angulos_circulo:
            # Ponto no círculo externo
            offset_vetor = (normal * np.cos(angulo) + binormal * np.sin(angulo))
            vertices.append(centro_anel + raio * offset_vetor)
            # Ponto no círculo interno
            vertices.append(centro_anel + raio_interno * offset_vetor)

    vertices = np.array(vertices)

    # --- 4. Gerar Faces Triangulares e Arestas ---
    for i in range(num_segmentos_curva - 1): # Itera pelos "segmentos" do cano
        for j in range(num_divisoes_circulo): # Itera pelos vértices de cada anel
            # Índice do próximo vértice no anel (com wrap-around)
            k = (j + 1) % num_divisoes_circulo

            # Índices dos vértices para o quadrilátero atual
            # Cada "passo" no loop externo gera 2 vértices (externo, interno)
            # por divisão de círculo.
            idx_v1_ext = (i * num_divisoes_circulo + j) * 2
            idx_v1_int = idx_v1_ext + 1
            idx_v2_ext = (i * num_divisoes_circulo + k) * 2
            idx_v2_int = idx_v2_ext + 1

            idx_v3_ext = ((i + 1) * num_divisoes_circulo + k) * 2
            idx_v3_int = idx_v3_ext + 1
            idx_v4_ext = ((i + 1) * num_divisoes_circulo + j) * 2
            idx_v4_int = idx_v4_ext + 1

            # Triangulação da superfície externa
            faces.append((idx_v1_ext, idx_v4_ext, idx_v3_ext))
            faces.append((idx_v1_ext, idx_v3_ext, idx_v2_ext))

            # Triangulação da superfície interna
            faces.append((idx_v1_int, idx_v3_int, idx_v4_int))
            faces.append((idx_v1_int, idx_v2_int, idx_v3_int))

            # Arestas
            arestas.append((idx_v1_ext, idx_v2_ext)) # Aresta no anel i (externo)
            arestas.append((idx_v1_int, idx_v2_int)) # Aresta no anel i (interno)
            arestas.append((idx_v1_ext, idx_v4_ext)) # Aresta longitudinal

    # --- 5. Gerar faces das "tampas" (anéis de início e fim) ---
    for j in range(num_divisoes_circulo):
        k = (j + 1) % num_divisoes_circulo

        # Tampa inicial
        idx_i_v1_ext = (0 * num_divisoes_circulo + j) * 2
        idx_i_v1_int = idx_i_v1_ext + 1
        idx_i_v2_ext = (0 * num_divisoes_circulo + k) * 2
        idx_i_v2_int = idx_i_v2_ext + 1
        faces.append((idx_i_v1_int, idx_i_v2_ext, idx_i_v1_ext))
        faces.append((idx_i_v1_int, idx_i_v2_int, idx_i_v2_ext))

        # Tampa final
        idx_f_v1_ext = ((num_segmentos_curva - 1) * num_divisoes_circulo + j) * 2
        idx_f_v1_int = idx_f_v1_ext + 1
        idx_f_v2_ext = ((num_segmentos_curva - 1) * num_divisoes_circulo + k) * 2
        idx_f_v2_int = idx_f_v2_ext + 1
        faces.append((idx_f_v1_int, idx_f_v1_ext, idx_f_v2_ext))
        faces.append((idx_f_v1_int, idx_f_v2_ext, idx_f_v2_int))

    return vertices, arestas, faces

# --- Bloco de Execução Principal e Visualização ---
if __name__ == '__main__':
    # --- Parâmetros da Curva de Hermite ---
    # Pontos de início e fim do cano
    P0 = np.array([0, 0, 0])
    P1 = np.array([10, 0, 10])
    # Vetores tangentes (controlam a "força" e direção da curvatura)
    T0 = np.array([15, 0, 0])
    T1 = np.array([0, 15, 0])

    # --- Parâmetros do Cano ---
    raio_cano = 1.0
    espessura_cano = 0.2

    # Gerar a geometria do cano curvado
    vertices_cano, arestas_cano, faces_cano = cano_curvado(
        raio=raio_cano,
        espessura=espessura_cano,
        P0=P0, P1=P1, T0=T0, T1=T1,
        num_segmentos_curva=40,
        num_divisoes_circulo=16
    )

    # --- Visualização 3D ---
    fig = plt.figure(figsize=(12, 10))
    ax: Axes3D = fig.add_subplot(projection='3d')

    # Preparar faces para renderização
    poly3d = [vertices_cano[list(face)] for face in faces_cano]

    # Adicionar a coleção de polígonos (faces) ao gráfico
    ax.add_collection3d(Poly3DCollection(
        poly3d,
        facecolors='deepskyblue',
        linewidths=0.5,
        edgecolors='black',
        alpha=1.0
    ))

    # Configurações do gráfico
    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')
    ax.set_title('Modelo de Cano Curvado com Curva de Hermite')

    # Ajustar limites para centralizar o objeto
    max_range = np.array([vertices_cano[:,0].max()-vertices_cano[:,0].min(),
                          vertices_cano[:,1].max()-vertices_cano[:,1].min(),
                          vertices_cano[:,2].max()-vertices_cano[:,2].min()]).max() / 2.0

    mid_x = (vertices_cano[:,0].max()+vertices_cano[:,0].min()) * 0.5
    mid_y = (vertices_cano[:,1].max()+vertices_cano[:,1].min()) * 0.5
    mid_z = (vertices_cano[:,2].max()+vertices_cano[:,2].min()) * 0.5

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    ax.view_init(elev=100, azim=220, roll=-50)
    plt.show()
