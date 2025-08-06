from Settings import *
import random
itens = [];

class ItemColetavel(pygame.sprite.Sprite):
    def __init__(self, pos, funcao, imagem):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(center=pos)
        self.funcao = funcao
        self.used = False


def drop_item(pos, imagens, grupo_itens):
    numero = random.randint(1, 100)
    if 0 < numero <= 25:
        item = ItemColetavel(pos, 'cracha', imagens['cracha'])
    elif 25 < numero <= 50:
        item = ItemColetavel(pos, 'redbull', imagens['redbull'])
    elif 50 < numero <= 75:
        item = ItemColetavel(pos, 'subway', imagens['subway'])
    else:
        return  
    grupo_itens.add(item)

def aplicar_poder(player, tipo):
    agora = pygame.time.get_ticks()
    duracao = 3000  # 3 segundos em ms

    if tipo == 'redbull':
        player.power_timers['speed'] = agora + duracao
        print("Velocidade aumentada por 3s!")

    elif tipo == 'cracha':
        player.power_timers['intangivel'] = agora + duracao
        print("Intangibilidade ativada por 3s!")

            