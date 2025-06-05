import pygame
import os

class Animacao:
    def __init__(self, sprites_info, estado_atual, velocidade_animacao):
        self.sprites_info = sprites_info
        self.velocidade_animacao = velocidade_animacao
        self.estado_atual = estado_atual
        self.contador_sprite_atual = 0
        self.frame_freq = 0.0 # usado para controlar o tempo entre frames

    def definir_estado(self, novo_estado):
        if novo_estado != self.estado_atual:
            self.estado_atual = novo_estado
            self.contador_sprite_atual = 0  # reinicia a animação para o novo estado
            self.frame_freq = 0
        else:
            return 
        
    def atualiza(self, dt):
        self.frame_freq += dt
        if self.frame_freq >= self.velocidade_animacao:
            self.frame_freq -= self.velocidade_animacao # subtrai para manter o excesso de tempo
            if self.estado_atual:
                self.contador_sprite_atual = (self.contador_sprite_atual + 1) % len(self.estado_atual)

            else:
                self.contador_sprite_atual = 0 # reinicia para 0 se a lista estiver vazia

    def pega_sprite_atual(self):
        sprites = self.sprites_info.get(self.estado_atual, [])
        if sprites and 0 <= self.contador_sprite_atual < len(sprites):
            return sprites[self.contador_sprite_atual]
        else:
            print(f"[ERRO] Sprite inválido: estado={self.estado_atual}, contador={self.contador_sprite_atual}")
            return pygame.Surface((1, 1), pygame.SRCALPHA)

def pega_sprite_na_pasta(pasta):
    sprites = []
    if not os.path.exists(pasta):
        print(f"pasta de sprites não encontrada: {pasta}")
        return []

    for nome_arquivo in sorted(os.listdir(pasta)):
        if nome_arquivo.endswith(".png"): #ou sla qual formato o vilches vai usar pras sprites. Definir posteriomente
            img_path = os.path.join(pasta, nome_arquivo)
            img = pygame.image.load(img_path).convert_alpha()
            sprites.append(img)
    return sprites
