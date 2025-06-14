import pygame as py
from Biblioteca import Animacao as Am #Importa a classe animacao

class Jogo():
    def __init__(self, id_game):
        self._id_game = id_game # pode ser usado para recuperar logs de sessões passadas
                                #podemos usar escrita em arquivos para isso

    #inicio da parte de declaração e preenchimento de sprites    
    def load_sprites_geral(self):
            
            sprite_inimigo_urso = {
            "urso_movimento_D_sprites": Am.pega_sprite_na_pasta("Assets/Urso/Direita"),
            "urso_movimento_E_sprites": Am.pega_sprite_na_pasta("Assets/Urso/Esquerda")
            }

            sprite_poo = {
            "pooh_idle_sprites": Am.pega_sprite_na_pasta("Assets/Poo/Idle"),
            "pooh_movimento_D_sprites": Am.pega_sprite_na_pasta("Assets/Poo/Direita"),
            "pooh_movimento_E_sprites": Am.pega_sprite_na_pasta("Assets/Poo/Esquerda"),
            "pooh_morte_poo": Am.pega_sprite_na_pasta("Assets/Poo/Morte")
            }

            sprite_leitao = {
            "npc_idle_sprites": Am.pega_sprite_na_pasta("Assets/Npc")
            }

            sprite_honey = {
                 "honey_sprites": Am.pega_sprite_na_pasta("Assets/Honey")
            }

            sprite_boss = {
            "boss_idle_sprites": Am.pega_sprite_na_pasta("Assets/Boss")
            }

            sprite_inimigo_abelha = {
            "abelha_idle_sprites": Am.pega_sprite_na_pasta("Assets/Abelha/idle"),
            }

            
            sprite_mapa= {
            "mapa_original_sprite": Am.pega_sprite_na_pasta("Assets/Mapas/Mapa_original"),
            "mapa_boss_sprites": Am.pega_sprite_na_pasta("")
            }

            sprite_projetil = {
            "projetil": Am.pega_sprite_na_pasta("Assets/Ferrao")
            }
            return  sprite_inimigo_urso, sprite_poo,  sprite_leitao, sprite_honey,  sprite_mapa, sprite_projetil, sprite_boss, sprite_inimigo_abelha
    #fim da parte de declaração e preenchimento de sprites

#jogar o codigo para chamada do gerenciamento de save aqui 
