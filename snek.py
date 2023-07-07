import pygame
import time
import random

# Set up some constants
WIDTH = 600
HEIGHT = 600
SNAKE_SIZE = 20
SNAKE_SPEED = 15
WIDTH = 600 // SNAKE_SIZE * SNAKE_SIZE  # This ensures that WIDTH is a multiple of SNAKE_SIZE
HEIGHT = 600 // SNAKE_SIZE * SNAKE_SIZE  # This ensures that HEIGHT is a multiple of SNAKE_SIZE


# Colors
GRAY = (34, 34, 34)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)  # New color for text

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')  # Add a title to the window

# Load a font
font = pygame.font.Font(None, 36)

def draw_snake(snake):
    for unit in snake:
        pygame.draw.rect(WINDOW, GREEN, pygame.Rect(unit[0], unit[1], SNAKE_SIZE, SNAKE_SIZE))

def move_snake(snake, direction):
    if direction == 'RIGHT':
        snake.insert(0, [snake[0][0] + SNAKE_SIZE, snake[0][1]])
    elif direction == 'LEFT':
        snake.insert(0, [snake[0][0] - SNAKE_SIZE, snake[0][1]])
    elif direction == 'UP':
        snake.insert(0, [snake[0][0], snake[0][1] - SNAKE_SIZE])
    elif direction == 'DOWN':
        snake.insert(0, [snake[0][0], snake[0][1] + SNAKE_SIZE])

def draw_fruit(fruit):
    pygame.draw.rect(WINDOW, RED, pygame.Rect(fruit[0], fruit[1], SNAKE_SIZE, SNAKE_SIZE))

def check_collision(snake, fruit):
    if snake[0] == fruit:
        return True 
    return False

def check_game_over(snake):
    # Check if snake is out of bounds
    if (snake[0][0] >= WIDTH or 
        snake[0][0] < 0 or 
        snake[0][1] >= HEIGHT or 
        snake[0][1] < 0):
        return True
    # Check if snake has collided with itself
    if snake[0] in snake[1:]:
        return True
    return False

def generate_fruit(snake):
    global fruit
    while True:
        fruit = [random.randrange(0, WIDTH//SNAKE_SIZE) * SNAKE_SIZE, 
                 random.randrange(0, HEIGHT//SNAKE_SIZE) * SNAKE_SIZE]
        if fruit not in snake:
            return fruit


def game_over_screen():
    WINDOW.fill(GRAY)
    text = font.render('Game Over. Press any key to play again.', True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    WINDOW.blit(text, text_rect)
    pygame.display.update()
    
    # Wait for a key press to restart the game
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                game_loop()

def move_snake(snake, direction):
    if direction == 'RIGHT':
        snake.insert(0, [snake[0][0] + SNAKE_SIZE, snake[0][1]])
    elif direction == 'LEFT':
        snake.insert(0, [snake[0][0] - SNAKE_SIZE, snake[0][1]])
    elif direction == 'UP':
        snake.insert(0, [snake[0][0], snake[0][1] - SNAKE_SIZE])
    elif direction == 'DOWN':
        snake.insert(0, [snake[0][0], snake[0][1] + SNAKE_SIZE])

def game_loop():
    global fruit
    # Set up the initial game state
    snake = [[100, 50], [90, 50], [80, 50]]
    direction = 'RIGHT'
    fruit = [random.randrange(0, WIDTH//SNAKE_SIZE) * SNAKE_SIZE, 
             random.randrange(0, HEIGHT//SNAKE_SIZE) * SNAKE_SIZE]
    
    clock = pygame.time.Clock()
    game_started = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        new_direction = direction
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and direction != 'DOWN':
            new_direction = 'UP'
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and direction != 'UP':
            new_direction = 'DOWN'
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and direction != 'RIGHT':
            new_direction = 'LEFT'
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and direction != 'LEFT':
            new_direction = 'RIGHT'

        direction = new_direction

        if game_started:
            # Predict the next position of the snake's head
            if direction == 'RIGHT':
                new_head = [snake[0][0] + SNAKE_SIZE, snake[0][1]]
            elif direction == 'LEFT':
                new_head = [snake[0][0] - SNAKE_SIZE, snake[0][1]]
            elif direction == 'UP':
                new_head = [snake[0][0], snake[0][1] - SNAKE_SIZE]
            elif direction == 'DOWN':
                new_head = [snake[0][0], snake[0][1] + SNAKE_SIZE]

            snake.insert(0, new_head)  # Add new head to the snake

            if new_head != fruit:  # If the snake didn't eat the fruit, remove the last segment
                snake.pop() 
            else:
                fruit = generate_fruit(snake)  # If the snake did eat the fruit, generate new fruit

            if check_game_over(snake):
                game_over_screen()
                return

            WINDOW.fill(GRAY)
            draw_snake(snake)
            draw_fruit(fruit)  # Draw the fruit after checking for collisions
            pygame.display.update()
            clock.tick(SNAKE_SPEED)
        else:
            # Wait for an arrow key or WASD key to start the game
            if keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
                game_started = True


if __name__ == "__main__":
    game_loop()
