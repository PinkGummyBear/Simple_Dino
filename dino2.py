import pygame
import random
import sys

# Constants
WIDTH, HEIGHT = 800, 400
GRAVITY = 0.6
JUMP_SPEED = -10
OBSTACLE_WIDTH = 30
OBSTACLE_HEIGHT = 50
GROUND_HEIGHT = HEIGHT - 40
FPS = 70
SCORE_INCREMENT_INTERVAL = 10  # Increase score every 10 frames
OBSTACLE_BASE_SPEED = 5
OBSTACLE_SPEED_INCREMENT = 2
OBSTACLE_DISTANCE = 100  # Initial distance between obstacles
FONT_NAME = pygame.font.match_font('arial')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player class
class Dinosaur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = GROUND_HEIGHT - self.rect.height
        self.velocity = 0
        self.jumping = False
        self.jump_duration = 0  # Track jump duration

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.bottom > GROUND_HEIGHT:
            self.rect.bottom = GROUND_HEIGHT
            self.velocity = 0
            self.jumping = False

    def jump(self):
        if not self.jumping:
            self.velocity = JUMP_SPEED
            self.jumping = True

    def long_jump(self):
        if not self.jumping:
            self.velocity = JUMP_SPEED * 1.5  # Adjust jump speed for long jump
            self.jumping = True

    def start_jump_timer(self):
        self.jump_duration = pygame.time.get_ticks()

    def end_jump_timer(self):
        return pygame.time.get_ticks() - self.jump_duration

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, speed):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = GROUND_HEIGHT - self.rect.height
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# Start menu function
def show_start_screen(screen):
    screen.fill(BLACK)
    draw_text(screen, "Chrome Dinosaur Game", 64, WHITE, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Press any key to start", 32, WHITE, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

# Draw text function
def draw_text(surface, text, size, color, x, y):
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Initialize game function
def initialize_game(player, all_sprites, obstacles):
    player.rect.x = 50
    player.rect.y = GROUND_HEIGHT - player.rect.height
    player.velocity = 0
    player.jumping = False
    all_sprites.empty()
    obstacles.empty()

# Main game function
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chrome Dinosaur Game")
    clock = pygame.time.Clock()

    show_start_screen(screen)

    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    player = Dinosaur()
    all_sprites.add(player)

    next_obstacle_x = WIDTH
    score = 0
    score_increment_counter = 0
    obstacle_speed = OBSTACLE_BASE_SPEED

    font = pygame.font.Font(None, 36)

    running = True
    game_over = False
    high_score = 0  # Initialize high score
    while running:
        if game_over:
            if score > high_score:  # Update high score if necessary
                high_score = score
            pygame.time.delay(1000)  # Delay for 1 second before restarting
            show_start_screen(screen)
            game_over = False
            initialize_game(player, all_sprites, obstacles)
            score = 0
            next_obstacle_x = WIDTH
            obstacle_speed = OBSTACLE_BASE_SPEED

       # Inside the main game loop, handle key events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                elif event.key == pygame.K_l:  # Key for long jump
                    player.long_jump()
                elif event.key == pygame.K_r:
                    game_over = True


        # Generate obstacles
        if pygame.time.get_ticks() > next_obstacle_x:
            obstacle = Obstacle(WIDTH, obstacle_speed)
            obstacles.add(obstacle)
            all_sprites.add(obstacle)
            next_obstacle_x += OBSTACLE_DISTANCE / obstacle_speed * FPS

        # Update
        all_sprites.update()

        # Check for collisions
        hits = pygame.sprite.spritecollide(player, obstacles, False)
        if hits:
            running = False  # End the game if collision happens

        # Increase score at intervals
        score_increment_counter += 1
        if score_increment_counter >= SCORE_INCREMENT_INTERVAL:
            score += 1
            score_increment_counter = 0

            # Increase obstacle speed every time score reaches a multiple of 100
            if score % 100 == 0:
                obstacle_speed += OBSTACLE_SPEED_INCREMENT

        # Draw
        screen.fill(BLACK)
        
        # Draw a line representing the ground
        pygame.draw.line(screen, WHITE, (0, GROUND_HEIGHT), (WIDTH, GROUND_HEIGHT), 3)
        
        obstacles.draw(screen)  # Draw obstacles before player
        all_sprites.draw(screen)  # Draw player on top of obstacles

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
