import pygame

# --- 1. DEFINIÇÃO DAS CLASSES ---

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([40, 60]).convert()
        self.image.fill((255, 165, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 300
        self.speed = 5
        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_strength = -14
        self.on_ground = False
        self.health = 3
        self.invincible = False
        self.invincibility_duration = 1500
        self.hurt_time = 0
        self.knockback_strength = 20

    # Dentro da classe Player, substitua o método 'update' inteiro por este:

    def update(self, plataforms_group):
        # Primeiro, cuidamos da invencibilidade e do efeito de piscar
        if self.invincible:
            current_time = pygame.time.get_ticks()
            self.image.set_alpha(128 if (current_time // 100) % 2 == 0 else 255)
            if current_time - self.hurt_time > self.invincibility_duration:
                self.invincible = False
                self.image.set_alpha(255)

        # --- 1. LÓGICA DE INPUT ---
        keys = pygame.key.get_pressed()

        # Movimento Horizontal (só se não estiver em knockback)
        if not self.invincible:
            if keys[pygame.K_d]:
                self.rect.x += self.speed
            if keys[pygame.K_a]:
                self.rect.x -= self.speed
        
        # Pulo (só se não estiver em knockback e estiver no chão)
        if not self.invincible and keys[pygame.K_w] and self.on_ground:
            self.velocity_y = self.jump_strength
            self.on_ground = False # Importante para evitar pulo duplo
            jump_sound.play()

        # --- 2. LÓGICA DE FÍSICA ---
        # Aplica a gravidade à velocidade vertical
        self.velocity_y += self.gravity
        
        # --- 3. ATUALIZAÇÃO DE POSIÇÃO ---
        # Move o jogador no eixo Y
        self.rect.y += self.velocity_y
        
        # --- 4. RESOLUÇÃO DE COLISÕES ---
        # Assume que o jogador está no ar até que uma colisão prove o contrário
        self.on_ground = False

        # Colisão com o chão
        if self.rect.bottom >= 440:
            self.rect.bottom = 440
            self.velocity_y = 0
            self.on_ground = True

        # Colisão com as plataformas (só verifica se estiver caindo)
        if self.velocity_y > 0:
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
                    self.velocity_y = 0
                    self.on_ground = True
        
        # Limites do mundo para o jogador
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > level_width:
            self.rect.right = level_width

class Plataform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface([w,h])
        self.image.fill((139, 69, 19))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Honey(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill((255, 215, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type, patrol_start, patrol_end):
        super().__init__()
        self.enemy_type = enemy_type
        if self.enemy_type == 'bear':
            self.image = pygame.Surface([35, 50])
            self.image.fill((88, 41, 0))
            self.speed_x = 2
            self.speed_y = 0
        elif self.enemy_type == 'bee':
            self.image = pygame.Surface([30, 25])
            self.image.fill((255, 255, 0))
            self.speed_x = 0
            self.speed_y = 2
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.patrol_start = patrol_start
        self.patrol_end = patrol_end

    def update(self, *args):
        if self.enemy_type == 'bear':
            self.rect.x += self.speed_x
            if self.rect.right > self.patrol_end or self.rect.left < self.patrol_start:
                self.speed_x *= -1
        elif self.enemy_type == 'bee':
            self.rect.y += self.speed_y
            if self.rect.bottom > 440 or self.rect.top < 0:
                self.speed_y *= -1

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 100
        self.image = pygame.Surface([80, 70])
        self.image.fill((255, 200, 0))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, 80))
        self.speed_x = 4
        self.shoot_delay = 1000
        self.last_shot_time = pygame.time.get_ticks()

    def update(self, all_sprites_group, stingers_group):
        self.rect.x += self.speed_x
        if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
            self.speed_x *= -1

        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            self.last_shot_time = now
            stinger = Stinger(self.rect.centerx, self.rect.bottom)
            all_sprites_group.add(stinger)
            stingers_group.add(stinger)

class Stinger(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 20])
        self.image.fill((211, 209, 209))
        self.rect = self.image.get_rect(center=(x,y))
        self.speed_y = 7.5

    def update(self, *args):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill((0,150,255))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_y = -12

    def update(self, *args):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

# --- 2. INÍCIO E CONFIGURAÇÕES ---
SCREEN_WIDTH = 840
SCREEN_HEIGHT = 480

pygame.init()
game_font = pygame.font.Font(None, 36)
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Ursinho POO')
clock = pygame.time.Clock()
pygame.mixer.init()
level1_music_path = 'Assets/Sons/fase1.mp3'
pygame.mixer.music.load('Assets/Sons/fase1.mp3')
pygame.mixer.music.set_volume(0.4)
jump_sound = pygame.mixer.Sound('Assets/Sons/jump.wav')
collect_sound = pygame.mixer.Sound('Assets/Sons/mel.wav')
hurt_sound = pygame.mixer.Sound('Assets/Sons/hit.wav')
boss_music = 'Assets/Sons/boss.mp3'

# --- 3. DEFINIÇÃO DO MAPA DO NÍVEL ---
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
    [600, 440 - 50, 'bear', 550, 800], [1000, 250 - 50, 'bear', 950, 1100], 
    [1500, 300 - 50, 'bear', 1450, 1600], [800, 200, 'bee', 0, 0], 
    [1800, 180, 'bee', 0, 0], [2400, 250, 'bee', 0, 0]
]

# --- 4. GRUPOS, FUNÇÕES E OBJETOS ---
all_sprites = pygame.sprite.Group()
plataforms_group = pygame.sprite.Group()
honey_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
stingers_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()

player = Player()
hose_rect = None

def draw_multiline_text(surface, text, font, color, rect):
    lines = text.splitlines()
    y = rect.y
    for line in lines:
        line_surface = font.render(line, True, color)
        surface.blit(line_surface, (rect.x, y))
        y += font.get_linesize()

def setup_level():
    all_sprites.empty()
    plataforms_group.empty()
    honey_group.empty()
    enemies_group.empty()
    boss_group.empty()
    stingers_group.empty()
    water_group.empty()

    all_sprites.add(player)
    player.rect.x = 100
    player.rect.y = 300
    player.health = 3
    player.invincible = False
    player.velocity_y = 0

    for data in platform_map:
        plat = Plataform(*data)
        all_sprites.add(plat)
        plataforms_group.add(plat)
    
    for data in honey_map:
        honey = Honey(*data)
        all_sprites.add(honey)
        honey_group.add(honey)

    for data in enemy_map:
        enemy = Enemy(*data)
        all_sprites.add(enemy)
        enemies_group.add(enemy)
    
    return len(honey_map)

def setup_boss_level():
    global hose_rect
    all_sprites.empty()
    plataforms_group.empty()
    honey_group.empty()
    enemies_group.empty()
    stingers_group.empty()
    water_group.empty()
    
    all_sprites.add(player)
    boss = Boss()
    all_sprites.add(boss)
    boss_group.add(boss)
    
    player.rect.x = 100
    player.rect.bottom = 440
    player.velocity_y = 0
    
    hose_rect = pygame.Rect(400, 440 - 50, 40, 50)

# --- 5. VARIÁVEIS DE CONTROLE DO JOGO ---
game_state = 'intro'
honey_score = 0
total_honey = setup_level()
boss_level_setup_done = False
camera_x = 0
camera_smoothing = 0.05

pygame.mixer.music.play(loops=-1)

# --- 6. LOOP PRINCIPAL ---
gameLoop = True
if __name__ == '__main__':
    while gameLoop:
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
                    total_honey = setup_level()
                    boss_level_setup_done = False
                    pygame.mixer.music.load(level1_music_path)
                    pygame.mixer.music.play(loops=-1)
        
        keys = pygame.key.get_pressed()
        
        # --- LÓGICA DE ESTADOS ---
        
        if game_state == 'intro':
            display.fill((93, 226, 231))
            for sprite in all_sprites:
                screen_rect = sprite.rect.copy()
                screen_rect.x -= int(camera_x)
                display.blit(sprite.image, screen_rect)
            
            health_text = game_font.render(f'Vida: {player.health}', True, (255, 255, 255))
            display.blit(health_text, (10, 10))
            honey_text = game_font.render(f'Mel: {honey_score}/{total_honey}', True, (255, 255, 255))
            display.blit(honey_text, (10, 40))

            smoke_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            smoke_overlay.fill((0, 0, 0, 180))
            display.blit(smoke_overlay, (0, 0))

            npc_rect = pygame.Rect(100, 380 - 80, 50, 80)
            pygame.draw.rect(display, (255, 100, 100), npc_rect)
            
            dialog_rect = pygame.Rect(200, 280, 680, 150)
            pygame.draw.rect(display, (50, 50, 50), dialog_rect)
            pygame.draw.rect(display, (255, 255, 255), dialog_rect, 3)
            
            instructions = ("Bem-vindo, Jogador!\nUse A/D para mover, W para pular.\nColete todo o mel para lutar contra a Abelha Rainha!\nAperte E para acionar a mangueira.\nPressione ESPAÇO para começar.")
            draw_multiline_text(display, instructions, game_font, (255, 255, 255), dialog_rect.inflate(-20, -20))

        elif game_state == 'level_1':
            
    
            
            all_sprites.update(plataforms_group)
            
            if pygame.sprite.spritecollide(player, honey_group, True):
                honey_score += 1
                collect_sound.play()
            
            if not player.invincible:
                enemy_hits = pygame.sprite.spritecollide(player, enemies_group, False)
                if enemy_hits:
                    enemy = enemy_hits[0]
                    player.invincible = True
                    player.hurt_time = pygame.time.get_ticks()
                    player.health -= 1
                    hurt_sound.play()
                    print(f'Atingido! Vidas restantes: {player.health}')
                    if player.rect.centerx < enemy.rect.centerx:
                        player.rect.x -= player.knockback_strength
                    else:
                        player.rect.x += player.knockback_strength
                    player.velocity_y = -8
            
            target_camera_x = player.rect.centerx - (SCREEN_WIDTH / 2)
            camera_x += (target_camera_x - camera_x) * camera_smoothing
            if camera_x < 0:
                camera_x = 0
            if camera_x > level_width - SCREEN_WIDTH:
                camera_x = level_width - SCREEN_WIDTH
            
            if honey_score >= total_honey:
                game_state = 'boss_level'
                pygame.mixer.music.load(boss_music) # Carrega a nova música
                pygame.mixer.music.play(loops=-1)
            if player.health <= 0:
                game_state = 'game_over'
            
            display.fill((93, 226, 231))
            for sprite in all_sprites:
                screen_rect = sprite.rect.copy()
                screen_rect.x -= int(camera_x)
                display.blit(sprite.image, screen_rect)
            
            health_text = game_font.render(f'Vida: {player.health}', True, (255, 255, 255))
            display.blit(health_text, (10, 10))
            honey_text = game_font.render(f'Mel: {honey_score}/{total_honey}', True, (255, 255, 255))
            display.blit(honey_text, (10, 40))

        elif game_state == 'boss_level':
            if not boss_level_setup_done:
                setup_boss_level()
                boss_level_setup_done = True
            
           
            
            if keys[pygame.K_e] and player.rect.colliderect(hose_rect):
                water = Water(hose_rect.centerx, hose_rect.top)
                all_sprites.add(water)
                water_group.add(water)
            
            player.update(plataforms_group)
            boss_group.update(all_sprites, stingers_group)
            stingers_group.update()
            water_group.update()
            
            if not player.invincible:
                stinger_hits = pygame.sprite.spritecollide(player, stingers_group, True)
                if stinger_hits:
                    player.invincible = True
                    player.hurt_time = pygame.time.get_ticks()
                    player.health -= 1
                    hurt_sound.play()
                    print(f'Atingido por um ferrão!')
                    player.velocity_y = -8
            
            boss_hit_dict = pygame.sprite.groupcollide(water_group, boss_group, True, False)
            if boss_hit_dict:
                boss = list(boss_hit_dict.values())[0][0]
                boss.health -= 1
                print(f"Chefe atingido! Vida restante: {boss.health}")
            
            if player.health <= 0:
                game_state = 'game_over'
            if len(boss_group) > 0 and list(boss_group)[0].health <= 0:
                game_state = 'you_win'
            
            display.fill((50, 0, 0))
            ground_boss = pygame.Rect(0, 440, SCREEN_WIDTH, 40)
            pygame.draw.rect(display, (34, 139, 34), ground_boss)
            pygame.draw.rect(display, (100, 100, 100), hose_rect)
            all_sprites.draw(display)
            
            health_text = game_font.render(f'Vida: {player.health}', True, (255, 255, 255))
            display.blit(health_text, (10, 10))
            if len(boss_group) > 0:
                boss_health_text = game_font.render(f'Vida Chefe: {list(boss_group)[0].health}', True, (255, 255, 0))
                display.blit(boss_health_text, (600, 10))
        
        elif game_state == 'game_over' or game_state == 'you_win':
            if game_state == 'game_over':
                display.fill((0, 0, 0))
                go_text = game_font.render("GAME OVER", True, (255, 0, 0))
                go_rect = go_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 20))
                display.blit(go_text, go_rect)
                restart_text = game_font.render("Pressione R para reiniciar", True, (255, 255, 255))
                restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20))
                display.blit(restart_text, restart_rect)
            else: # you_win
                display.fill((255, 255, 255))
                win_text = game_font.render("VOCE VENCEU!", True, (0, 200, 0))
                win_rect = win_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                display.blit(win_text, win_rect)
        
        pygame.display.update()
        clock.tick(60)

pygame.quit()
