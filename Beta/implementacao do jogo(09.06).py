import pygame

# --- Definição das Classes ---

# Nossa nova classe Player herda de pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Inicializador da classe Sprite 
        super().__init__()

        # Criando a imagem do player
        self.image = pygame.Surface([40, 60]).convert()
        self.image.fill((255, 165, 0))
        self.rect = self.image.get_rect() #hitbox, o pygame pega as dimensões da self.image automaticamente
        # Posicionando o jogador
        self.rect.x = 100
        self.rect.y = 300
        # Variáveis específicas do jogador
        self.speed = 5
        # variáveis de física
        self.velocity_y = 0
        self.gravity = 0.8 # força da gravidade que puxa pra baixo
        self.jump_strength = -18 # força do pulo
        self.on_ground = False # saiu do chã0, ent nao pode pular dnv
        self.health = 3 # vida
        # Variaveis do Knockback:
        self.invincible = False
        self.invinciblity_duration = 1500 # duração em milissegundos(1.5s)
        self.hurt_time = 0
        self.knockback_strength = 40

    # A função update será chamada a cada frame
    def update(self, plataforms_group):
        # Move o jogador baseado nas teclas pressionadas
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        # pulo do player
        if keys[pygame.K_w] and self.on_ground: # player só pula se estiver no chão
            self.velocity_y = self.jump_strength
            self.on_ground = False 

        # Gravidade:
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        
        # Detectação do chão:
       
        if self.rect.bottom >= 440: # Usar .bottom é mais preciso
            self.rect.bottom = 440
            self.velocity_y = 0
            self.on_ground = True # Tocou no chão, pode pular de novoa

        # Detecção com Plataformas:
        # Verifique se o jogador está caindo (velocidade positiva)
        if self.velocity_y > 0:
            # A função retorna uma lista de plataformas com as quais colidimos
            hits = pygame.sprite.spritecollide(self, plataforms_group, False)
            if hits:
                # Se colidiu, pega a primeira plataforma da lista (hits[0])
                # e ajusta a posição do jogador para ficar em cima dela.
                self.rect.bottom = hits[0].rect.top
                self.velocity_y = 0
                self.on_ground = True
        # Implementação do Knockback
        if self.invincible:
            current_time = pygame.time.get_ticks()
            self.image.set_alpha(100 if (current_time // 100) % 2 == 0 else 255) # efeito de piscar

            if current_time - self.hurt_time > self.invinciblity_duration:
                self.invincible = False
                self.image.set_alpha(255) # garante que o player volte normal


#Classe da plataforma
class Plataform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h): #dimensões e posição
        super().__init__()
        self.image = pygame.Surface([w,h]) #criando a plataforma
        self.image.fill([139, 69, 19])# as cores dela
        #criando o hitbox dela:
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Classe do Mel
class Honey(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill([255, 215, 0])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type):
        super().__init__()
        self.enemy_type = enemy_type
        if self.enemy_type == 'bear':
            # Configurações do Urso
            self.image = pygame.Surface([35, 50])
            self.image.fill((88, 41, 0)) # Marrom escuro
            self.speed_x = 2
            self.speed_y = 0
        elif self.enemy_type == 'bee':
            # Configurações da Abelha
            self.image = pygame.Surface([30, 25])
            self.image.fill((255, 255, 0)) # Amarelo
            self.speed_x = 0
            self.speed_y = 2

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        # Movimento Horizontal para o Urso
        if self.enemy_type == 'bear':
            self.rect.x += self.speed_x
            # Inverte a direção se atingir as bordas da tela
            if self.rect.right > 840 or self.rect.left < 0:
                self.speed_x *= -1
        
        # Movimento Vertical para a Abelha
        elif self.enemy_type == 'bee':
            self.rect.y += self.speed_y
            # Inverte a direção se atingir o topo ou a base da área de jogo
            if self.rect.bottom > 440 or self.rect.top < 0: # 440 é o nosso chão
                self.speed_y *= -1

# --- Início do Jogo ---

pygame.init()

# criando uma fonte para o placar
game_font = pygame.font.Font(None, 36) # fonte padrão, tam.36

display = pygame.display.set_mode([840, 480])
pygame.display.set_caption('Ursinho POO')
clock = pygame.time.Clock()

# --- Criação dos Objetos e Grupos ---

ground_rect = pygame.Rect(0, 440, 840, 40)
all_sprites = pygame.sprite.Group(); plataforms_group = pygame.sprite.Group()
honey_group = pygame.sprite.Group(); enemies_group = pygame.sprite.Group()
honey_score = 0; player = Player(); all_sprites.add(player)

# Cria o urso
enemy1 = Enemy(x=300, y=440 - 50, enemy_type='bear')
all_sprites.add(enemy1); enemies_group.add(enemy1)

# Cria a abelha
bee1 = Enemy(x=700, y=200, enemy_type='bee')
all_sprites.add(bee1); enemies_group.add(bee1)

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
honey1 = Honey(x=250, y=325) # Em cima da plat1
honey2 = Honey(x=500, y=255) # Em cima da plat2
honey3 = Honey(x=180, y=155) # Em cima da plat3

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
                player.health -= 1
                print(f'Atingido! vidas restanntes:{player.health}')
                enemy = enemy_hits[0]
                if player.rect.centerx < enemy.rect.centerx: player.rect.x -= player.knockback_strength
                else: player.rect.x += player.knockback_strength
                player.velocity_y = -8 # Impulso para cima

        # verificação de GAME OVERdd
        if player.health <= 0:
            print('GAME OVER!')
            gameLoop = False # Jogo encerra


        # --- Desenho ---
        display.fill((93, 226, 231))
        pygame.draw.rect(display, (34, 139, 34), ground_rect) # Desenha o chão verde
        # o .draw() desenha TODOS os sprites do grupo na tela
        all_sprites.draw(display)
        
        health_text = game_font.render(f'Vida:{player.health}', True, (255,255,255))
        display.blit(health_text, (10,10)) # posicao no canto superior esquerdo

        honey_text = game_font.render(f'Mel: {honey_score}', True,(255,255,255))
        display.blit(honey_text, (10,40))


        pygame.display.update()
        clock.tick(60)

pygame.quit()
