# -*- coding: utf-8 -*-
import numpy as np
#Si usas Mac, descomenta las siguientes líneas:
#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
from haggerstrand.diffusion import SimpleDiffusion

# if plt.get_backend() == 'MacOSX':
#     print 'MAC'
#     import matplotlib
#     matplotlib.use('TkAgg')

if __name__ == "__main__":
    s = SimpleDiffusion(50,50,9,20,[(20,20)],0.3,18)
    #s.spatial_diffusion()
    s.random_diffusion()
    fig = plt.figure()
    gs = gridspec.GridSpec(4,1)
    #gs = gridspec.GridSpec(2,1,width_ratios=[1,2],height_ratios=[2,1])
    ax_i_loc = gs.new_subplotspec((0,0), rowspan=3, colspan=1)
    ax_image = plt.subplot(ax_i_loc)
    ims = []
    for i in range(0,s.max_iter):
        im = ax_image.imshow(s.result[:,:,i])
        ims.append([im])

    ani = animation.ArtistAnimation(fig, ims, interval=100, blit=True)
    time_data = np.array([range(0,s.max_iter),s.time_series])
    def update_line(num,data,line):
        line.set_data(data[...,:num])
        return line,

    ax_line = plt.subplot(gs[3,0])
    ax_line.set_xlim(0,s.max_iter)
    ax_line.set_ylim(0,max(s.time_series)+100)
    l, = ax_line.plot([],[],'r-')
    line_ani = animation.FuncAnimation(fig, update_line, frames=s.max_iter, fargs=(time_data, l),
                                       interval=100, blit=True)
    #plt.tight_layout()
    plt.show()

    # fig, ax = plt.subplots()
    # ax.imshow(s.result[:,:,19])
    # plt.show()
