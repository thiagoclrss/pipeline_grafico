import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D

def cano_reto(raio, altura, espessura, num_divisoes=20):
    """
    Modela um cano reto (cilindro oco) alinhado com o eixo Z, usando faces triangulares.

    Args:
        raio (float): O raio externo do cano.
        comprimento (float): O comprimento do cano ao longo do eixo Z.
        espessura (float): A espessura da parede do cano.
        num_divisoes (int): O número de segmentos para formar os círculos.

    Returns:
        tuple: Uma tupla contendo (vértices, arestas, faces).
               - vertices: um array NumPy de pontos [x, y, z].
               - arestas: uma lista de tuplas conectando os índices dos vértices.
               - faces: uma lista de tuplas definindo as superfícies triangulares.
    """
    if espessura >= raio:
        raise ValueError("A espessura deve ser menor que o raio.")

    # Listas para armazenar a geometria
    vertices = []
    faces = []
    arestas = []

    # --- 1. Geração dos Vértices ---
    raio_interno = raio - espessura
    angulos = np.linspace(0, 2 * np.pi, num_divisoes, endpoint=False)

    # Vértices do círculo externo no início (z=0) e no fim (z=comprimento)
    for angulo in angulos:
        # O círculo agora é formado por X e Z para ficar no "chão"
        x = raio * np.cos(angulo)
        z = raio * np.sin(angulo) # MUDANÇA: y -> z

        # A altura agora é aplicada em Y
        vertices.append([x, 0, z])      # Vértice externo na base (y=0)
        vertices.append([x, altura, z]) # Vértice externo no topo (y=altura)

        # Vértices internos
        x_int = raio_interno * np.cos(angulo)
        z_int = raio_interno * np.sin(angulo) # MUDANÇA: y -> z
        vertices.append([x_int, 0, z_int])      # Vértice interno na base (y=0)
        vertices.append([x_int, altura, z_int]) # Vértice interno no topo (y=altura)

    vertices = np.array(vertices)

        # --- 2. Geração das Faces e Arestas (Lógica de indexação não muda) ---
    for i in range(num_divisoes):
        j = (i + 1) % num_divisoes

        # Índices dos 4 vértices para o segmento atual (externo e interno)
        idx_ext_base_i, idx_ext_topo_i = i * 4, i * 4 + 1
        idx_int_base_i, idx_int_topo_i = i * 4 + 2, i * 4 + 3
        idx_ext_base_j, idx_ext_topo_j = j * 4, j * 4 + 1
        idx_int_base_j, idx_int_topo_j = j * 4 + 2, j * 4 + 3

        # Triangulação da superfície externa
        faces.append((idx_ext_base_i, idx_ext_topo_j, idx_ext_topo_i))
        faces.append((idx_ext_base_i, idx_ext_base_j, idx_ext_topo_j))

        # Triangulação da superfície interna
        faces.append((idx_int_base_i, idx_int_topo_i, idx_int_topo_j))
        faces.append((idx_int_base_i, idx_int_topo_j, idx_int_base_j))

        # Triangulação do anel da base
        faces.append((idx_ext_base_i, idx_int_base_i, idx_int_base_j))
        faces.append((idx_ext_base_i, idx_int_base_j, idx_ext_base_j))

        # Triangulação do anel do topo
        faces.append((idx_ext_topo_i, idx_int_topo_j, idx_int_topo_i))
        faces.append((idx_ext_topo_i, idx_ext_topo_j, idx_int_topo_j))

        # Arestas
        arestas.append((idx_ext_base_i, idx_ext_base_j))
        arestas.append((idx_int_base_i, idx_int_base_j))
        arestas.append((idx_ext_topo_i, idx_ext_topo_j))
        arestas.append((idx_int_topo_i, idx_int_topo_j))
        arestas.append((idx_ext_base_i, idx_ext_topo_i))

    return vertices, arestas, faces

# --- Bloco de Execução Principal e Visualização ---
if __name__ == '__main__':
    # Parâmetros do cano
    raio_cano = 2.5
    altura_cano = 5.0
    espessura_cano = 0.5

    # Gerar a geometria do cano
    vertices_cano, arestas_cano, faces_cano = cano_reto(
        raio_cano, altura_cano, espessura_cano, num_divisoes=24
    )

    # Configuração da visualização 3D
    fig = plt.figure(figsize=(10, 8))
    ax: Axes3D = fig.add_subplot(projection='3d')

    # Preparar faces para renderização
    poly3d = [vertices_cano[list(face)] for face in faces_cano]

    # Adicionar a coleção de polígonos (faces) ao gráfico
    ax.add_collection3d(Poly3DCollection(
        poly3d,
        facecolors='lightgreen',
        linewidths=0.5,
        edgecolors='darkgreen',
        alpha=1.0
    ))

    # Configurações do gráfico
    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')
    ax.set_title('Modelo de Cano Reto com Malha Triangular')

    # Ajustar os limites para visualização adequada
    ax.set_xlim([-raio_cano*1.5, raio_cano*1.5])
    ax.set_ylim([-1, altura_cano + 1])
    ax.set_zlim([-raio_cano*1.5, raio_cano*1.5])

    ax.view_init(elev=110, azim=210, roll=-61)

    plt.show()
