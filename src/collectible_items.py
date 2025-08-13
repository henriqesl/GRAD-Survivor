from .settings import *
import random
from . import game_data
itens = [];

class ItemColetavel(pygame.sprite.Sprite):
    def __init__(self, pos, funcao, imagem):
        super().__init__()
        self.image = imagem
        self.rect = self.image.get_rect(center=pos)
        self.funcao = funcao
        self.used = False


def drop_item(pos, imagens, grupos):
    # Itera sobre cada item definido em ITEM_DATA
    for nome_item, dados_item in game_data.ITEM_DATA.items():
        # Rola um dado de 1 a 100 e verifica se é menor que a chance de drop
        if random.randint(1, 100) <= dados_item['drop_chance']:
            item = ItemColetavel(pos, nome_item, imagens[nome_item])
            for grupo in grupos:
                grupo.add(item)
            return # Retorna após dropar um item para não dropar vários de uma vez

def aplicar_poder(player, tipo):
    agora = pygame.time.get_ticks()
    
    # Busca os dados do item específico no game_data
    item_info = game_data.ITEM_DATA.get(tipo)

    # Se o item não for encontrado nos dados, não faz nada
    if not item_info:
        return

    if tipo == 'redbull':
        # Pega a duração; se não existir, não ativa o poder temporal
        duracao = item_info.get('duration')
        if duracao:
            player.power_timers['speed'] = agora + duracao
            print(f"Velocidade aumentada por {duracao / 1000}s!")

    elif tipo == 'cracha':
        # Pega a duração; se não existir, não ativa o poder temporal
        duracao = item_info.get('duration')
        if duracao:
            player.power_timers['intangivel'] = agora + duracao
            print(f"Intangibilidade ativada por {duracao / 1000}s!")
    
    elif tipo == 'subway':
        # Este item não tem duração, o efeito é instantâneo
        if player.lives < player.max_lives:
            player.lives += 1
            print("Vida aumentada em +1!")
        else:
            print("Vida já está no máximo!")