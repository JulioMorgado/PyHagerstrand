from classes.diffusion import SimpleDiffusion

if __name__ == "__main__":
    s = SimpleDiffusion(100,100,5,20,(50,50),0.3,100)
    # print s._mif
    # print s._infected_pop
    # print s._random_adress()
    #s.random_diffusion()
    s.spatial_diffusion()
