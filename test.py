import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from classes.diffusion import SimpleDiffusion

if __name__ == "__main__":
    s = SimpleDiffusion(100,100,9,20,(50,50),0.3,10)
    s.spatial_diffusion()
    fig = plt.figure()
    ax_image = fig.add_subplot(2,1,1)
    ims = []
    for i in range(0,s.max_iter-1):
        im = ax_image.imshow(s.result[:,:,i])
        ims.append([im])

    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True)
    time_data = np.array([range(0,s.max_iter),s.time_series])
    def update_line(num,data,line):
        line.set_data(data[...,:num])
        return line,

    ax_line = fig.add_subplot(2,1,2)
    ax_line.set_xlim(0,s.max_iter)
    ax_line.set_ylim(0,max(s.time_series)+100)
    l, = ax_line.plot([],[],'r-')
    line_ani = animation.FuncAnimation(fig, update_line, 25, fargs=(time_data, l),
                                       interval=50, blit=True)
    plt.tight_layout()
    plt.show()

    # fig, ax = plt.subplots()
    # ax.imshow(s.result[:,:,19])
    # plt.show()
