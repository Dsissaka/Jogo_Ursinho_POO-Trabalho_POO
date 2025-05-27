import pygame
import os

class Animador:
    def __init__(self, sprites_info, estado_padrao="idle", velocidade_animacao=100):
        self.sprites_info = sprites_info
        self.velocidade_animacao = velocidade_animacao
        self.estado_atual = estado_padrao
        self.current_frame_index = 0
        self.frame_freq = 0.0 # usado para controlar o tempo entre frames

    def definir_estado(self, novo_estado):
        if novo_estado != self.estado_atual:
            self.estado_atual = novo_estado
            self.contador_sprite = 0  # reinicia a animação para o novo estado
            self.frame_freq = 0.0 
    def atualiza(self, dt):
        self.frame_freq += dt
        if self.frame_freq >= self.velocidade_animacao:
            self.frame_freq -= self.velocidade_animacao # subtrai para manter o excesso de tempo
            if self.sprites_info[self.estado_atual]:
                self.contador_sprite = (self.contador_sprite + 1) % len(self.sprites_info[self.estado_atual])
            else:
                self.contador_sprite = 0 # reinicia para 0 se a lista estiver vazia

    def pega_sprite_atual(self):
            return self.sprites_info[self.estado_atual][self.contador_sprite]


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
