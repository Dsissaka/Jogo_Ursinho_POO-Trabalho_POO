from abc import ABC, abstractmethod
import pygame
from Biblioteca import Projetil as Pj # IMPORTA A CLASSE PROJETIL
from Biblioteca import Animacao as Am #Importa a classe animacao
from Biblioteca import saveLoadManager as Slm
from Biblioteca import Prepara_jogo as Pg

ALTURA_TELA = 600
COMPRIMENTO_TELA = 800
INTERVALO_DISPARO = 3000 # 1.5 segundos


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
    def __init__(self, x, y, sprite):
        super().__init__()
        self.animacao = Am.Animacao(sprite, "honey_sprites", 100)
        self.image = self.animacao.pega_sprite_atual()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        self.image = self.animacao.pega_sprite_atual()

class Personagens(pygame.sprite.Sprite, ABC):
    def __init__(self, id_character,  name_character,  sprite, pos_x, pos_y, tam_x, tam_y):
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

    def verifica_colisao(self, outro):
        hitbox_self = pygame.Rect(self._pos_x, self._pos_y, self._tam_x, self._tam_y)
        hitbox_outro = pygame.Rect(outro._pos_x, outro._pos_y, outro._tam_x, outro._tam_y)
        return hitbox_self.colliderect(hitbox_outro)


    @abstractmethod
    def movimento(self):
        # possui implementações diferenes para cada personagem.
        # Inimigo possui implimentação de forma randômica ou a vir pra cima do personagem (a definir)
        # Player possui movimentação baseada nas entradas do teclado
        pass

class Npc(Personagens):
    def __init__(self,  id_character, name_character, sprite, pos_x, pos_y, tam_x, tam_y,):
        super().__init__( id_character,  name_character, sprite, pos_x, pos_y, tam_x, tam_y)
        self.animacao = Am.Animacao(sprite,"npc_idle_sprites", 100)

    def comentario(self, surface):
        fonte = pygame.font.Font(None, 24)
        texto = fonte.render("Cuidado com as abelhas!", True, (255, 255, 255))
        surface.blit(texto, (self._pos_x, self._pos_y - 30))


    def fazer_animacao(self, tipo):
        self.animacao.definir_estado(tipo)

class Player(Personagens):
    def __init__ (self, id_character, name_character,  sprite, pos_x, pos_y, tam_x, tam_y, speed_x, speed_y):
        super().__init__(id_character, name_character,   sprite, pos_x, pos_y, tam_x, tam_y,)
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

    def update(self, plataforms_group):
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
        self.rect.x = self._pos_x
        self.rect.y = self._pos_y


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
    def __init__(self, id_character, name_character,  sprite, pos_x, pos_y, vida, tam_x, tam_y):
        super().__init__( id_character, name_character, sprite, pos_x, pos_y, vida, tam_x, tam_y,)
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
        self.rect.x = self._pos_x
        self.rect.y = self._pos_y

    def fazer_animacao(self, tipo):
        self.animacao.definir_estado(tipo)

    def update(self):
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
    


pygame.init()

# criando uma fonte para o placar
game_font = pygame.font.Font(None, 36) # fonte padrão, tam.36
display = pygame.display.set_mode([COMPRIMENTO_TELA, ALTURA_TELA])
pygame.display.set_caption('Ursinho POO')
clock = pygame.time.Clock()
# --- Criação dos Objetos e Grupos ---
Game = Pg.Jogo(1)
sprite_inimigo_urso, sprite_poo, sprite_leitao, sprite_honey, sprite_boss, sprite_inimigo_abelha, sprite_mapa, sprite_projetil = Game.load_sprites_geral()
ground_rect = pygame.Rect(0, 440, 840, 40)
all_sprites = pygame.sprite.Group(); plataforms_group = pygame.sprite.Group()
honey_group = pygame.sprite.Group(); enemies_group = pygame.sprite.Group()
honey_score = 0; player = Player(
    id_character=0,
    name_character="Pooh",
    sprite=sprite_poo,
    pos_x=100,
    pos_y=300,
    tam_x=40,
    tam_y=60,
    speed_x=5,
    speed_y=0
); all_sprites.add(player)

