from abc import ABC, abstractmethod
import pygame
from Biblioteca import Projetil as Pj # IMPORTA A CLASSE PROJETIL
from Biblioteca import Animacao as Am #Importa a classe animacao
from Biblioteca import saveLoadManager as Slm
from Biblioteca import Prepara_jogo as Pg

ALTURA_TELA = 480
COMPRIMENTO_TELA = 840
INTERVALO_DISPARO = 1000 # 1.5 segundos


class Plataform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h): #dimensões e posição
        super().__init__()
        self.image = pygame.Surface([w,h]) #criando a plataforma
        self.image.fill([139, 69, 19])# as cores dela
        #criando o hitbox dela:
        self.rect = self.image.get_rect(x=x,y=y)

class Honey(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite):
        super().__init__()
        self.animacao = Am.Animacao(sprite, "honey_sprites", 100)
        self.image = self.animacao.pega_sprite_atual()
        self.rect = self.image.get_rect(x=x,y=y)
 
    def update(self, dt):
        #a
        pass

class Personagens(pygame.sprite.Sprite, ABC):
    def __init__(self, id_character,  name_character,  sprite, pos_x, pos_y, tam_x, tam_y):
        super().__init__()
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
    def update(self, dt):
        # possui implementações diferenes para cada personagem.
        # Inimigo possui implimentação de forma randômica ou a vir pra cima do personagem (a definir)
        # Player possui movimentação baseada nas entradas do teclado
        pass

