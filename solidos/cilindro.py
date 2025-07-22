import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D

def cilindro(raio, altura, num_divisoes=20):
    """
    Modela um cilindro sólido com orientação Y-Up (Y como altura), usando faces triangulares.
    A base do cilindro está no plano XZ.

    Args:
        raio (float): O raio da base do cilindro.
        altura (float): A altura do cilindro ao longo do eixo Y.
        num_divisoes (int): O número de segmentos para formar a base circular.

    Returns:
        tuple: Uma tupla contendo (vértices, arestas, faces).
    """
    # Listas para armazenar a geometria
    vertices = []
    faces = []
    arestas = []

    # --- 1. Geração dos Vértices (LÓGICA Y-UP) ---
    # Adicionar os pontos centrais da base (y=0) e do topo (y=altura)
    centro_base = [0, 0, 0]
    centro_topo = [0, altura, 0] # MUDANÇA: Altura aplicada em Y
    vertices.append(centro_base)
    vertices.append(centro_topo)

    # Gerar os vértices para as bordas dos círculos no plano XZ
    angulos = np.linspace(0, 2 * np.pi, num_divisoes, endpoint=False)
    for angulo in angulos:
        # O círculo é formado pelas coordenadas X e Z
        x = raio * np.cos(angulo)
        z = raio * np.sin(angulo)      # MUDANÇA: y -> z

        # A altura é aplicada na coordenada Y
        vertices.append([x, 0, z])      # Vértice na borda da base (y=0)
        vertices.append([x, altura, z]) # Vértice na borda do topo (y=altura)

    vertices = np.array(vertices)

    # --- 2. Geração das Faces Triangulares e Arestas ---
    # A lógica de indexação permanece a mesma, pois a ordem de criação dos vértices foi mantida.
    idx_centro_base = 0
    idx_centro_topo = 1

    for i in range(num_divisoes):
        j = (i + 1) % num_divisoes

        # Índices dos vértices nas bordas
        idx_base_i = 2 + i * 2
        idx_topo_i = 2 + i * 2 + 1
        idx_base_j = 2 + j * 2
        idx_topo_j = 2 + j * 2 + 1

        # Triangulação da parede lateral
        faces.append((idx_base_i, idx_topo_j, idx_topo_i))
        faces.append((idx_base_i, idx_base_j, idx_topo_j))

        # Triangulação da tampa da base (sentido horário para normal apontar para -Y)
        faces.append((idx_centro_base, idx_base_j, idx_base_i))

        # Triangulação da tampa do topo (sentido anti-horário para normal apontar para +Y)
        faces.append((idx_centro_topo, idx_topo_i, idx_topo_j))

        # Arestas (opcional, para visualização wireframe)
        arestas.append((idx_base_i, idx_base_j))
        arestas.append((idx_topo_i, idx_topo_j))
        arestas.append((idx_base_i, idx_topo_i))
        arestas.append((idx_centro_base, idx_base_i))
        arestas.append((idx_centro_topo, idx_topo_i))

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

    ax.set_box_aspect([raio_cilindro*2, altura_cilindro, raio_cilindro*2])
    # Limites em X e Z são baseados no raio
    ax.set_xlim(-raio_cilindro*1.5, raio_cilindro*1.5)
    ax.set_zlim(-raio_cilindro*1.5, raio_cilindro*1.5)
    # Limite em Y é baseado na altura
    ax.set_ylim(0, altura_cilindro)

    ax.view_init(elev=110, azim=210, roll=-61)
    plt.show()