# Cria o urso
enemy1 = Inimigo(
        id_character= 3,
        name_character= "Urso",
        sprite = sprite_inimigo_urso,
        pos_x= 300,
        pos_y= 390,
        vida=10, #adaptar posteriormente
        tam_x=35,
        tam_y= 50)
all_sprites.add(enemy1); enemies_group.add(enemy1)

# Cria a abelha
bee1 = Inimigo(
        id_character= 2,
        name_character= "Abelha",
        sprite = sprite_inimigo_abelha,
        pos_x= 300,
        pos_y= 390,
        vida=10, #adaptar posteriormente
        tam_x=30,
        tam_y= 25)
all_sprites.add(bee1); enemies_group.add(bee1)

leitao = Npc(
        id_character= 2,
        name_character= "Leitao",
        sprite = sprite_leitao,
        pos_x= 50,    #definir quando o mapa ficar pronto
        pos_y= 100,    #definir quando o mapa ficar pronto
        vida = 9999,    #npc não morre
        tam_x= 30,    #definir conforme a sprite
        tam_y= 20,    #definir conforme a sprite
    )
all_sprites.add(leitao)

for data in [[200, 350, 150, 20], [450, 280, 200, 20], [150, 180, 100, 20]]:
    plat = Plataform(*data); all_sprites.add(plat); plataforms_group.add(plat)
total_honey = len([[250, 325], [500, 255], [180, 155]])
for data in [[250, 325], [500, 255], [180, 155]]:
    honey = Honey(*data); all_sprites.add(honey); honey_group.add(honey)


# Criando as plataformas:
plat1 = Plataform(x=200, y=350, w=150, h=20)
plat2 = Plataform(x=450, y=280, w=200, h=20)
plat3 = Plataform(x=150, y=180, w=100, h=20)

# Adicionando as plataformas aos grupos
all_sprites.add(plat1, plat2, plat3)
plataforms_group.add(plat1, plat2, plat3)

#criando alguns potes de mel
honey1 = Honey(250, 325, sprite_honey) # Em cima da plat1
honey2 = Honey(500, 255, sprite_honey) # Em cima da plat2
honey3 = Honey(180, 155, sprite_honey) # Em cima da plat3

all_sprites.add(honey1, honey2, honey3)
honey_group.add(honey1, honey2, honey3)

honey_score = 0 # variável para contar o mel

# --- Loop Principal ---
gameLoop = True
if __name__ == '__main__':
    while gameLoop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameLoop = False
        
        # --- Lógica ---
        # o .update() chama a função update de TODOS os sprites no grupo
        all_sprites.update(plataforms_group)

        honey_collected = pygame.sprite.spritecollide(player, honey_group, True)# O 'True' no final faz com que o mel atingido seja removido de todos os grupos
        if honey_collected:
            print("Mel coletado!")# No futuro, aqui aumentaremos um placar
            honey_score += 1 #incrementaçao do mel
        if not player.invincible:
             enemy_hits = pygame.sprite.spritecollide(player, enemies_group, False)# verifica a colisão do player com o inimigo, o False serve para que o inimigo nao suma depois
             if enemy_hits:
                player.invincible = True
                player.hurt_time = pygame.time.get_ticks()
                player.vida -= 1
                print(f'Atingido! vidas restanntes:{player.vida}')
                enemy = enemy_hits[0]
                if player.rect.centerx < enemy.rect.centerx: player.rect.x -= player.knockback_strength
                else: player.rect.x += player.knockback_strength
                player._speed_y = -8 # Impulso para cima

        # verificação de GAME OVERdd
        if player.vida <= 0:
            print('GAME OVER!')
            gameLoop = False # Jogo encerra


        # --- Desenho ---
        display.fill((93, 226, 231))
        pygame.draw.rect(display, (34, 139, 34), ground_rect) # Desenha o chão verde
        # o .draw() desenha TODOS os sprites do grupo na tela
        all_sprites.draw(display)
        
        health_text = game_font.render(f'Vida:{player.vida}', True, (255,255,255))
        display.blit(health_text, (10,10)) # posicao no canto superior esquerdo

        honey_text = game_font.render(f'Mel: {honey_score}', True,(255,255,255))
        display.blit(honey_text, (10,40))

        if player.verifica_colisao(leitao):
            leitao.comentario(display)



        pygame.display.update()
        clock.tick(60)

pygame.quit()
