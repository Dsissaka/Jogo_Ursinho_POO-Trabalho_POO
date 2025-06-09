import pygame

# --- Definição das Classes ---

# Nossa nova classe Player herda de pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Inicializador da classe Sprite 
        super().__init__()

        # Criando a imagem do player
        self.image = pygame.Surface([40, 60])
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
            self.on_ground = True # Tocou no chão, pode pular de novo

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



# --- Início do Jogo ---

pygame.init()

display = pygame.display.set_mode([840, 480])
pygame.display.set_caption('Ursinho POO')
clock = pygame.time.Clock()

# --- Criação dos Objetos e Grupos ---

# criar chão visualmente
ground_rect = pygame.Rect(0, 440, 840, 40) # x, y, largura, altura

# "Grupos de Sprites" são como listas especiais para organizar e
# gerenciar múltiplos objetos de uma só vez.
all_sprites = pygame.sprite.Group()
plataforms_group = pygame.sprite.Group() # novo grupo, só para as plataformas
#criando grupo do mel:
honey_group = pygame.sprite.Group() # novo grupo só pro mel

# Agora, em vez de criar um rect, nós criamos um objeto da nossa classe Player
player = Player()
all_sprites.add(player) # Adicionamos nossa instância do jogador ao grupo

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

        # --- Desenho ---
        display.fill((93, 226, 231))
        pygame.draw.rect(display, (34, 139, 34), ground_rect) # Desenha o chão verde
        # o .draw() desenha TODOS os sprites do grupo na tela
        all_sprites.draw(display)
        
        pygame.display.update()
        clock.tick(60)

pygame.quit()