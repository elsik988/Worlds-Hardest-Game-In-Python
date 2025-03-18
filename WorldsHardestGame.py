import pygame
import sys
import random

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("World's Hardest Game - Image Edition")

# Colores
WHITE = (255, 255, 255)

# Cargar imágenes
player_img = pygame.image.load("player.png")
killbrick_img = pygame.image.load("killbrick.png")
point_img = pygame.image.load("point.png")
victory_img = pygame.image.load("victory.png")
wall_img = pygame.image.load("wall.png")

# Cargar sonidos
sound_death = pygame.mixer.Sound("death.mp3")
sound_victory = pygame.mixer.Sound("victory.mp3")
sound_point = pygame.mixer.Sound("point.mp3")
game_music = "game_music.mp3"
pygame.mixer.music.load(game_music)
pygame.mixer.music.play(-1)

# Variables globales
level_difficulty = 1
default_level_data = None
killbricks = []  

def points_required():
    return len(points) == 0

def find_safe_spawn():
    for _ in range(100):
        x, y = random.randint(50, 750), random.randint(50, 550)
        new_rect = pygame.Rect(x, y, 30, 30)
        if not any(new_rect.colliderect(k.rect) for k in killbricks):
            return x, y
    return 50, 50  

def generate_level():
    global player, victory, killbricks, points, walls, level_difficulty, default_level_data
    spawn_x, spawn_y = find_safe_spawn()
    player = Player(spawn_x, spawn_y)
    victory = Victory(750, 275)
    num_killbricks = min(3 + level_difficulty, 10)
    num_points = max(2 - (level_difficulty // 5), 1)
    killbricks = [KillBrick(random.randint(100, 700), random.randint(100, 500), random.choice([-2, 2]) * level_difficulty) for _ in range(num_killbricks)]
    points = [Point(random.randint(100, 700), random.randint(100, 500)) for _ in range(num_points)]
    walls = [
        Wall(0, 0, WIDTH, 20),  # Pared superior
        Wall(0, HEIGHT - 20, WIDTH, 20),  # Pared inferior
        Wall(0, 0, 20, HEIGHT),  # Pared izquierda
        Wall(WIDTH - 20, 0, 20, HEIGHT)  # Pared derecha
    ]
    default_level_data = (player, victory, killbricks, points, walls)
    level_difficulty += 1

def reset_level():
    global player
    spawn_x, spawn_y = find_safe_spawn()
    player.rect.x, player.rect.y = spawn_x, spawn_y

def render_image(image, size):
    return pygame.transform.scale(image, size)

# Clase del jugador
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.speed = 4
        self.image = render_image(player_img, (30, 30))
    
    def move(self, keys):
        old_x, old_y = self.rect.x, self.rect.y  

        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        
        # Verificar colisión con paredes
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.x, self.rect.y = old_x, old_y  # Revertir movimiento

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

# Clase de la meta
class Victory:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.image = render_image(victory_img, (40, 40))
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

# Clase de los killbricks
class KillBrick:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.image = render_image(killbrick_img, (30, 30))
        self.speed = speed
    
    def move(self):
        self.rect.x += self.speed
        if self.rect.x <= 20 or self.rect.x >= WIDTH - 50:
            self.speed *= -1
    
    def draw(self, screen):
        self.move()
        screen.blit(self.image, (self.rect.x, self.rect.y))

# Clase de los puntos
class Point:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.image = render_image(point_img, (20, 20))
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

# Clase de las paredes
class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = render_image(wall_img, (width, height))
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

# Generar primer nivel
generate_level()

# Bucle principal
running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    player.move(keys)
    
    player.draw(screen)
    victory.draw(screen)
    
    for killbrick in killbricks:
        killbrick.draw(screen)
        if player.rect.colliderect(killbrick.rect):
            sound_death.play()
            pygame.time.delay(1000)
            reset_level()
    
    for point in points[:]:
        point.draw(screen)
        if player.rect.colliderect(point.rect):
            sound_point.play()
            points.remove(point)
    
    for wall in walls:
        wall.draw(screen)
    
    if player.rect.colliderect(victory.rect) and points_required():
        sound_victory.play()
        pygame.time.delay(2000)
        generate_level()
    
    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
sys.exit()
