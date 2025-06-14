from abc import ABC, abstractmethod
import pygame
from Biblioteca import Projetil as Pj # IMPORTA A CLASSE PROJETIL
from Biblioteca import Animacao as Am #Importa a classe animacao
from Biblioteca import saveLoadManager as Slm

ALTURA_TELA = 600
COMPRIMENTO_TELA = 800
GRAVIDADE = 1
INTERVALO_DISPARO = 3000 # 1.5 segundos

class Personagens():
    def __init__(self, id_character,  name_character, pos_x, pos_y, vida, tam_x, tam_y, sprite):
        self._id_character= id_character #id de identificação do personagem
        self._name_character= name_character #nome do personagem
        self._pos_x = pos_x #posicao no eixo X do personagem em relação ao mapa
        self._pos_y= pos_y #posicao no eixo Y do personagem em relação ao mapa
        self._vida = vida #contador de vida do personagem
        self._tam_x = tam_x #altura do personagem
        self._tam_y = tam_y # largura do personagem
        self._sprite = sprite

        #ID DE PERSONAGEM
        #0 = POOH
        #1 = NPC
        #2 = ABELHA
        #3 = URSO
        #4 = BOSS

    @abstractmethod
    def fazer_animacao(self, tipo):
        #será utilizado a variavel "self.id_character" para identificar qual personagem 
        # e a variavel tipo para identificar o tipo da animação
        pass

    @abstractmethod
    def verifica_colisao(self, outro):
        #verifica se a posição do objeto self coincide com a do objeto outro. Assim permitindo intereção do POOH com NPC, além do ataque 
        # e hit de projeteis inimigos. Utiliza a variavel "outro" para identificar como calcular a colisão
        pass

    @abstractmethod
    def movimento(self):
        # possui implementações diferenes para cada personagem.
        # Inimigo possui implimentação de forma randômica ou a vir pra cima do personagem (a definir)
        # Player possui movimentação baseada nas entradas do teclado
        pass

class Npc(Personagens):
    def __init__(self,  name_character, id_character, sprite, pos_x, pos_y, vida, tam_x, tam_y,):
        super().__init__(  name_character, id_character, sprite, pos_x, pos_y, vida, tam_x, tam_y)
        self.animacao = Am.Animacao(sprite,"npc_idle_sprites", 100)

    def comentario(self):
        text_box = "Cuidado com as abelhas" #frase dita pelo npc ao haver colisão com o personagem principal
        print(text_box) #ainda definir como fazer isto aparecer na tela e não no terminal


    def fazer_animacao(self, tipo):
        self.animacao.definir_estado(tipo)

    
class Player(Personagens):
    def __init__ (self, id_game, name_character, id_character, sprite, pos_x, pos_y, vida, tam_x, tam_y, speed_x, speed_y, amount_honey_coletada,):
        super().__init__(id_game, id_character, name_character, pos_x, pos_y, vida, tam_x, tam_y, sprite)
        self._amount_honey_coletada = amount_honey_coletada #quantidade de mel coletada pelo personagem
        self._speed_x = speed_x
        self._speed_y = speed_y #velocidade de movimento do personagem
        self._no_chao = True #variável para definir o contato do poo com o chão
        self.animacao = Am.Animacao(sprite, "pooh_idle_sprites", 100)
        self.speed_jump = -15


    def fazer_animacao(self, tipo):
        self.animacao.definir_estado(tipo)

    def movimento(self):
        animacao = "pooh_idle_sprites"
        tecla = pygame.key.get_pressed()

        if tecla[pygame.K_LEFT]:
            self._pos_x -= self._speed_x
            animacao = "pooh_movimento_E_sprites"
        elif tecla[pygame.K_RIGHT]:
            self._pos_x += self._speed_x
            animacao = "pooh_movimento_D_sprites"
        elif tecla[pygame.K_UP] and self._no_chao:
            self._speed_y = self.speed_jump
            self._no_chao = False 
            animacao = "pooh_movimento_U_sprites"

        self._speed_y += GRAVIDADE
        self._pos_y += self._speed_y

        if self._pos_y >= 401:  #definir posteriormente onde vai ser o chão 
            self._pos_y = 400
            self._speed_y = 0
            self._no_chao = True 

        self.fazer_animacao(animacao)

class Inimigo(Personagens):
    def __init__(self, id_game, name_character,  id_character, sprite, pos_x, pos_y, vida, tam_x, tam_y, speed):
        super().__init__(id_game, id_character,  name_character, pos_x, pos_y, vida, tam_x, tam_y, sprite)
        self.inimigo_ativo= True
        self.speed= speed
        self.lim_sup = 400
        self.lim_inf = 100
        self.dir = 1 #supoe-se que a abelha ja nasce no ar

        if self._id_character ==1:
            self.animacao = Am.Animacao(sprite, "abelha_idle_sprites", 100)
        elif self._id_character == 3:
            self.animacao = Am.Animacao(sprite, "inimigo_idle_sprites", 100)
        self.lim_sup = 400 #definir posteriormente
        self.lim_inf = 100 #definir posteriormente


    def movimento(self):
        self._pos_y += self.speed * self.dir
        if self._pos_y <= self.lim_sup:
            self._pos_y = self.lim_sup # Garante que não passe do limite
            self.dir = 1 # Muda para baixo
        elif self._pos_y >= self.lim_inf:
            self._pos_y = self.lim_inf # Garante que não passe do limite
            self.dir = -1 # Muda para cima 
        if self._id_character == 1:
            self.fazer_animacao("abelha_idle_sprites")
        else:
            self.fazer_animacao("boss_idle_sprites")
                

    def fazer_animacao(self, tipo):
        self.animacao.definir_estado(tipo)

    
    def dispara_projetil(self, outro):
        velocidade = 10   # definir posteriormente
        direcao = -1 if self._pos_x > outro._pos_x else 1
        distancia_disparo = 10 #distancia minima para o inimigo atirar contra poo
                               #definir posteriormente
        proj_ativo =True    
        largura_proj = 5 # definir posteriormente
        altura_proj = 2  # definir posteriormente
        sprite_proj = Am.pega_sprite_na_pasta("Assets/Projetil")
        if abs(self._pos_x - outro._pos_x) <= distancia_disparo :
                projetil = Pj(
                    velocidade_projetil= velocidade,
                    pos_x_projetil=self._pos_x, #por estar na classe inimigo, o puxam-se os dados de posicao e assim o ferrao parte da posicao do inimigo
                    pos_y_projetil=self._pos_y, #por estar na classe inimigo, o puxam-se os dados de posicao e assim o ferrao parte da posicao do inimigo
                    direcao= direcao,
                    ativo = proj_ativo,
                    largura_proj = largura_proj,
                    altura_proj = altura_proj,
                    sprite = sprite_proj
        )
        return projetil

def verifica_colisao(self, outro):
        hitbox_self = pygame.Rect(self._pos_x, self._pos_y, self._tam_x, self._tam_y)
        hitbox_outro = pygame.Rect(outro._pos_x, outro._pos_y, outro._tam_x, outro._tam_y)
        return hitbox_self.colliderect(hitbox_outro)
