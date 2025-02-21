# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:50:01 2020

@author: Sander
"""


import numba

class MandleBrot():
    gpu_enabled = True
    try:
        import cupy as cp
    except:
        print("Cupy could not be imported properly, GPU mode has been disabled")
        gpu_enabled = False
    import matplotlib.pyplot as plt
    import numpy as np
    import time
    import os
    import cv2
    
    power = 2
    resolution = 1000
    iterations = 250
    #map_range = (-2,2,-2,2)
    map_range = (-2,2,0,2)   # Experimental
    zoom = 0.75
    offset_x = -0.75
    offset_y = 0
    
    glowIntensity = 1.5
    
    zoomed_offset_y = 0 * zoom
    zoomed_offset_x = 0 * zoom
    
    path = "./mandlebrot_renders/"
    
    dark_mode_type = 0
    # 0 = white background, black mandlebrot
    # 1 = black background, white mandlebrot
    # 2 = black background, black mandlebrot
    
    
    def save_last(self, name):
        if not self.os.path.exists(self.path):
            self.os.mkdir(self.path)
        self.cv2.imwrite(self.path + name + ".png", self.rendered_pic)
    
    
    def render(self, mode = "CPU", show_output = 0, Experimental = False):
        if not self.gpu_enabled and mode == "GPU":
            mode = "CPU"
            print("As some functionality has been disabled, the render will be performed in CPU mode")
            
        if Experimental:
            self.map_range = (-2,2,0,2)
            if mode == "GPU":
                self.rendered_pic = self.__render_optimized(self.cp)
            if mode == "CPU":
                self.rendered_pic = self.__render_optimized(self.np)
        
        else:
            self.map_range = (-2,2,-2,2)
            if mode == "GPU":
                self.rendered_pic = self.__render(self.cp)
            if mode == "CPU":
                self.rendered_pic = self.__render(self.np)
                    
        if show_output: self.plt.imshow(self.rendered_pic * 255, cmap = "gray")
        if self.dark_mode_type == 0: self.rendered_pic = 255 - self.rendered_pic
        if self.dark_mode_type == 2: self.rendered_pic[self.np.where(self.rendered_pic == 255)] = 0
    
    
    def __render(self, math_funcs):
            
        bin_map       = math_funcs.empty((self.resolution, self.resolution), dtype = math_funcs.uint8)
        bin_iteration = math_funcs.zeros((self.resolution, self.resolution), dtype = math_funcs.uint32)
        
        print("coordinates are x=" + str(self.offset_x + self.zoomed_offset_x) + ", y=" + str(self.offset_y + self.zoomed_offset_y) + ", zoom=" + str(1/self.zoom))
        
        mesh = math_funcs.meshgrid(math_funcs.linspace(self.map_range[0] * self.zoom + self.offset_x + self.zoomed_offset_x, \
                                    self.map_range[1] * self.zoom + self.offset_x + self.zoomed_offset_x, bin_map.shape[1]), \
                   math_funcs.linspace(self.map_range[2] * self.zoom - self.offset_y - self.zoomed_offset_y,\
                                    self.map_range[3] * self.zoom - self.offset_y - self.zoomed_offset_y, bin_map.shape[0]))
        mesh = mesh[0].astype(math_funcs.complex128) + 1j * mesh[1].astype(math_funcs.complex128)
        print(mesh.shape)
        
        t = self.time.time()
        bin_map = self.iterate2(mesh, self.iterations, bin_iteration, math_funcs)
        if self.gpu_enabled: 
            if math_funcs == self.cp:
                math_funcs.cuda.Device(0).synchronize()
        print("Rendered in " + str(round(self.time.time()-t, 3)) + " seconds")
        
        if self.gpu_enabled: 
            if math_funcs == self.cp:
                bin_iteration = bin_iteration.get()
        
        
        
        bin_iteration = self.np.log2(bin_iteration+1)**self.glowIntensity
        
        end_result = ((bin_iteration / bin_iteration.max()) * 255).astype(self.np.uint8)
        
        return end_result

    
    def __render_optimized(self, math_funcs):
        """

        Parameters
        ----------
        math_funcs : This is the value that indicates if cupy or numpy is used.
              cupy  - use the GPU
              numpy - use the CPU (VERY SLOW!!!)

        Returns
        -------
        end_result_2 : rendered mandlebrot
        """
        
        bin_iteration = math_funcs.zeros((self.resolution//2, self.resolution), dtype = math_funcs.uint16)
        print("coordinates are x=" + str(self.offset_x + self.zoomed_offset_x) + ", y=" + str(self.offset_y + self.zoomed_offset_y) + ", zoom=" + str(1/self.zoom))
        
        mesh = math_funcs.meshgrid( \
        math_funcs.linspace(self.map_range[0] * self.zoom + self.offset_x + self.zoomed_offset_x, self.map_range[1] * self.zoom + self.offset_x + self.zoomed_offset_x, bin_iteration.shape[1]), \
        math_funcs.linspace(self.map_range[2] * self.zoom - self.offset_y - self.zoomed_offset_y, self.map_range[3] * self.zoom - self.offset_y - self.zoomed_offset_y, bin_iteration.shape[0]))
        mesh = mesh[0].astype(math_funcs.complex64) + 1j * mesh[1].astype(math_funcs.complex64)
        t = self.time.time()
        self.__iterate(mesh, self.iterations, bin_iteration, math_funcs)
        if self.gpu_enabled: 
            if math_funcs == self.cp:
                math_funcs.cuda.Device(0).synchronize()
        print("Rendered in " + str(round(self.time.time()-t, 3)) + " seconds")
        
        if self.gpu_enabled: 
            if math_funcs == self.cp:
                bin_iteration = bin_iteration.get()
        
        end_result = bin_iteration.max() - bin_iteration
        end_result = end_result / self.iterations
        end_result = (end_result * 255).astype(self.np.uint8)
        end_result_2 = self.np.empty((self.resolution-1, self.resolution))
        end_result_2[:self.resolution//2, :] = end_result[::-1]
        end_result_2[self.resolution//2:, :] = end_result[1:]
        
        return end_result_2
    
    # @numba.jit
    def iterate2(self, num, iterations, bin_iteration, math_funcs):
        value = num
        for i in range(iterations):
            value = value ** 2 + num
            bin_iteration += math_funcs.abs(value) < 2
        return bin_iteration
    
    def renderHUGE(self, size):
        print("initting empty array", flush=True)
        self.map_range = (-2,2,-2,2)
        bin_iteration = self.np.zeros((size, size), dtype = self.np.float32)
        print("Creating meshgrid", flush=True)
        #mesh = self.np.tile(self.np.linspace(self.map_range[0] * self.zoom + self.offset_x + self.zoomed_offset_x, self.map_range[1] * self.zoom + self.offset_x + self.zoomed_offset_x, bin_iteration.shape[1], dtype=self.np.complex64))
        #print("Making the mesh complex", flush=True)
        #mesh.imag = self.np.tile(self.np.linspace(self.map_range[2] * self.zoom - self.offset_y - self.zoomed_offset_y, self.map_range[3] * self.zoom - self.offset_y - self.zoomed_offset_y, bin_iteration.shape[0], dtype=self.np.float32)
        #x = 
        X_line = self.np.linspace(self.map_range[0] * self.zoom + self.offset_x + self.zoomed_offset_x,\
                                  self.map_range[1] * self.zoom + self.offset_x + self.zoomed_offset_x,\
                                  bin_iteration.shape[1])
        
        Y_line = 1j * self.np.linspace(self.map_range[2] * self.zoom + self.offset_y + self.zoomed_offset_y,\
                                  self.map_range[3] * self.zoom + self.offset_y + self.zoomed_offset_y,\
                                  bin_iteration.shape[0]).reshape(-1,1)
           
        # self.X = X_line
        # self.Y = Y_line
        
        splitSize = 5000
        splits = self.np.ceil(size / splitSize)
        
        print("{} splits required".format(splits**2))
        
        # splits = 5
        
        t = self.time.time()
        for block_y in range(int(splits)):
            for block_x in range(int(splits)):
                #print("Calc block")
                calc_block = self.cp.asarray(X_line[block_x*splitSize:block_x*splitSize+splitSize]) + \
                             self.cp.asarray(Y_line[block_y*splitSize:block_y*splitSize+splitSize])
                # print("BLOCK->",calc_block.shape)
                # print("BIN  ->", bin_iteration.shape)
                #print("Iterate")
                yoink = \
                    self.iterate2(calc_block, \
                                  self.iterations, \
                                  self.cp.asarray(bin_iteration[block_y*splitSize:block_y*splitSize+splitSize, block_x*splitSize:block_x*splitSize+splitSize]), \
                                  self.cp).get()
                print("\rSplit " + str(block_y * splits + block_x+1) + "/" + str(splits ** 2) +" done", end="", flush=True)
                bin_iteration[block_y*splitSize:block_y*splitSize+splitSize, block_x*splitSize:block_x*splitSize+splitSize] = yoink
        
        print("\nRendered in " + str(round(self.time.time()-t, 3)) + " seconds", flush=True)
        
                # bin_iteration[]
                # pass
        
        # print("Flattening Mesh", flush=True)
        # # mesh = mesh.ravel()
        # bin_iteration = bin_iteration.ravel()
        # # self.mesh = mesh
        # self.bin_iteration = bin_iteration
        # splitSize = 100 ** 2
        # totalSize = size ** 2
        # splits = self.np.ceil(totalSize/(splitSize)).astype(self.np.uint16)
        
        # print(str(splits) + " split(s) required", flush=True)
        # t = self.time.time()
        # for i in range(splits):
        #     bin_iteration[splitSize*i:splitSize*(i+1)] = self.iterate2(self.cp.asarray(mesh[splitSize*i:splitSize*(i+1)]), self.iterations, self.cp.asarray(bin_iteration[splitSize*i:splitSize*(i+1)]), self.cp).get()
        #     print("\rSplit " + str(i+1) + "/" + str(splits) +" done", end="", flush=True)
        # print()
        
        # print("\nRendered in " + str(round(self.time.time()-t, 3)) + " seconds", flush=True)

        # print(bin_iteration.max())
        # del(mesh)
        
        print("optimizing output-1")
        # bin_iteration[self.np.where(bin_iteration != 0)] = self.np.log2(bin_iteration[self.np.where(bin_iteration != 0)]+1)**self.glowIntensity
        
        print("optimizing output-2")
        # end_result = ((bin_iteration / bin_iteration.max()) * 255).astype(self.np.uint8)
        
        return bin_iteration
        # bin_iteration = self.np.sqrt(self.np.sqrt(bin_iteration))
        # return (bin_iteration / bin_iteration.real.max() * 255).astype(self.np.uint8).reshape(size,size)
    
if __name__ == "__main__":
    
    import cv2
    m = MandleBrot() 
    m.resolution    = 10000
    m.iterations    = 255
    m.glowIntensity = 1.5
    
    a = m.renderHUGE(40000)
    cv2.imwrite("HUGE.png", a)
    
    # for mode in ["GPU"]:
    #     for dm in range(1):
    #         if 1:
    #             m.dark_mode_type = dm
    #             m.render(mode, show_output = False, Experimental = False)
    #             m.save_last("dark_mode_" + mode + "_" + str(dm))
            
            
            
            
            
            
            
            
            
            
            
            
            