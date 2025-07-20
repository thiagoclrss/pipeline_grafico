import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D

def cano_reto(raio, comprimento, espessura, num_divisoes=20):
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
        x_ext = raio * np.cos(angulo)
        y_ext = raio * np.sin(angulo)
        vertices.append([x_ext, y_ext, 0])
        vertices.append([x_ext, y_ext, comprimento])

    # Vértices do círculo interno no início (z=0) e no fim (z=comprimento)
    for angulo in angulos:
        x_int = raio_interno * np.cos(angulo)
        y_int = raio_interno * np.sin(angulo)
        vertices.append([x_int, y_int, 0])
        vertices.append([x_int, y_int, comprimento])

    vertices = np.array(vertices)

    # --- 2. Geração das Faces Triangulares e Arestas ---
    num_vertices_externos = num_divisoes * 2

    for i in range(num_divisoes):
        j = (i + 1) % num_divisoes

        # Índices para os vértices do anel externo
        idx_ext_inicio_i = i * 2
        idx_ext_fim_i = i * 2 + 1
        idx_ext_inicio_j = j * 2
        idx_ext_fim_j = j * 2 + 1

        # Índices para os vértices do anel interno
        idx_int_inicio_i = num_vertices_externos + i * 2
        idx_int_fim_i = num_vertices_externos + i * 2 + 1
        idx_int_inicio_j = num_vertices_externos + j * 2
        idx_int_fim_j = num_vertices_externos + j * 2 + 1

        # Triangulação da superfície externa
        faces.append((idx_ext_inicio_i, idx_ext_fim_j, idx_ext_fim_i))
        faces.append((idx_ext_inicio_i, idx_ext_inicio_j, idx_ext_fim_j))

        # Triangulação da superfície interna (ordem invertida para a normal)
        faces.append((idx_int_inicio_i, idx_int_fim_i, idx_int_fim_j))
        faces.append((idx_int_inicio_i, idx_int_fim_j, idx_int_inicio_j))

        # Triangulação do anel de início (borda)
        faces.append((idx_ext_inicio_i, idx_int_inicio_j, idx_int_inicio_i))
        faces.append((idx_ext_inicio_i, idx_ext_inicio_j, idx_int_inicio_j))

        # Triangulação do anel de fim (borda)
        faces.append((idx_ext_fim_i, idx_int_fim_i, idx_int_fim_j))
        faces.append((idx_ext_fim_i, idx_int_fim_j, idx_ext_fim_j))

        # Arestas (opcional, para visualização wireframe)
        arestas.append((idx_ext_inicio_i, idx_ext_inicio_j))
        arestas.append((idx_ext_fim_i, idx_ext_fim_j))
        arestas.append((idx_int_inicio_i, idx_int_inicio_j))
        arestas.append((idx_int_fim_i, idx_int_fim_j))
        arestas.append((idx_ext_inicio_i, idx_ext_fim_i))
        arestas.append((idx_int_inicio_i, idx_int_fim_i))

    return vertices, arestas, faces

# --- Bloco de Execução Principal e Visualização ---
if __name__ == '__main__':
    # Parâmetros do cano
    raio_cano = 2.5
    comprimento_cano = 8.0
    espessura_cano = 0.5

    # Gerar a geometria do cano
    vertices_cano, arestas_cano, faces_cano = cano_reto(
        raio_cano, comprimento_cano, espessura_cano, num_divisoes=24
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
    ax.set_ylim([-raio_cano*1.5, raio_cano*1.5])
    ax.set_zlim([-1, comprimento_cano + 1])
    ax.view_init(elev=25, azim=45)

    plt.show()
