from abc import ABC, abstractmethod
import pygame
from Biblioteca import Projetil as Pj # IMPORTA A CLASSE PROJETIL
from Biblioteca import Animacao as Am #Importa a classe animacao
from Biblioteca import saveLoadManager as Slm

ALTURA_TELA = 600
COMPRIMENTO_TELA = 800
INTERVALO_DISPARO = 3000 # 1.5 segundos

def verifica_colisao(self, outro):
        hitbox_self = pygame.Rect(self._pos_x, self._pos_y, self._tam_x, self._tam_y)
        hitbox_outro = pygame.Rect(outro._pos_x, outro._pos_y, outro._tam_x, outro._tam_y)
        return hitbox_self.colliderect(hitbox_outro)

class Personagens():
    def __init__(self, id_character,  name_character, pos_x, pos_y, vida, tam_x, tam_y, sprite):
        self._id_character= id_character #id de identificação do personagem
        self._name_character= name_character #nome do personagem
        self._pos_x = pos_x #posicao no eixo X do personagem em relação ao mapa
        self._pos_y= pos_y #posicao no eixo Y do personagem em relação ao mapa
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

    
class Player(Personagens, pygame.sprite.Sprite):
    def __init__ (self, name_character, id_character, sprite, pos_x, pos_y, tam_x, tam_y, speed_x, speed_y):
        super().__init__(name_character, id_character,  sprite, pos_x, pos_y, tam_x, tam_y,)
        #criando imagem do player
        self.animacao = Am.Animacao(sprite, "pooh_idle_sprites", 100)
        self.image = self.animacao.pega_sprite_atual()
        self.rect = self.image.get_rect()
        #fim
        self._speed_x = speed_x
        #variaveis para fisica
        self._speed_y = speed_y #velocidade de movimento do personagem
        self._no_chao = False #variável para definir o contato do poo com o chão
        self.gravidade = 0.8
        self.speed_jump = -18
        self.vida = 3

        #fim
        self.invincible = False
        self.invinciblity_duration = 1500 # duração em milissegundos(1.5s)
        self.hurt_time = 0
        self.knockback_strength = 40

    def fazer_animacao(self, tipo):
        self.animacao.definir_estado(tipo)

    def movimento(self, plataforms_group):
        animacao = "pooh_idle_sprites"
        tecla = pygame.key.get_pressed()

        if tecla[pygame.K_a]:
            self._pos_x -= self._speed_x
            animacao = "pooh_movimento_E_sprites"

        if tecla[pygame.K_d]:
            self._pos_x += self._speed_x
            animacao = "pooh_movimento_D_sprites"

        if tecla[pygame.K_w] and self._no_chao:
            self._speed_y = self.speed_jump
            self._no_chao = False 

        self._speed_y += self.gravidade
        self._pos_y += self._speed_y

        if self._pos_y >= 440:  #definir posteriormente onde vai ser o chão 
            self._pos_y = 440
            self._speed_y = 0
            self._no_chao = True 

        self.fazer_animacao(animacao)

        # Detecção com Plataformas:
        # Verifique se o jogador está caindo (velocidade positiva)
        if self._speed_y > 0:
            # A função retorna uma lista de plataformas com as quais colidimos
            hits = pygame.sprite.spritecollide(self, plataforms_group, False)
            if hits:
                # Se colidiu, pega a primeira plataforma da lista (hits[0])
                # e ajusta a posição do jogador para ficar em cima dela.
                self.rect.bottom = hits[0].rect.top
                self._speed_y = 0
                self._no_chao = True
        if self.invincible:
            current_time = pygame.time.get_ticks()
            self.image.set_alpha(100 if (current_time // 100) % 2 == 0 else 255) # efeito de piscar

            if current_time - self.hurt_time > self.invinciblity_duration:
                self.invincible = False
                self.image.set_alpha(255) # garante que o player volte normal 


class Inimigo(Personagens):
    def __init__(self, name_character,  id_character, sprite, pos_x, pos_y, vida, tam_x, tam_y):
        super().__init__( name_character, id_character, sprite, pos_x, pos_y, vida, tam_x, tam_y,)
        self.inimigo_ativo= True
        self.lim_sup = 400
        self.lim_inf = 100
        self.dir = 1 #supoe-se que a abelha ja nasce no ar

        if self._id_character ==2:
            self.animacao = Am.Animacao(sprite, "abelha_idle_sprites", 100)
            self.speed_x = 0
            self.speed_y = 2

        elif self._id_character == 3:
            self.animacao = Am.Animacao(sprite, "urso_idle_sprites", 100)
            self.speed_x = 2
            self.speed_y = 0

        elif self._id_character == 4:
            self.animacao = Am.Animacao(sprite, "boss_idle_sprites", 100)
            #definir o movimento x e y do boss
        
        self.image = self.animacao.pega_sprite_atual()
        self.rect = self.image.get_rect()
        self.rect.x = tam_x
        self.rect.y = tam_y

    def fazer_animacao(self, tipo):
        self.animacao.definir_estado(tipo)

    def movimento(self):
         # Movimento Horizontal para o Urso
        if self._id_character == 2:
            self.rect.x += self.speed_x
            animacao = "urso_movimento_D_sprites"

            # Inverte a direção se atingir as bordas da tela
            if self.rect.right > 840 or self.rect.left < 0:
                self.speed_x *= -1
                animacao = "urso_movimento_E_sprites"
        
        # Movimento Vertical para a Abelha
        elif self._id_character == 3:
            self.rect.y += self.speed_y
            animacao = "abelha_idle_sprites"
            # Inverte a direção se atingir o topo ou a base da área de jogo
            if self.rect.bottom > 440 or self.rect.top < 0: # 440 é o nosso chão
                self.speed_y *= -1

        elif self._id_character ==4:
            #terminar a parte do boss
            pass
        self.fazer_animacao(animacao)
    
    def dispara_projetil(self, outro, sprite_projetil):
        velocidade = 10   # definir posteriormente
        direcao = -1 if self._pos_x > outro._pos_x else 1
        distancia_disparo = 10 #distancia minima para o inimigo atirar contra poo
                               #definir posteriormente
        proj_ativo =True    
        largura_proj = 5 # definir posteriormente
        altura_proj = 2  # definir posteriormente
        sprite_proj = sprite_projetil
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

class Plataform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h): #dimensões e posição
        super().__init__()
        self.image = pygame.Surface([w,h]) #criando a plataforma
        self.image.fill([139, 69, 19])# as cores dela
        #criando o hitbox dela:
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Honey(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill([255, 215, 0])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
