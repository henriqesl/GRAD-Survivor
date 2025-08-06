import pygame
import sys

pygame.init()
pygame.display.set_caption("GRAD-Survivor")
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
map = pygame.image.load('assets/images/mapa1.0.png')

#class obstaculos:
#    def obstasculo(X,Y,L,H):
#        return pygame.Rect(map,)


#Definindo os retângulos de contato

#Paredes
parede1 =  pygame.Rect((0,0,4,600)) #(X, Y, L, H)
parede2 = pygame.Rect((796,0,4,600))
parede3 = pygame.Rect((0,0,800,4))
parede4 = pygame.Rect((0, 595, 800,4))

#Portas
porta1 = pygame.Rect((0, 56, 57,3))
macaneta1 = pygame.Rect((40,51,12,5))

porta2 = pygame.Rect((743,53,53,3))
macaneta2 = pygame.Rect((746, 48, 12, 5))

porta3 = pygame.Rect((0, 493, 55,3))
macaneta3 = pygame.Rect((40,488,12,5))

porta4 = pygame.Rect((744, 492, 55,3))
macaneta4 = pygame.Rect((747,487,12,5))

#Mesas
mesa1 = pygame.Rect((0,370,185,80))
mesa2 = pygame.Rect((0,173,185,80))
mesa3 = pygame.Rect((620,169,185,80))
mesa4 = pygame.Rect((620,375,185,80))
mesa5 = pygame.Rect((464,33,88,52))

#Tv inútil do grad
tv = pygame.Rect((308,4,185,4))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.blit(map, (0,0))
    pygame.display.flip()
