import pygame

# --- 1. DEFINIÇÃO DAS CLASSES ---

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        try:
            _sprites_direita_originais = [pygame.image.load(f"Assets/Poo/Direita/poo.{i}.png").convert_alpha() for i in [1, 3, 5, 7]]
            self._sprites_direita = [pygame.transform.scale(img, (32, 78)) for img in _sprites_direita_originais]
            self._sprites_esquerda = [pygame.transform.flip(img, True, False) for img in self._sprites_direita]
        except pygame.error as e:
            print(f"Erro ao carregar sprites do jogador: {e}")
            self._sprites_direita = [pygame.Surface([40, 60]) for _ in range(4)]
            for surf in self._sprites_direita: surf.fill((255, 165, 0))
            self._sprites_esquerda = [pygame.transform.flip(surf, True, False) for surf in self._sprites_direita]

        self._indice_animacao = 0
        self._velocidade_animacao = 0.15
        self._contador_frame = 0
        self._direcao = "direita"
        
        # Não sofrem encapsulamento por serem essenciais para desenho e colisao
        self.image = self._sprites_direita[self._indice_animacao] 
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        #

        self.rect.x = 100
        self.rect.y = 300
        self._speed = 5
        self._velocity_y = 0
        self._gravity = 0.5
        self._jump_strength = -14
        self._on_ground = False
        self._health = 3
        self._total_health = 3 
        self._invincible = False
        self._invincibility_duration = 1500
        self._hurt_time = 0
        self._knockback_strength = 20

    def animar(self, is_moving):
        if is_moving:
            self._contador_frame += self._velocidade_animacao
            if self._contador_frame >= 1:
                self._contador_frame = 0
                self._indice_animacao = (self._indice_animacao + 1) % len(self._sprites_direita)
        else:
            self._indice_animacao = 0

        if self._direcao == "direita":
            self.image = self._sprites_direita[self._indice_animacao]
        else:
            self.image = self._sprites_esquerda[self._indice_animacao]
        
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, plataforms_group):
        if self._invincible:
            current_time = pygame.time.get_ticks()
            self.image.set_alpha(128 if (current_time // 100) % 2 == 0 else 255)
            if current_time - self._hurt_time > self._invincibility_duration:
                self._invincible = False
                self.image.set_alpha(255)

        keys = pygame.key.get_pressed()
        is_moving = False 

        if not self._invincible:
            if keys[pygame.K_d]:
                self.rect.x += self._speed
                self._direcao = "direita"
                is_moving = True
            if keys[pygame.K_a]:
                self.rect.x -= self._speed
                self._direcao = "esquerda"
                is_moving = True
        
        self.animar(is_moving)
        
        if not self._invincible and keys[pygame.K_w] and self._on_ground:
            self._velocity_y = self._jump_strength
            self._on_ground = False 
            jump_sound.play()

        self._velocity_y += self._gravity
        self.rect.y += self._velocity_y
        
        self._on_ground = False
        if self.rect.bottom >= chao_y:
            self.rect.bottom = chao_y
            self._velocity_y = 0
            self._on_ground = True

        if self._velocity_y > 0:
            hits = pygame.sprite.spritecollide(self, plataforms_group, False)
            if hits:
                closest_platform = min(hits, key=lambda p: p.rect.top)
                if self.rect.bottom > closest_platform.rect.top:
                    self.rect.bottom = closest_platform.rect.top
                    self._velocity_y = 0
                    self._on_ground = True
        
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > level_width: self.rect.right = level_width

class Plataform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, top_tile_img, body_tile_img):
        super().__init__()
        self.image = pygame.Surface([w,h])
        tile_w, tile_h = top_tile_img.get_size() #Por serem atributos loais que só existem dentro de __init__, naturalmente ja externamente inacessiveis 

        for tile_x in range(0, w, tile_w):  #Por serem atributos loais que só existem dentro de __init__, naturalmente ja externamente inacessiveis 
            for tile_y in range(0, h, tile_h): #Por serem atributos loais que só existem dentro de __init__, naturalmente ja externamente inacessiveis 
                if tile_y == 0:
                    self.image.blit(top_tile_img, (tile_x, tile_y))
                else:
                    self.image.blit(body_tile_img, (tile_x, tile_y))
        
        self.rect = self.image.get_rect(topleft=(x, y))

class Honey(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load("Assets/Itens/pote_de_mel.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (96, 96))
        except pygame.error as e:
            print(f"Erro ao carregar sprite do mel: {e}. Usando um quadrado amarelo.")
            self.image = pygame.Surface([20, 20])
            self.image.fill((255, 215, 0))
        
        self.rect = self.image.get_rect(bottomleft=(x, y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type, patrol_start, patrol_end):
        super().__init__()
        self._enemy_type = enemy_type
        self._indice_animacao = 0
        self._velocidade_animacao = 0.1
        self._contador_frame = 0


        if self._enemy_type == 'bear':
            try:
                _sprites_originais = [pygame.image.load(f"Assets/Urso/urso_{i}.png").convert_alpha() for i in [1, 2]]
                self._sprites_esquerda = [pygame.transform.scale(img, (87, 45)) for img in _sprites_originais]
                self._sprites_direita = [pygame.transform.flip(img, True, False) for img in self._sprites_esquerda]
                
            except pygame.error as e:
                print(f"Erro ao carregar sprites do urso: {e}")
                _fallback_surf = pygame.Surface([70, 50]); _fallback_surf.fill((88, 41, 0))
                self._sprites_direita = [_fallback_surf] * 2
                self._sprites_esquerda = [_fallback_surf] * 2
            self.image = self._sprites_direita[self._indice_animacao]
            self._speed_x, self._speed_y = 2, 0

        elif self._enemy_type == 'bee':
            try:
                _sprites_originais = [pygame.image.load(f"Assets/Abelha/abelha_{i}.png").convert_alpha() for i in range(1, 5)]
                self._sprites = [pygame.transform.scale(img, (96, 96)) for img in _sprites_originais]
            except pygame.error as e:
                print(f"Erro ao carregar sprites da abelha: {e}")
                _fallback_surf = pygame.Surface([48, 48]); _fallback_surf.fill((255, 255, 0))
                self._sprites = [_fallback_surf] * 4
            self.image = self._sprites[self._indice_animacao]
            self._speed_x, self._speed_y = 0, 2
        
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self._patrol_start = patrol_start
        self._patrol_end = patrol_end

    def animar(self):
        self._contador_frame += self._velocidade_animacao
        if self._contador_frame >= 1:
            self._contador_frame = 0
            if self._enemy_type == 'bear':
                self._indice_animacao = (self._indice_animacao + 1) % len(self._sprites_direita)
                self.image = self._sprites_direita[self._indice_animacao] if self._speed_x > 0 else self._sprites_esquerda[self._indice_animacao]
            elif self._enemy_type == 'bee':
                self._indice_animacao = (self._indice_animacao + 1) % len(self._sprites)
                self.image = self._sprites[self._indice_animacao]
        
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        if self._enemy_type == 'bear':
            self.rect.x += self._speed_x
            if self.rect.right > self._patrol_end or self.rect.left < self._patrol_start:
                self._speed_x *= -1
        elif self._enemy_type == 'bee':
            self.rect.y += self._speed_y
            if self.rect.bottom > chao_y or self.rect.top < 10:
                self._speed_y *= -1
        self.animar()

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 100 # Atributo público, pois a vida do chefe será modificada de fora da classe
        
        try:
            _sprites_originais = [pygame.image.load(f"Assets/Boss/abelha_rainha_{i}.png").convert_alpha() for i in [1, 2]]
            self._sprites_esquerda = [pygame.transform.scale(img, (120, 100)) for img in _sprites_originais]
            self._sprites_direita = [pygame.transform.flip(img, True, False) for img in self._sprites_esquerda]

        except pygame.error as e:
            print(f"Erro ao carregar sprites do Boss: {e}")
            _fallback_surf = pygame.Surface([120, 100]); _fallback_surf.fill((255, 200, 0))
            self._sprites_direita = [_fallback_surf] * 2
            self._sprites_esquerda = [_fallback_surf] * 2

        self._indice_animacao = 0
        self._velocidade_animacao = 0.2
        self._contador_frame = 0
        
        self._speed_x = 4
        self.image = self._sprites_direita[self._indice_animacao]
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / (2 * zoom_level), 100))
        self.mask = pygame.mask.from_surface(self.image)

        self._shoot_delay = 1000
        self._last_shot_time = pygame.time.get_ticks()

    def animar(self):
        self._contador_frame += self._velocidade_animacao
        if self._contador_frame >= 1:
            self._contador_frame = 0
            self._indice_animacao = (self._indice_animacao + 1) % len(self._sprites_direita)
            
            if self._speed_x > 0:
                self.image = self._sprites_direita[self._indice_animacao]
            else:
                self.image = self._sprites_esquerda[self._indice_animacao]
        
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, all_sprites_group, stingers_group):
        self.animar()
        self.rect.x += self._speed_x
        if self.rect.right > game_surface.get_width() or self.rect.left < 0:
            self._speed_x *= -1

        now = pygame.time.get_ticks()
        if now - self._last_shot_time > self._shoot_delay:
            self._last_shot_time = now
            stinger = Stinger(self.rect.centerx, self.rect.bottom)
            all_sprites_group.add(stinger)
            stingers_group.add(stinger)

class Stinger(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load("Assets/Ferrao/ferrao.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (15, 25))
        except pygame.error as e:
            print(f"Erro ao carregar sprite do ferrão: {e}. Usando um retângulo cinza.")
            self.image = pygame.Surface([10, 20])
            self.image.fill((211, 209, 209))

        self.rect = self.image.get_rect(center=(x,y))
        self.mask = pygame.mask.from_surface(self.image)
        self._speed_y = 7.5

    def update(self, *args):
        self.rect.y += self._speed_y
        if self.rect.top > game_surface.get_height():
            self.kill()

class Water(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill((0,150,255))
        self.rect = self.image.get_rect(center=(x, y))
        self._speed_y = -12

    def update(self, *args):
        self.rect.y += self._speed_y
        if self.rect.bottom < 0:
            self.kill()

class Mangueira(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load("Assets/Mangueira/mangueira.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (61, 50))
        except pygame.error as e:
            print(f"Erro ao carregar sprite da mangueira: {e}. Usando um retângulo cinza.")
            self.image = pygame.Surface([40, 50])
            self.image.fill((100, 100, 100))
        
        self.rect = self.image.get_rect(bottomleft=(x, y))

class Npc(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(image,(80,100))
        self.rect = self.image.get_rect(bottomleft=(x, y))

# --- 2. INÍCIO E CONFIGURAÇÕES ---
pygame.init()

display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH = display.get_width()
SCREEN_HEIGHT = display.get_height()

zoom_level = 1.5 
game_surface = pygame.Surface((SCREEN_WIDTH / zoom_level, SCREEN_HEIGHT / zoom_level))

game_font = pygame.font.Font(None, 48)
pygame.display.set_caption('Ursinho POO')
clock = pygame.time.Clock()
pygame.mixer.init()

# --- CARREGAMENTO DE ASSETS DO CENÁRIO ---
try:
    grass_tile_img = pygame.image.load("Assets/Tiles/grama_topo_outono.png").convert_alpha()
    dirt_tile_img = pygame.image.load("Assets/Tiles/terra_baixo_centro_outono.png").convert_alpha()
    background_images = []
    for i in range(1, 6):
        path = f"Assets/Mapas/floresta_outono/camada_{i}.png"
        img = pygame.image.load(path).convert_alpha()
        escala = game_surface.get_height() / img.get_height()
        img_redimensionada = pygame.transform.scale(img, (int(img.get_width() * escala), game_surface.get_height()))
        background_images.append(img_redimensionada)
except pygame.error as e:
    print(f"Erro ao carregar assets do cenário de outono: {e}")
    grass_tile_img = pygame.Surface((32,32)); grass_tile_img.fill((34, 139, 34))
    dirt_tile_img = pygame.Surface((32,32)); dirt_tile_img.fill((139, 69, 19))
    background_images = []

try:
    grass_tile_summer_img = pygame.image.load("Assets/Tiles/grama_topo_outono.png").convert_alpha()
    dirt_tile_summer_img = pygame.image.load("Assets/Tiles/terra_baixo_centro_outono.png").convert_alpha()
    boss_background_images = []
    for i in range(1, 6):
        path = f"Assets/Mapas/floresta_verao/camada_{i}.png"
        img = pygame.image.load(path).convert_alpha()
        escala = game_surface.get_height() / img.get_height()
        img_redimensionada = pygame.transform.scale(img, (int(img.get_width() * escala), game_surface.get_height()))
        boss_background_images.append(img_redimensionada)


except pygame.error as e:
    print(f"Erro ao carregar assets do cenário de verão (chefe): {e}")
    grass_tile_summer_img = pygame.Surface((32,32))
    grass_tile_summer_img.fill((60, 179, 113))
    dirt_tile_summer_img = pygame.Surface((32,32))
    dirt_tile_summer_img.fill((101, 67, 33))
    boss_background_images = []
    npc_img = pygame.Surface((50, 80))
    npc_img.fill((255, 100, 100))

try:
    npc_img = pygame.image.load("Assets/Npc/pig.png")

except pygame.error as e:
    # ... (código de erro da UI) ...
    # Fallback para o NPC
    npc_img = pygame.Surface((50, 80))
    npc_img.fill((255, 100, 100))
    
# --- HUD DE VIDA E MEL COM SPRITES ---
try:
    full_heart_img = pygame.image.load("Assets/UI/coracao_cheio.png").convert_alpha()
    empty_heart_img = pygame.image.load("Assets/UI/coracao_vazio.png").convert_alpha()
    
    heart_size = (int(35 * zoom_level), int(35 * zoom_level))
    full_heart_img = pygame.transform.scale(full_heart_img, heart_size)
    empty_heart_img = pygame.transform.scale(empty_heart_img, heart_size)

    honey_pot_ui_img = pygame.image.load("Assets/Itens/pote_de_mel.png").convert_alpha()
    honey_pot_ui_img = pygame.transform.scale(honey_pot_ui_img, (int(96 * zoom_level), int(96 * zoom_level)))

except pygame.error as e:
    print(f"Erro ao carregar sprites da UI: {e}")
    heart_size = (int(35 * zoom_level), int(35 * zoom_level))
    full_heart_img = pygame.Surface(heart_size); full_heart_img.fill((255, 0, 0))
    empty_heart_img = pygame.Surface(heart_size); empty_heart_img.fill((50, 50, 50))
    honey_pot_ui_img = pygame.Surface((int(40 * zoom_level), int(40 * zoom_level))); honey_pot_ui_img.fill((255, 215, 0))


level1_music_path = 'Assets/Sons/fase1.mp3'
pygame.mixer.music.load(level1_music_path)
pygame.mixer.music.set_volume(0.4)
jump_sound = pygame.mixer.Sound('Assets/Sons/jump.wav')
collect_sound = pygame.mixer.Sound('Assets/Sons/mel.wav')
hurt_sound = pygame.mixer.Sound('Assets/Sons/hit.wav')
boss_music = 'Assets/Sons/boss.mp3'

# --- 3. DEFINIÇÃO DO MAPA DO NÍVEL ---
level_width = 3000
chao_y = game_surface.get_height() - 40

# As coordenadas Y das plataformas (CORREÇÃO DO ERRO)
p_chao = chao_y
p1_y = chao_y - 90
p2_y = chao_y - 160
p3_y = chao_y - 80
p4_y = chao_y - 190
p5_y = chao_y - 260
p6_y = chao_y - 140
p7_y = chao_y - 220
p8_y = chao_y - 290
p9_y = chao_y - 160
p10_y = chao_y - 90

platform_map = [
    (0, p_chao, level_width, 40), (200, p1_y, 150, 20), (450, p2_y, 200, 20), 
    (700, p3_y, 100, 20), (900, p4_y, 150, 20), (1150, p5_y, 120, 20), 
    (1400, p6_y, 180, 20), (1650, p7_y, 100, 20), (1900, p8_y, 100, 20), 
    (2200, p9_y, 150, 20), (2500, p10_y, 100, 20)
]

honey_map = [
    [250, p1_y], [500, p2_y], [950, p4_y], [1200, p5_y], [1450, p6_y], 
    [1700, p7_y], [1950, p8_y], [2250, p9_y], [2550, p10_y]
]
enemy_map = [
    [600, p_chao, 'bear', 550, 800], [1000, p4_y, 'bear', 950, 1100], 
    [1500, p6_y, 'bear', 1450, 1600], [800, 200, 'bee', 0, 0], 
    [1800, 180, 'bee', 0, 0], [2400, 250, 'bee', 0, 0]
]

# --- 4. GRUPOS, FUNÇÕES E OBJETOS ---
all_sprites = pygame.sprite.Group()
plataforms_group = pygame.sprite.Group()
honey_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
boss_group = pygame.sprite.GroupSingle()
stingers_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()

player = Player()
mangueira_sprite = None

def draw_multiline_text(surface, text, font, color, rect):
    lines = text.splitlines()
    y = rect.y
    for line in lines:
        line_surface = font.render(line, True, color)
        surface.blit(line_surface, (rect.x, y))
        y += font.get_linesize()

def draw_background(surface, camera_offset, image_list):
    surface.fill((93, 226, 231))
    
    scroll_speed = 0.2
    for layer in image_list:
        layer_width = layer.get_width()
        tiles_needed = (surface.get_width() // layer_width) + 2
        scroll_offset = -(camera_offset * scroll_speed) % layer_width

        for i in range(tiles_needed):
            surface.blit(layer, (scroll_offset + (i * layer_width) - layer_width, 0))
        
        scroll_speed += 0.15

def draw_lives(surface, current_lives, total_lives, full_img, empty_img):
    for i in range(total_lives):
        x_pos = 10 + i * (full_img.get_width() + 5)
        if i < current_lives:
            surface.blit(full_img, (x_pos, 10))
        else:
            surface.blit(empty_img, (x_pos, 10))

def setup_level():
    all_sprites.empty()
    plataforms_group.empty()
    honey_group.empty()
    enemies_group.empty()
    boss_group.empty() 
    stingers_group.empty()
    water_group.empty()

    all_sprites.add(player)
    player.rect.x, player.rect.y = 100, 300
    # Acessando atributos "privados" do player aqui, mas é dentro do contexto de setup do jogo.
    player._health, player._invincible, player._velocity_y = player._total_health, False, 0 

    npc = Npc(100, chao_y, npc_img) # Cria o NPC na posição x=100, no chão
    all_sprites.add(npc)

    for x, y, w, h in platform_map: 
        plat = Plataform(x, y, w, h, grass_tile_img, dirt_tile_img)
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
    global mangueira_sprite
    all_sprites.empty(); plataforms_group.empty(); honey_group.empty()
    enemies_group.empty(); stingers_group.empty(); water_group.empty()
    
    all_sprites.add(player)
    boss = Boss(); all_sprites.add(boss); boss_group.add(boss)
    
    chao_y_boss = game_surface.get_height() - 40
    chao = Plataform(0, chao_y_boss, game_surface.get_width(), 40, grass_tile_summer_img, dirt_tile_summer_img)
    all_sprites.add(chao)
    plataforms_group.add(chao)
    
    mangueira_x_pos = game_surface.get_width() / 2 - 200
    mangueira_sprite = Mangueira(mangueira_x_pos, chao_y_boss)
    all_sprites.add(mangueira_sprite)
    
    player.rect.x, player.rect.bottom, player._velocity_y = 100, chao_y_boss, 0
    
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
        # --- Eventos Globais (Fechar, Reiniciar, Começar) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                gameLoop = False
            
            # Evento para iniciar o jogo a partir da intro
            if game_state == 'intro' and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = 'level_1'

            # Evento para reiniciar o jogo a partir do game over
            if game_state == 'game_over' and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    honey_score = 0
                    game_state = 'level_1'
                    total_honey = setup_level()
                    boss_level_setup_done = False
                    pygame.mixer.music.load(level1_music_path)
                    pygame.mixer.music.play(loops=-1)
        
        # Pega as teclas pressionadas uma vez por frame
        keys = pygame.key.get_pressed()

        # --- ESTRUTURA DE ESTADOS CORRIGIDA (if/elif) ---
        
        if game_state == 'intro':
            # Na intro, a lógica do jogo não roda, apenas o desenho.

            # 1. Desenha o fundo e os sprites "congelados" no game_surface
            draw_background(game_surface, camera_x, background_images)
            for sprite in all_sprites:
                screen_rect = sprite.rect.copy()
                screen_rect.x -= int(camera_x)
                game_surface.blit(sprite.image, screen_rect)
            
            # 2. Escala o game_surface para a tela principal (para criar o efeito de fundo)
            scaled_surface = pygame.transform.scale(game_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
            display.blit(scaled_surface, (0, 0))

            # 3. Desenha a interface da intro POR CIMA da tela principal
            smoke_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            smoke_overlay.fill((0, 0, 0, 180))
            display.blit(smoke_overlay, (0, 0))
            
            dialog_rect = pygame.Rect(SCREEN_WIDTH/2 - 340, SCREEN_HEIGHT - 280, 850, 250)
            pygame.draw.rect(display, (50, 50, 50), dialog_rect)
            pygame.draw.rect(display, (255, 255, 255), dialog_rect, 3)
            
            instructions = ("Bem-vindo, Jogador!\nUse A/D para mover, W para pular.\nColete todo o mel para lutar contra a Abelha Rainha!\nAperte E para acionar a mangueira.\n\nPressione ESPAÇO para começar.")
            draw_multiline_text(display, instructions, game_font, (255, 255, 255), dialog_rect.inflate(-20, -20))

        elif game_state == 'level_1':
            all_sprites.update(plataforms_group)
            
            if pygame.sprite.spritecollide(player, honey_group, True):
                honey_score += 1; collect_sound.play()
            
            if not player._invincible:
                enemy_hits = pygame.sprite.spritecollide(player, enemies_group, False, pygame.sprite.collide_mask)
                if enemy_hits:
                    enemy = enemy_hits[0]
                    player._invincible, player._hurt_time = True, pygame.time.get_ticks()
                    player._health -= 1; hurt_sound.play()
                    player.rect.x += -player._knockback_strength if player.rect.centerx < enemy.rect.centerx else player._knockback_strength
                    player._velocity_y = -8
            
            target_camera_x = player.rect.centerx - (game_surface.get_width() / 2)
            camera_x += (target_camera_x - camera_x) * camera_smoothing
            if camera_x < 0: camera_x = 0
            if camera_x > level_width - game_surface.get_width(): camera_x = level_width - game_surface.get_width()
            
            if honey_score >= total_honey:
                game_state = 'boss_level'
                pygame.mixer.music.load(boss_music); pygame.mixer.music.play(loops=-1)
            if player._health <= 0: game_state = 'game_over'
            
            # Desenho da Fase 1
            draw_background(game_surface, camera_x, background_images)
            for sprite in all_sprites:
                screen_rect = sprite.rect.copy()
                screen_rect.x -= int(camera_x)
                game_surface.blit(sprite.image, screen_rect)
            
            scaled_surface = pygame.transform.scale(game_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
            display.blit(scaled_surface, (0, 0))
            
            # Acessando _health para desenhar na tela
            draw_lives(display, player._health, player._total_health, full_heart_img, empty_heart_img) 
            
            honey_y_pos = 55 
            display.blit(honey_pot_ui_img, (10, honey_y_pos))
            honey_text = game_font.render(f'{honey_score}/{total_honey}', True, (255, 255, 255))
            text_x_pos = 10 + honey_pot_ui_img.get_width() + 10
            text_y_pos = honey_y_pos + (honey_pot_ui_img.get_height() / 2) - (honey_text.get_height() / 2)
            display.blit(honey_text, (text_x_pos, text_y_pos))

        elif game_state == 'boss_level':
            if not boss_level_setup_done:
                setup_boss_level(); boss_level_setup_done = True
            
            if mangueira_sprite and keys[pygame.K_e] and player.rect.colliderect(mangueira_sprite.rect):
                water = Water(mangueira_sprite.rect.centerx, mangueira_sprite.rect.top)
                all_sprites.add(water); water_group.add(water)
            
            player.update(plataforms_group); boss_group.update(all_sprites, stingers_group)
            stingers_group.update(); water_group.update()
            
            if not player._invincible and pygame.sprite.spritecollide(player, stingers_group, True, pygame.sprite.collide_mask):
                player._invincible, player._hurt_time = True, pygame.time.get_ticks()
                player._health -= 1; hurt_sound.play()
                player._velocity_y = -8
            
            if boss_group.sprite:
                if pygame.sprite.groupcollide(water_group, boss_group, True, False, pygame.sprite.collide_mask):
                    # health do boss é publico pois é diretamente afetado por uma ação do jogador (atingido pela água)
                    boss_group.sprite.health -= 1 
            
            if player._health <= 0: game_state = 'game_over'
            if boss_group.sprite and boss_group.sprite.health <= 0: game_state = 'you_win'
            
            draw_background(game_surface, 0, boss_background_images)
            all_sprites.draw(game_surface)
            scaled_surface = pygame.transform.scale(game_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
            display.blit(scaled_surface, (0, 0))
            
            # Acessando _health para desenhar na tela
            draw_lives(display, player._health, player._total_health, full_heart_img, empty_heart_img)
            if boss_group.sprite:
                boss_health_text = game_font.render(f'Vida Chefe: {boss_group.sprite.health}', True, (255, 255, 0))
                display.blit(boss_health_text, (SCREEN_WIDTH - 300, 10))
        
        elif game_state in ['game_over', 'you_win']:
            is_game_over = game_state == 'game_over'
            display.fill((0,0,0) if is_game_over else (255,255,255))
            text_content, text_color = ("GAME OVER", (255,0,0)) if is_game_over else ("VOCÊ VENCEU!", (0,200,0))
            text = game_font.render(text_content, True, text_color)
            rect = text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - (20 if is_game_over else 0)))
            display.blit(text, rect)
            if is_game_over:
                text2 = game_font.render("Pressione R para reiniciar", True, (255, 255, 255))
                rect2 = text2.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20))
                display.blit(text2, rect2)
        
        # Atualiza a tela inteira uma vez no final do loop
        pygame.display.update()
        clock.tick(60)

pygame.quit()