class Npc(Personagens):
    def __init__(self,  id_character, name_character, sprite, pos_x, pos_y, tam_x, tam_y,):
        super().__init__( id_character,  name_character, sprite, pos_x, pos_y, tam_x, tam_y)
        self.animacao = Am.Animacao(sprite,"npc_idle_sprites", 100)
        self.image = self.animacao.pega_sprite_atual()
        self.rect = self.image.get_rect()

    def comentario(self, surface):
        fonte = pygame.font.Font(None, 24)
        texto = fonte.render("Cuidado com as abelhas!", True, (255, 255, 255))
        surface.blit(texto, (self._pos_x, self._pos_y - 30))


    def fazer_animacao(self, tipo):
        self.animacao.definir_estado(tipo)

    def update(self, dt):
        self.animacao.atualiza(dt)
        self.image = self.animacao.pega_sprite_atual()

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
        self.gravidade = 0.5
        self.forca_pulo = -14
        self.vida = 3
        #fim

        self.invincible = False
        self.invinciblity_duration = 1500 # duração em milissegundos(1.5s)
        self.hurt_time = 0
        self.knockback_strength = 20

    def fazer_animacao(self, tipo):
        self.animacao.definir_estado(tipo)

    def update(self, plataforms_group, level_width, jump_sound, dt):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            self.image.set_alpha(128 if (current_time // 100) % 2 == 0 else 255) # efeito de piscar

            if current_time - self.hurt_time > self.invinciblity_duration:
                self.invincible = False
                self.image.set_alpha(255) # garante que o player volte normal 
        
        animacao = "pooh_idle_sprites"
        tecla = pygame.key.get_pressed()
        if not self.invincible:
            if tecla[pygame.K_a]:
                self._pos_x -= self._speed_x
                animacao = "pooh_movimento_E_sprites"

            elif tecla[pygame.K_d]:
                self._pos_x += self._speed_x
                animacao = "pooh_movimento_D_sprites"

            if tecla[pygame.K_w] and self._no_chao:
                self._speed_y = self.forca_pulo
                self._no_chao = False 
                jump_sound.play()

        self._speed_y += self.gravidade
        self._pos_y += self._speed_y
        self._no_chao = False

        if self._pos_y >= 440:  #definir posteriormente onde vai ser o chão 
            self._pos_y = 440
            self._speed_y = 0
            self._no_chao = True 

        self.animacao.atualiza(dt)
        self.fazer_animacao(animacao)
        self.image = self.animacao.pega_sprite_atual()
        self.rect.x = self._pos_x
        self.rect.y = self._pos_y


        # Detecção com Plataformas:
        # Verifica se o jogador está caindo (velocidade positiva)
        if self._speed_y > 0:
            # A função retorna uma lista de plataformas com as quais colidimos
            hits = pygame.sprite.spritecollide(self, plataforms_group, False)
            if hits:
                # Encontra a plataforma mais alta com que colidiu
                closest_platform = hits[0]
                for hit in hits:
                    if hit.rect.top < closest_platform.rect.top:
                        closest_platform = hit
                
                # Para em cima da plataforma se os pés estiverem abaixo do topo dela
                if self.rect.bottom > closest_platform.rect.top:
                    self.rect.bottom = closest_platform.rect.top
                    self._pos_y = self.rect.y
                    self._speed_y = 0
                    self._no_chao = True
        
        # Limites do mundo para o jogador
        if self.rect.left < 0:
            self.rect.left = 0
            self._pos_x = self.rect.x
        if self.rect.right > level_width:
            self.rect.right = level_width
            self._pos_x = self.rect.x
        
class Inimigo(Personagens):
    def __init__(self, id_character, name_character,  sprite, pos_x, pos_y, tam_x, tam_y, patrol_start, patrol_end):
        super().__init__( id_character, name_character, sprite, pos_x, pos_y, tam_x, tam_y)
       
        if self._id_character ==2:
            self.animacao = Am.Animacao(sprite, "abelha_idle_sprites", 100)
            self.speed_x = 0
            self.speed_y = 2

        elif self._id_character == 3:
            self.animacao = Am.Animacao(sprite, "urso_idle_sprites", 100)
            self.speed_x = 2
            self.speed_y = 0

        
        self.image = self.animacao.pega_sprite_atual()
        self.rect = self.image.get_rect()
        self.rect.x = self._pos_x
        self.rect.y = self._pos_y
        self.patrol_start = patrol_start
        self.patrol_end = patrol_end


    def fazer_animacao(self, tipo):
        self.animacao.definir_estado(tipo)

    def update(self, dt):
         # Movimento Horizontal para o Urso
        if self._id_character == 3:
            self.rect.x += self.speed_x
            animacao = "urso_movimento_D_sprites"
            if self.rect.right > self.patrol_end or self.rect.left < self.patrol_start:
                self.speed_x *= -1
                animacao = "urso_movimento_E_sprites"
        
        # Movimento Vertical para a Abelha
        elif self._id_character == 2:
            self.rect.y += self.speed_y
            animacao = "abelha_idle_sprites"
            # Inverte a direção se atingir o topo ou a base da área de jogo
            if self.rect.bottom > 440 or self.rect.top < 0: # 440 é o nosso chão
                self.speed_y *= -1

        self.fazer_animacao(animacao)
        self.animacao.atualiza(dt)
        self._pos_x = self.rect.x 
        self._pos_y = self.rect.y

    
class Stinger(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite):
        super().__init__()
        self.animacao = Am.Animacao(sprite, "Projetil", 100)
        self.image = self.animacao.pega_sprite_atual()
        self.rect = self.image.get_rect(center=(x,y))
        self.speed_y = 7.5

    def update(self, dt):
        self.rect.y += self.speed_y
        if self.rect.top > ALTURA_TELA:
            self.kill()
        self.animacao.atualiza(dt)
        self.image = self.animacao.pega_sprite_atual()

class Boss(pygame.sprite.Sprite):
    def __init__(self,  sprite):
        super().__init__()
        self.health = 100
        self.animacao = Am.Animacao (sprite, "boss_idle_sprites", 100)
        self.image = self.animacao.pega_sprite_atual()
        self.rect = self.image.get_rect(center=(COMPRIMENTO_TELA / 2, 80))
        self.speed_x = 4
        self.last_shot_time = pygame.time.get_ticks()

    def update(self, all_sprites_group, stingers_group, dt):
        self.rect.x += self.speed_x
        if self.rect.right > COMPRIMENTO_TELA or self.rect.left < 0:
            self.speed_x *= -1

        now = pygame.time.get_ticks()
        if now - self.last_shot_time > INTERVALO_DISPARO:
            self.last_shot_time = now
            stinger = Stinger(self.rect.centerx, self.rect.bottom)
            all_sprites_group.add(stinger)
            stingers_group.add(stinger)

        self.animacao.atualiza(dt) 
        self.fazer_animacao("boss_idle_sprites") 
        self.image = self.animacao.pega_sprite_atual()
        self._pos_x = self.rect.x 
        self._pos_y = self.rect.y  

class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill((0,150,255))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_y = -12

    def update(self, dt):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()


pygame.init()
# criando uma fonte para o placar
game_font = pygame.font.Font(None, 36) # fonte padrão, tam.36
display = pygame.display.set_mode(([COMPRIMENTO_TELA, ALTURA_TELA]), pygame.FULLSCREEN)
pygame.display.set_caption('Ursinho POO')
clock = pygame.time.Clock()

#definição das musicas
level1_music_path = 'Assets/Sons/fase1.mp3'
pygame.mixer.music.load('Assets/Sons/fase1.mp3')
pygame.mixer.music.set_volume(0.4)
jump_sound = pygame.mixer.Sound('Assets/Sons/jump.wav')
collect_sound = pygame.mixer.Sound('Assets/Sons/mel.wav')
hurt_sound = pygame.mixer.Sound('Assets/Sons/hit.wav')
boss_music = 'Assets/Sons/boss.mp3'
#fim

Game = Pg.Jogo(1) #alterar esta linha ao implementar o save
sprite_inimigo_urso, sprite_poo, sprite_leitao, sprite_honey, sprite_boss, sprite_inimigo_abelha, sprite_mapa, sprite_projetil = Game.load_sprites_geral()
level_width = 3000
platform_map = [
    [0, 440, level_width, 40], [200, 350, 150, 20], [450, 280, 200, 20], 
    [700, 360, 100, 20], [900, 250, 150, 20], [1150, 180, 120, 20], 
    [1400, 300, 180, 20], [1650, 220, 100, 20], [1900, 150, 100, 20], 
    [2200, 280, 150, 20], [2500, 350, 100, 20]
]
honey_map = [
    [250, 325], [500, 255], [950, 225], [1200, 155], [1450, 275], 
    [1700, 195], [1950, 125], [2250, 255], [2550, 325], [2800, 350]
]
enemy_map = [
    # Urso 1
    [3, "Urso", sprite_inimigo_urso, 600, 440 - 50, 35, 50, 550, 800],
    # Urso 2
    [3, "Urso", sprite_inimigo_urso, 1000, 250 - 50, 35, 50, 950, 1100],
    # Urso 3
    [3, "Urso", sprite_inimigo_urso, 1500, 300 - 50, 35, 50, 1450, 1600],
    # Abelha 1
    [2, "Abelha", sprite_inimigo_abelha, 800, 200, 30, 25, 0, 0], # Note: patrol_start e patrol_end para abelhas geralmente definem o limite do movimento vertical
    # Abelha 2
    [2, "Abelha", sprite_inimigo_abelha, 1800, 180, 30, 25, 0, 0],
    # Abelha 3
    [2, "Abelha", sprite_inimigo_abelha, 2400, 250, 30, 25, 0, 0]
]

game_sprites_assets = {
    'sprite_inimigo_urso': sprite_inimigo_urso,
    'sprite_poo': sprite_poo,
    'sprite_leitao': sprite_leitao,
    'sprite_honey': sprite_honey,
    'sprite_boss': sprite_boss,
    'sprite_inimigo_abelha': sprite_inimigo_abelha,
    'sprite_mapa': sprite_mapa,
    'sprite_projetil': sprite_projetil
}


all_sprites = pygame.sprite.Group()
plataforms_group = pygame.sprite.Group()
honey_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
stingers_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()

player = Player(
    id_character=0,
    name_character="Pooh",
    sprite=sprite_poo,
    pos_x=100,
    pos_y=300,
    tam_x=40,
    tam_y=60,
    speed_x=5,
    speed_y=0
    )
hose_rect = None

def draw_multiline_text(surface, text, font, color, rect):
    lines = text.splitlines()
    y = rect.y
    for line in lines:
        line_surface = font.render(line, True, color)
        surface.blit(line_surface, (rect.x, y))
        y += font.get_linesize()

leitao = Npc(
        id_character= 2,
        name_character= "Leitao",
        sprite = sprite_leitao,
        pos_x= 100,    #definir quando o mapa ficar pronto
        pos_y= 300,    #definir quando o mapa ficar pronto
        tam_x= 8,    #definir conforme a sprite
        tam_y= 5,    #definir conforme a sprite
    )

game_state = 'intro'
honey_score = 0
total_honey = Game.setup_level(all_sprites, plataforms_group, honey_group, enemies_group,
    boss_group, stingers_group, water_group, player,
    platform_map, honey_map, enemy_map, game_sprites_assets, Plataform, Honey, Inimigo)

all_sprites.add(leitao)
boss_level_setup_done = False
camera_x = 0
camera_smoothing = 0.05

pygame.mixer.music.play(loops=-1)

gameLoop = True
if __name__ == '__main__':
    while gameLoop:
        dt = clock.get_time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                gameLoop = False
            if game_state == 'intro' and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = 'level_1'
            if game_state == 'game_over' and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    honey_score = 0
                    game_state = 'level_1'
                    total_honey = Game.setup_level(all_sprites, plataforms_group, honey_group, enemies_group,
                        boss_group, stingers_group, water_group, player,
                        platform_map, honey_map, enemy_map, game_sprites_assets, Plataform, Honey, Inimigo)
                    
                    all_sprites.add(leitao)
                    boss_level_setup_done = False
                    pygame.mixer.music.load(level1_music_path)
                    pygame.mixer.music.play(loops=-1)
        keys = pygame.key.get_pressed()

         # --- LÓGICA DE ESTADOS ---
        
        if game_state == 'intro':
            display.fill((93, 226, 231))
            leitao.update(dt)
            display.blit(leitao.image, leitao.rect) 

            health_text = game_font.render(f'Vida: {player.vida}', True, (255, 255, 255))
            display.blit(health_text, (10, 10))
            honey_text = game_font.render(f'Mel: {honey_score}/{total_honey}', True, (255, 255, 255))
            display.blit(honey_text, (10, 40))

            smoke_overlay = pygame.Surface((COMPRIMENTO_TELA, ALTURA_TELA), pygame.SRCALPHA)
            smoke_overlay.fill((0, 0, 0, 180))
            display.blit(smoke_overlay, (0, 0))
            
            dialog_rect = pygame.Rect(50, ALTURA_TELA/2, 75, COMPRIMENTO_TELA)
            pygame.draw.rect(display, (50, 50, 50), dialog_rect)
            pygame.draw.rect(display, (255, 255, 255), dialog_rect, 3)
            
            instructions = ("Bem-vindo, Jogador!\nUse A/D para mover, W para pular.\nColete todo o mel para lutar contra a Abelha Rainha!\nAperte E para acionar a mangueira.\nPressione ESPAÇO para começar.")
            draw_multiline_text(display, instructions, game_font, (255, 255, 255), dialog_rect.inflate(-20, -20))

        elif game_state == 'level_1':
            player.update(plataforms_group, level_width, jump_sound, dt)
            
            for enemy in enemies_group:
                enemy.animacao.atualiza(dt)


            for honey_pot in honey_group:
                honey_pot.animacao.atualiza(dt)
            leitao.update(dt)
            
            if pygame.sprite.spritecollide(player, honey_group, True):
                honey_score += 1
                collect_sound.play()
            
            if not player.invincible:
                enemy_hits = pygame.sprite.spritecollide(player, enemies_group, False)
                if enemy_hits:
                    enemy = enemy_hits[0]
                    player.invincible = True
                    player.hurt_time = pygame.time.get_ticks()
                    player.vida -= 1
                    hurt_sound.play()
                    print(f'Atingido! Vidas restantes: {player.vida}')
                    if player.rect.centerx < enemy.rect.centerx:
                        player.rect.x -= player.knockback_strength
                    else:
                        player.rect.x += player.knockback_strength
                    player._speed_y = -8
            
            target_camera_x = player.rect.centerx - (COMPRIMENTO_TELA / 2)
            camera_x += (target_camera_x - camera_x) * camera_smoothing
            if camera_x < 0:
                camera_x = 0
            if camera_x > level_width - COMPRIMENTO_TELA:
                camera_x = level_width - COMPRIMENTO_TELA
            
            if honey_score >= total_honey:
                game_state = 'boss_level'
                pygame.mixer.music.load(boss_music) # Carrega a nova música
                pygame.mixer.music.play(loops=-1)
            if player.vida <= 0:
                game_state = 'game_over'
            
            display.fill((93, 226, 231))
            for sprite in all_sprites:
                screen_rect = sprite.rect.copy()
                screen_rect.x -= int(camera_x)
                display.blit(sprite.image, screen_rect)
            
            health_text = game_font.render(f'Vida: {player.vida}', True, (255, 255, 255))
            display.blit(health_text, (10, 10))
            honey_text = game_font.render(f'Mel: {honey_score}/{total_honey}', True, (255, 255, 255))
            display.blit(honey_text, (10, 40))

        elif game_state == 'boss_level':
            if not boss_level_setup_done:
                boss = Game.setup_boss_level(all_sprites, plataforms_group,honey_group, enemies_group, stingers_group, water_group, boss_group, player, sprite_boss)
                boss_level_setup_done = True
            dt = clock.get_time()
            player.update(plataforms_group, COMPRIMENTO_TELA, jump_sound, dt) 
            
            for boss_sprite in boss_group:
                boss_sprite.animacao.atualiza(dt)
            boss_group.update(all_sprites, stingers_group, sprite_projetil, dt) 
            

            for stinger in stingers_group:
                stinger.animacao.atualiza(dt) # Se Stinger usa Animacao
            stingers_group.update(dt)

            for water_splash in water_group:
                pass #agua não tem animação no seu código, só se move
            water_group.update(dt)
           
            
            if keys[pygame.K_e] and player.rect.colliderect(hose_rect):
                water = Water(hose_rect.centerx, hose_rect.top)
                all_sprites.add(water)
                water_group.add(water)
            
            player.update(plataforms_group, dt)
            
            for boss_sprite in boss_group:
                 boss_sprite.update(all_sprites, stingers_group, game_sprites_assets['sprite_projetil'], dt)
            
            for stinger in stingers_group:
                stinger.update(dt)

            for water_splash in water_group:
                water_splash.update(dt)

            if not player.invincible:
                stinger_hits = pygame.sprite.spritecollide(player, stingers_group, True)
                if stinger_hits:
                    player.invincible = True
                    player.hurt_time = pygame.time.get_ticks()
                    player.vida -= 1
                    hurt_sound.play()
                    print(f'Atingido por um ferrão!')
                    player._speed_y = -8
            
            boss_hit_dict = pygame.sprite.groupcollide(water_group, boss_group, True, False)
            if boss_hit_dict:
                boss = list(boss_hit_dict.values())[0][0]
                boss.health -= 1
                print(f"Chefe atingido! Vida restante: {boss.health}")
            
            if player.vida <= 0:
                game_state = 'game_over'
            if len(boss_group) > 0 and list(boss_group)[0].health <= 0:
                game_state = 'you_win'
            
            display.fill((50, 0, 0))
            ground_boss = pygame.Rect(0, 440, COMPRIMENTO_TELA, 40)
            pygame.draw.rect(display, (34, 139, 34), ground_boss)
            pygame.draw.rect(display, (100, 100, 100), hose_rect)
            all_sprites.draw(display)
            health_text = game_font.render(f'Vida: {player.vida}', True, (255, 255, 255))
            display.blit(health_text, (10, 10))
            if len(boss_group) > 0:
                boss_health_text = game_font.render(f'Vida Chefe: {list(boss_group)[0].health}', True, (255, 255, 0))
                display.blit(boss_health_text, (600, 10))
        
        elif game_state == 'game_over' or game_state == 'you_win':
            if game_state == 'game_over':
                display.fill((0, 0, 0))
                go_text = game_font.render("GAME OVER", True, (255, 0, 0))
                go_rect = go_text.get_rect(center=(COMPRIMENTO_TELA/2, ALTURA_TELA/2 - 20))
                display.blit(go_text, go_rect)
                restart_text = game_font.render("Pressione R para reiniciar", True, (255, 255, 255))
                restart_rect = restart_text.get_rect(center=(COMPRIMENTO_TELA/2, ALTURA_TELA/2 + 20))
                display.blit(restart_text, restart_rect)
            else: # you_win
                display.fill((255, 255, 255))
                win_text = game_font.render("VOCE VENCEU!", True, (0, 200, 0))
                win_rect = win_text.get_rect(center=(COMPRIMENTO_TELA/2, ALTURA_TELA/2))
                display.blit(win_text, win_rect)
        
        pygame.display.update()
        clock.tick(60)

pygame.quit()
