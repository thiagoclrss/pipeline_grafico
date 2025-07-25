import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import solidos
import matplotlib.pyplot as plt
from skimage.draw import polygon as sk_polygon, line as sk_line

from camera import matriz_visao, aplicar_transformacao
from mundo import compor_cena
from cena_2d import matriz_projecao_perspectiva

def rasterizar_cena_resolucoes(vertices_cena, faces_cena, cores_faces, vertices_linha, arestas_linha, 
                               camera_pos, ponto_alvo, up_mundo, resolucoes):
    """
    Executa o pipeline de projeção e rasteriza a cena em um conjunto de imagens 2D
    em diferentes resoluções.
    """
    # --- 1. Definir Parâmetros e Matrizes de Transformação ---
    near_plane, far_plane, fov = 1.0, 50.0, 60.0
    
    mat_view = matriz_visao(camera_pos, ponto_alvo, up_mundo)
    # A razão de aspecto é 1.0 pois nossas telas de pixel serão quadradas
    mat_persp = matriz_projecao_perspectiva(fov, 1.0, near_plane, far_plane)
    mat_transform = mat_persp @ mat_view

    # --- 2. Preparar e Ordenar Polígonos (Algoritmo do Pintor) ---
    render_list_poligonos = []
    vertices_cena_scc = aplicar_transformacao(vertices_cena, mat_view)
    
    for i, face in enumerate(faces_cena):
        profundidade = np.mean(vertices_cena_scc[list(face), 2])
        if profundidade < -near_plane and profundidade > -far_plane:
            render_list_poligonos.append({
                'vertices_mundo': vertices_cena[list(face)],
                'cor': cores_faces[i],
                'profundidade': profundidade
            })
    render_list_poligonos.sort(key=lambda item: item['profundidade'])

    # --- 3. Configurar os Gráficos de Saída ---
    fig, axes = plt.subplots(1, len(resolucoes), figsize=(6 * len(resolucoes), 6))
    if len(resolucoes) == 1: axes = [axes] # Garante que axes seja uma lista
    fig.suptitle("Cena Rasterizada em Diferentes Resoluções", fontsize=16)

    # Dicionário para converter nomes de cores em valores RGB (0-1)
    cores_rgb = plt.colormaps['tab10'].colors
    mapa_cores = {
        'gray': (0.5, 0.5, 0.5), 'cornflowerblue': cores_rgb[0], 
        'lightgreen': cores_rgb[2], 'deepskyblue': cores_rgb[1], 'red': (1,0,0)
    }

    # --- 4. Loop de Rasterização para Cada Resolução ---
    for ax, res in zip(axes, resolucoes):
        # Cria um framebuffer (tela de pixels) RGB, inicializado como preto.
        framebuffer = np.zeros((res, res, 3))
        
        # --- 4a. Rasterizar Polígonos ---
        for item in render_list_poligonos:
            v_mundo = item['vertices_mundo']
            v_homogeneos = np.hstack((v_mundo, np.ones((v_mundo.shape[0], 1))))
            v_clip = (mat_transform @ v_homogeneos.T).T
            
            v_cn = v_clip[:, :2] / v_clip[:, 3, np.newaxis]
            
            # Mapear coordenadas Normalizadas [-1, 1] para coordenadas de pixel [0, res-1]
            pixel_coords = (v_cn + 1) / 2 * (res - 1)
            
            # Obter os pixels a serem preenchidos
            rr, cc = sk_polygon(pixel_coords[:, 1], pixel_coords[:, 0], shape=framebuffer.shape)
            # Pintar os pixels no framebuffer
            framebuffer[rr, cc] = mapa_cores.get(item['cor'], (1,1,1)) # Padrão branco se cor não encontrada

        # --- 4b. Rasterizar a Linha (sobre os polígonos) ---
        v_homogeneos_linha = np.hstack((vertices_linha, np.ones((vertices_linha.shape[0], 1))))
        v_clip_linha = (mat_transform @ v_homogeneos_linha.T).T
        
        if np.all(v_clip_linha[:, 3] > 0): # Clipping simples
            v_cn_linha = v_clip_linha[:, :2] / v_clip_linha[:, 3, np.newaxis]
            pixel_coords_linha = (v_cn_linha + 1) / 2 * (res - 1)
            
            for aresta in arestas_linha:
                p1, p2 = pixel_coords_linha[aresta[0]], pixel_coords_linha[aresta[1]]
                rr, cc = sk_line(int(p1[1]), int(p1[0]), int(p2[1]), int(p2[0]))
                valid_idx = (rr >= 0) & (rr < res) & (cc >= 0) & (cc < res)
                framebuffer[rr[valid_idx], cc[valid_idx]] = mapa_cores['red']
        
        # --- 4c. Exibir a Imagem Rasterizada ---
        ax.imshow(framebuffer, origin='lower')
        ax.set_title(f"{res}x{res} pixels")
        ax.set_xticks([]); ax.set_yticks([])

    plt.show()

if __name__ == '__main__':

    # --- Montagem da Cena no SCM (sem alterações) ---
    vertices_cena, faces_cena, cores_faces, vertices_linha, arestas_linha = compor_cena()

    posicao_camera = np.array([15, 13, 12])
    ponto_alvo = np.array([0, 0, 0])
    vetor_up_mundo = np.array([0, 0, 1])

    resolucoes = [100, 250, 800]

    rasterizar_cena_resolucoes(vertices_cena, faces_cena, cores_faces, vertices_linha, arestas_linha,
                               posicao_camera, ponto_alvo, vetor_up_mundo, resolucoes)
