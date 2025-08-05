import pygame as pg
import random
itens = [];

class Item_Coletavel:
    def __init__(self, funcao, imagens):
        self.funcao = funcao
        self.imagem = imagens.get()
        #self.pos = 
        self.used = False

        
    def drop_item():
        numero_aleatorio = random.randint(1, 100)
        #if 0 < numero_aleatorio <= 25:
            #itens.append(Item_Coletavel(inimigo.x, inimigo.y, cracha_image))
        #elif 25 < numero_aleatorio <= 50:
            #itens.append(Item_Coletavel(inimigo.x, inimigo.y, redbull_image))
        #elif 50 < numero_aleatorio <= 75 :
            #itens.append(Item_Coletavel(inimigo.x, inimigo.y, subway_image))


            