# -*- coding: utf-8 -*-
import sys
from random import randint
from random import uniform
import numpy as np
from scipy.spatial.distance import cdist


sys.setrecursionlimit(11500)
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

    :attribute space: np.array(M,N,dtype=np.int8) El espacio disponible
    :attribute _pop_array: np.array(M*N,pob,dtype=np.bool) array de habitantes
                           en cada celda
    :attribute _infected_pop: list (space_idx,int) Lista de los índices de las
                                celdas adoptantes. La primera entrada es el
                                índice aplanado de la celda en la matriz space y
                                la segunda es el número del poblador en
                                pop_array. Es decir, la lista de las direcciones
                                de cada poblador infectado.
    :attribute results: np.array((M,N,max_iter)) Guarda los resultados de cada
                        iteración.
    :attribute time_series: list int Propagaciones por cada iteración

    """

    def __init__(self,N=100,M=100,mif_size=5,pob=20,initial_diff=(50,50),
                p0=0.3, max_iter=1000):

        self.M = M
        self.N = N
        self._pob = pob
        self._p0 = p0
        self.max_iter = max_iter
        self.mif_size = mif_size
        self.iteration = 0
        self._infected_pop = []
        self._tmp_adopted = []
        self.space = np.zeros((N,M),dtype=np.int8)
        self._pop_array = np.zeros((len(np.ravel(self.space)),pob),
                                    dtype=np.bool)
        self.result = np.zeros((M,N,max_iter),dtype=np.int8)
        self.time_series = []
        if initial_diff[0] > M or initial_diff[1] > N:
            raise ValueError("Las coordenadas del difusor inicial no caen \
                                en el espacio")
        self.space[initial_diff[0],initial_diff[1]] = 1
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



    def _propagate(self,pob_adress):
        """Propaga hacia el habitante en pob_adress si es no-adoptante.

        :param pob_adress: (int,int) la dirección del habitante a propagar.
                            La primera entrada es el índice (aplanado) en space
                            y la segunda es el número del poblador en la celda
        """

        #checo si es no-adoptante
        if self._pop_array[pob_adress[0]][pob_adress[1]] == False:
            self._pop_array[pob_adress[0]][pob_adress[1]] = True
            self._tmp_adopted.append(pob_adress)
            print "infecté al "  + str(pob_adress)

        else:
            print "Pasé"
            pass


    def _space2pop_index(self,index):
        """Transforma el índice de space en el índice del pop_array.
        :param index (int,int) el ínidice a transformar
        """
        return np.ravel_multi_index(index,dims=(self.M,self.N))

    def _pop2space_index(self,index):
        """Regresa la tupla (i,j) que corresponde al índice aplanado."""
        return np.unravel_index(index,dims=(self.M,self.N))

    def _mif2delta(self,index):
        """Regresa un tupla con los incrementos para llegar al cuadro propagado."""

        return np.unravel_index(index,dims=(self.mif_size,self.mif_size))

    def _random_adress(self):
        """Regresa una dirección (pob_adress) al azar."""
        return (randint(0,(self.M*self.N) - 1),randint(0,self._pob - 1))

    def _select_from_mif(self):
        """Regresa una dirección (pob_adress) a partir del MIF."""
        rnd = uniform(0,1)
        index = np.nonzero(self._mif>rnd)[0][0]
        return self._mif2delta(index)

    def _get_propagation_adress(self,adress):
        """Regresa una dirección pop_adress propagada por el MIF"""

        print "Propagó: " + str(adress)
        delta = self._select_from_mif()
        delta = (delta[0] - self.mif_size/2,delta[1] - self.mif_size/2)
        space_adress = self._pop2space_index(adress[0])
        prop_space_adress = (space_adress[0] + delta[0],
                              space_adress[1] + delta[1])
        try:
            habitant = randint(0,self._pob - 1)
            return (self._space2pop_index(prop_space_adress),habitant)
        except ValueError:
            return self._get_propagation_adress(adress)

    def spatial_diffusion(self):
        """Propaga al estilo Hagerstrand."""

        if self.iteration == self.max_iter:
            print "acabé"
            return
        else:
            for adress in self._infected_pop:
                propagated_adress = self._get_propagation_adress(adress)
                self._propagate(propagated_adress)

            self._infected_pop.extend(self._tmp_adopted)
            #print "Hay %i adoptantes" % len(self._infected_pop)
            self.result[:,:,self.iteration] = np.sum(self._pop_array,
                                                axis=1).reshape(self.M,self.N)
            self.time_series.append(len(self._tmp_adopted))
            self.iteration += 1
            self._tmp_adopted = []
            return self.spatial_diffusion()




    def random_diffusion(self):
        """Propaga aleatoriamente en el espacio."""

        print self.iteration
        if self.iteration == self.max_iter:
            #self.space = np.sum(s._pop_array,axis=1).reshape(s.M,s.N)
            print "acabé"
            return None
        else:
            for adress in self._infected_pop:
                rand_adress = self._random_adress()
                # if adress == rand_adress:
                #     #TODO: hay que cambiar, podría pasar obtener dos veces
                #     #el mismo
                #     rand_adress = self._random_adress()
                #
                print "Largo de lista: %i, número de iteraciones %i" % (len(self._infected_pop),self.iteration)
                self._propagate(rand_adress)

            self._infected_pop.extend(self._tmp_adopted)
            print "Hay %i adoptantes" % len(self._infected_pop)
            self.result[:,:,iteration] = np.sum(s._pop_array,axis=1).reshape(
                                                s.M,s.N)
            self.time_series.append(len(self-_tmp_adopted))
            self.iteration += 1
            self._tmp_adopted = []
            return self.random_diffusion()
