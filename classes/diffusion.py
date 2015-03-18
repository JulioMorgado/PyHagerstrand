# -*- coding: utf-8 -*-
import numpy as np
from scipy.spatial.distance import cdist



class SimpleDiffusion(object):
    """Modelo simple de difusión espacial basado en Hägerstrand.

    1.- Espacio homogeneo e isotrópico
    2.- Un sólo difusor inicial
    3.- ....otras suposiciones...

    :param N: int Número de renglones en el espacio de simulación
    :param M: int Número de columnas en el espacio de simulación
    :param mif_size: int Tamaño de la matriz (cuadrada) del MIF (debe ser non)
    :param pob: int población en cada celda
    :param initial_diff: (int,int) Coordenadas del difusor inicial
    :param p0: float Probabilidad de auto-difusión

    """

    def __init__(self,N=100,M=100,mif_size=5,pob=20,initial_diff=(50,50),
                p0=0.3):

        self.M = M
        self.N = N
        self._pob = pob
        self._p0 = p0
        self._infected_cells = []
        self._space = np.zeros((N,M),dtype=np.int8)
        self._pop_array = np.zeros((len(np.ravel(self._space)),pob),
                                    dtype=np.bool)
        if initial_diff[0] > M or initial_diff[1] > N:
            raise ValueError("Las coordenadas del difusor inicial no caen \
                                en el espacio")
        self._space[initial_diff[0],initial_diff[1]] = 1
        self._update_pop_array(initial_diff,False)
        if mif_size%2 == 0:
            raise ValueError("El tamaño del MIF debe ser non")
        else:
            self._mif = self._initialize_mif(mif_size)


    def _initialize_mif(self,mif_size):
        """Inicializa el MIF"""
        x = np.linspace(0.5,mif_size - 0.5,mif_size)
        y = np.linspace(0.5,mif_size - 0.5,mif_size)
        xv,yv = np.meshgrid(x,y)
        points = np.array(zip(np.ravel(xv),np.ravel(yv)))
        center = np.array([[mif_size/2 + 0.5,mif_size/2 + 0.5]])
        dist = cdist(center,points)
        dist = dist/np.sum(dist)
        #TODO: tiene que ser diferente para respetar el p0 del usuario
        dist.reshape(mif_size,mif_size)[mif_size/2,mif_size/2] = self._p0
        dist = dist/np.sum(dist)
        return np.cumsum(dist)



    def _update_pop_array(self,index,rand=True):
        """Actualiza la entrada index del array de población."""
        current = self._pop_array[self._space2pop_index(index)]
        if len(np.nonzero(current)[0]) < self._pob:
            current[len(np.nonzero(current)[0])] = True
            self._infected_cells.append(self._space2pop_index(index))
            return True
        else:
            return False

    def _space2pop_index(self,index):
        """Transforma el índice de space en el índice del pop_array.
        :param index (int,int) el ínidice a transformar
        """
        return np.ravel_multi_index(index,dims=(self.M,self.N))
