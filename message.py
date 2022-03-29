
import math, cmath
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Pool
from enum import Enum
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

def bounded(args):
    number, iterations = args
    z=0
    for i in range(iterations):
        z=(z**2) + number
        if abs(z) > 1000:
            break
    return number.real, number.imag,int((i/iterations) * 512)


def render(xmin, xmax, ymin, ymax, resolution, iterations):
    width = int(abs(lowX - highX) * resolution)
    height = int(abs(lowY - highY) * resolution)
    
    j=cmath.sqrt(-1)
    
    
    numbers=[]
    for x in np.linspace(lowX,highX,width):
        for y in np.linspace(lowY, highY,height):
            numbers.append((x+y*j, iterations))
    
    output = []
    with Pool() as p:
        output = p.map(bounded, numbers)
    
        
    return output


class mode(Enum):
    centre = 1
    zoom = 2
    outer_rect = 3
    quality = 4

if __name__ == '__main__':
    
    
    
    magnification = 200
    
    centreX = 0
    centreY = 1
    
    radiusX = 1.5
    radiusY = 1
    
    quality = 50
    
    lowX = centreX - radiusX
    highX= centreX + radiusX

    lowY =centreY - radiusY
    highY=centreY + radiusY
    
    width = int(abs(lowX - highX) * magnification)
    height = int(abs(lowY - highY) * magnification)
    
    pygame.init()
    screen = pygame.display.set_mode([width, height], pygame.RESIZABLE)
    running = True
    
    
    
    mode = mode.centre
    while running:
        print(f"{centreX},{centreY} z:{magnification}")
        screen.fill((0,0,0))
        lowX = centreX - radiusX
        highX= centreX + radiusX
    
        lowY =centreY - radiusY
        highY=centreY + radiusY
        
        width = int(abs(lowX - highX) * magnification)
        height = int(abs(lowY - highY) * magnification)
        
        
        output = render(lowX,highX,lowY,highY,magnification,quality)
        for i in range(len(output)):
            x, y, loops = output[i]
            x=-int((x-lowX)*(width)/(lowX-highX))
            
            y=int((y-lowY)*(height)/(lowY-highY))+height
            
            r=loops
            if r>255:
                r=255
            g=loops-255
            if g<0:
                g=0
            b=int((512 - loops)/2)
            
            
            pygame.draw.circle(screen, (r, g, b), (x, y), 1)
        pygame.display.flip()
        print(screen.get_size())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                pressed = pygame.key.name(event.key)
                print(pressed)
                if pressed == 'z':
                    mode=mode.zoom
                elif pressed == 'c':
                    mode=mode.centre
                elif pressed == 'r':
                    mode=mode.outer_rect
                elif pressed == 'q':
                    mode=mode.quality
                else:
                    if pressed == 'right':
                        if mode == mode.centre:
                            centreX = centreX - (0.1*radiusX)
                        elif mode == mode.outer_rect:
                            radiusX = radiusX + 0.1
                            
                    if pressed =='left':
                        if mode == mode.centre:
                            centreX = centreX + (0.1*radiusX)
                        elif mode == mode.outer_rect:
                            radiusX = radiusX - 0.1
                            
                    if pressed == 'up':
                        if mode == mode.centre:
                            centreY = centreY - (0.1* radiusY)
                        elif mode == mode.outer_rect:
                            radiusY = radiusY - 0.1
                        elif mode == mode.zoom:
                            magnification = int(magnification *1.25)
                            radiusX=radiusX-(0.2*radiusX)
                            radiusY = radiusY-(0.2*radiusY)
                            
                        elif mode == mode.quality:
                            quality = quality + 10
                            
                    if pressed == 'down':
                        if mode == mode.centre:
                            centreY = centreY + (0.1*radiusY)
                        elif mode == mode.outer_rect:
                            radiusY = radiusY + 0.1
                        elif mode == mode.zoom:
                            magnification = magnification -10
                            radiusX=radiusX+(0.2*radiusX)
                            radiusY = radiusY+(0.2*radiusY)
                        elif mode == mode.quality:
                            quality = quality - 10
                            if quality < 10:
                                quality = 10
                        
                
        
    pygame.quit()
    
        
    
