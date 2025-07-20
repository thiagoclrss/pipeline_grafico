import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D

def cilindro(raio, altura, num_divisoes=20):
    """
    Modela um cilindro sólido alinhado com o eixo Z, usando faces triangulares.

    Args:
        raio (float): O raio da base do cilindro.
        altura (float): A altura do cilindro ao longo do eixo Z.
        num_divisoes (int): O número de segmentos para formar a base circular.

    Returns:
        tuple: Uma tupla contendo (vértices, arestas, faces).
               - vertices: um array NumPy de pontos [x, y, z].
               - arestas: uma lista de tuplas conectando os índices dos vértices.
               - faces: uma lista de tuplas definindo as superfícies triangulares.
    """
    # Listas para armazenar a geometria
    vertices = []
    faces = []
    arestas = []

    # --- 1. Geração dos Vértices ---
    # Adicionar os pontos centrais da base e do topo primeiro
    centro_base = [0, 0, 0]
    centro_topo = [0, 0, altura]
    vertices.append(centro_base)
    vertices.append(centro_topo)

    # Gerar os vértices para as bordas dos círculos da base e do topo
    angulos = np.linspace(0, 2 * np.pi, num_divisoes, endpoint=False)
    for angulo in angulos:
        x = raio * np.cos(angulo)
        y = raio * np.sin(angulo)
        vertices.append([x, y, 0])      # Vértice na borda da base
        vertices.append([x, y, altura]) # Vértice na borda do topo

    vertices = np.array(vertices)

    # --- 2. Geração das Faces Triangulares e Arestas ---
    idx_centro_base = 0
    idx_centro_topo = 1

    for i in range(num_divisoes):
        j = (i + 1) % num_divisoes

        # Índices dos vértices nas bordas. Cada passo no loop de geração
        # criou 2 vértices (base, topo), começando do índice 2.
        idx_base_i = 2 + i * 2
        idx_topo_i = 2 + i * 2 + 1
        idx_base_j = 2 + j * 2
        idx_topo_j = 2 + j * 2 + 1

        # Triangulação da parede lateral
        faces.append((idx_base_i, idx_topo_j, idx_topo_i))
        faces.append((idx_base_i, idx_base_j, idx_topo_j))

        # Triangulação da tampa da base (sentido horário para normal apontar para baixo)
        faces.append((idx_centro_base, idx_base_j, idx_base_i))

        # Triangulação da tampa do topo (sentido anti-horário para normal apontar para cima)
        faces.append((idx_centro_topo, idx_topo_i, idx_topo_j))

        # Arestas (opcional, para visualização wireframe)
        arestas.append((idx_base_i, idx_base_j))  # Borda da base
        arestas.append((idx_topo_i, idx_topo_j))  # Borda do topo
        arestas.append((idx_base_i, idx_topo_i))  # Linha lateral
        arestas.append((idx_centro_base, idx_base_i)) # Raio da base
        arestas.append((idx_centro_topo, idx_topo_i)) # Raio do topo

    return vertices, arestas, faces

# --- Bloco de Execução Principal e Visualização ---
if __name__ == '__main__':
    # Parâmetros do cilindro
    raio_cilindro = 3.0
    altura_cilindro = 7.0

    # Gerar a geometria do cilindro
    vertices_cilindro, arestas_cilindro, faces_cilindro = cilindro(
        raio_cilindro, altura_cilindro, num_divisoes=32
    )

    # Configuração da visualização 3D
    fig = plt.figure(figsize=(10, 8))
    ax: Axes3D = fig.add_subplot(projection='3d')

    # Preparar faces para renderização
    poly3d = [vertices_cilindro[list(face)] for face in faces_cilindro]

    # Adicionar a coleção de polígonos (faces) ao gráfico
    ax.add_collection3d(Poly3DCollection(
        poly3d,
        facecolors='cornflowerblue',
        linewidths=0.5,
        edgecolors='black',
        alpha=1.0
    ))

    # Configurações do gráfico
    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')
    ax.set_title('Modelo de Cilindro Sólido com Malha Triangular')

    # Ajustar os limites para visualização adequada
    ax.set_box_aspect([raio_cilindro*2, raio_cilindro*2, altura_cilindro]) # Proporções mais realistas
    ax.set_xlim(-raio_cilindro*1.2, raio_cilindro*1.2)
    ax.set_ylim(-raio_cilindro*1.2, raio_cilindro*1.2)
    ax.set_zlim(0, altura_cilindro)

    ax.view_init(elev=20, azim=30)
    plt.show()
