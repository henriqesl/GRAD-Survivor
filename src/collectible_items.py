from settings import *
import random
itens = [];

class ItemColetavel(pygame.sprite.Sprite):
    def __init__(self, pos, funcao, imagem):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(center=pos)
        self.funcao = funcao
        self.used = False


def drop_item(pos, imagens, grupos):
    numero = random.randint(1, 100)

    if 20 < numero <= 30:
        item = ItemColetavel(pos, 'cracha', imagens['cracha'])
    elif 10 < numero <= 20:
        item = ItemColetavel(pos, 'redbull', imagens['redbull'])
    elif 0 < numero <= 10:
        item = ItemColetavel(pos, 'subway', imagens['subway'])
    else:
        return

    for grupo in grupos:
        grupo.add(item)

def aplicar_poder(player, tipo):
    agora = pygame.time.get_ticks()
    duracao = 3000

    if tipo == 'redbull':
        player.power_timers['speed'] = agora + duracao
        print("Velocidade aumentada por 3s!")

    elif tipo == 'cracha':
        player.power_timers['intangivel'] = agora + duracao
        print("Intangibilidade ativada por 3s!")
    
    elif tipo == 'subway':
        if player.lives < player.max_lives:
            player.lives += 1
            print("Vida aumentada em +1!")
        else:
            print("Vida já está no máximo!")

            