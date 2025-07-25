import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D

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
    vertices_2d = np.atleast_2d(vertices)
    vertices_homogeneos = np.hstack((vertices_2d, np.ones((vertices_2d.shape[0], 1))))
    vertices_transformados = (matriz @ vertices_homogeneos.T).T
    return vertices_transformados[:, :3]
