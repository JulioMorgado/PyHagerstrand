# -*- coding: utf-8 -*-
from random import randint
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
    :param max_iter: int Máximo número de iteraciones

    :attribute _space: np.array(M,N,dtype=np.int8) El espacio disponible
    :attribute _pop_array: np.array(M*N,pob,dtype=np.bool) array de habitantes
                           en cada celda
    :attribute _infected_pop: list (space_idx,int) Lista de los índices de las
                                celdas adoptantes. La primera entrada es el
                                índice aplanado de la celda en la matriz space y
                                la segunda es el número del poblador en
                                pop_array. Es decir, la lista de las direcciones
                                de cada poblador infectado.

    """

    def __init__(self,N=100,M=100,mif_size=5,pob=20,initial_diff=(50,50),
                p0=0.3, max_iter=1000):

        self.M = M
        self.N = N
        self._pob = pob
        self._p0 = p0
        self.max_iter = max_iter
        self.iteration = 0
        self._infected_pop = []
        self._space = np.zeros((N,M),dtype=np.int8)
        self._pop_array = np.zeros((len(np.ravel(self._space)),pob),
                                    dtype=np.bool)
        if initial_diff[0] > M or initial_diff[1] > N:
            raise ValueError("Las coordenadas del difusor inicial no caen \
                                en el espacio")
        self._space[initial_diff[0],initial_diff[1]] = 1
        #Modificamos también al poblador original:
        index = self._space2pop_index(initial_diff)
        self._pop_array[index][0] = True
        self._infected_pop.append((index,0))
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



    def _update_pop_array(self,pob_adress):
        """Propaga hacia el habitante en pob_adress si es no-adoptante.

        :param pob_adress: (int,int) la dirección del habitante a propagar.
                            La primera entrada es el índice (aplanado) en space
                            y la segunda es el número del poblador en la celda
        """
        print "entr'e"
        current = self._pop_array[pob_adress[0]]
        #checo si es no-adoptante
        if current[pob_adress[1]] == False:
            current[pob_adress[1]] = True
        else:
            pass


    def _space2pop_index(self,index):
        """Transforma el índice de space en el índice del pop_array.
        :param index (int,int) el ínidice a transformar
        """
        print "el indice" + str(index)
        return np.ravel_multi_index(index,dims=(self.M,self.N))

    def _random_adress(self):
        """Regresa una dirección (pob_adress) al azar."""
        return (randint(0,(self.M*self.N) - 1),randint(0,self._pob - 1))

    # def diffuse(self):
    #     """Realiza la simulación.
    #
    #     :param iter: int iteración en la que vamos
    #     """
    #     print self.iteration
    #     if self.iteration == self.max_iter:
    #         print "acabé"
    #         return
    #     else:
    #         for cell in self._infected_pop:
    #             adress = self._random_adress()
    #             if adress == cell:
    #                 #TODO: hay que cambiar, podría pasar obtener dos veces
    #                 #el mismo
    #                 adress = self._random_adress()
    #
    #             self._update_pop_array(adress)
    #
    #     self.iteration += 1
    #     #self.diffuse()
