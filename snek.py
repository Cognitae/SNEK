import pygame
import time
import random
from collections import namedtuple # I will use namedtuple to represent fruits

# Set up some constants
SNAKE_SIZE = 10
SNAKE_SPEED = 15
WIDTH = 600  # width of the game window
HEIGHT = 400  # height of the game window
WIDTH = WIDTH // SNAKE_SIZE * SNAKE_SIZE  # This ensures that WIDTH is a multiple of SNAKE_SIZE
HEIGHT = HEIGHT // SNAKE_SIZE * SNAKE_SIZE  # This ensures that HEIGHT is a multiple of SNAKE_SIZE
FONT_SIZE = 18

# Colors
GRAY = (34, 34, 34) # Background Color
GREEN = (0, 255, 0) # Snek Color
RED = (255, 0, 0) # Fruit Color
WHITE = (255, 255, 255)    # Text Color
BLACK = (0, 0, 0)  # placeholder color
GOLD = (255, 215, 0) # Rare gold fruit (1/100 chance)
BLUE = (0, 115, 207)  # New color for special fruit

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('No Step on SNEK!!!') 

# Load a font
FONT = pygame.font.Font(None, FONT_SIZE)

# Render the first line of instructions
line1 = FONT.render('No sTeP oN Sn3k!!!!!!', True, WHITE)

# Render the second line of instructions
line2 = FONT.render('Press SPACEBAR to start!', True, WHITE)

# Blit the first line on the window, centered horizontally and slightly above the middle vertically
WINDOW.blit(line1, (WIDTH // 2 - line1.get_width() // 2, HEIGHT // 2 - line1.get_height() - 10))

# Blit the second line on the window, centered horizontally and slightly below the middle vertically
WINDOW.blit(line2, (WIDTH // 2 - line2.get_width() // 2, HEIGHT // 2 + 10))
pygame.display.update()

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

# Create a namedtuple to represent fruits
Fruit = namedtuple('Fruit', ['position', 'type'])

def draw_fruit(fruit):
    if fruit.type == 'GOLDEN':
        color = GOLD
    elif fruit.type == 'SPECIAL':
        color = BLUE
    else:  # 'NORMAL'
        color = RED
    pygame.draw.rect(WINDOW, color, pygame.Rect(fruit.position[0], fruit.position[1], SNAKE_SIZE, SNAKE_SIZE))


def check_collision(snake, fruit):
    # Check if the head of the snake is within the fruit rectangle
    head_rect = pygame.Rect(snake[0][0], snake[0][1], SNAKE_SIZE, SNAKE_SIZE)
    fruit_rect = pygame.Rect(fruit.position[0], fruit.position[1], SNAKE_SIZE, SNAKE_SIZE)
    return head_rect.colliderect(fruit_rect)

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
    all_positions = [[x, y] for x in range(0, WIDTH, SNAKE_SIZE) for y in range(0, HEIGHT, SNAKE_SIZE)]
    free_positions = [pos for pos in all_positions if pos not in snake]
    position = random.choice(free_positions)
    random_number = random.random()  # Generate a random number between 0 and 1
    if random_number < 0.01:  # 1% chance the fruit is golden
        fruit_type = 'GOLDEN'
    elif random_number < 0.11:  # 10% chance the fruit is special (but not golden)
        fruit_type = 'SPECIAL'
    else:  # 89% chance the fruit is normal
        fruit_type = 'NORMAL'
    return Fruit(position, fruit_type)  # Return the fruit with its type


# Initialize the high score    
high_score = 0

def game_over_screen(score):
    # Check if the current score is higher than the high score
    global high_score
    new_high_score = False
    if score > high_score:
        high_score = score
        new_high_score = True

    # Clear the screen
    WINDOW.fill(GRAY)

    lines = [f'GAME OVER', f'Score: {score}', f'High Score: {high_score}', 'Press SPACEBAR Three Times to play again or Q to quit']
    
    if new_high_score:
        lines.insert(1, "New High Score! Congratulations!")
    
    for i, line in enumerate(lines):
        text = FONT.render(line, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * FONT_SIZE))
        WINDOW.blit(text, text_rect)

    # Update the display
    pygame.display.update()

    # Wait for a SPACE keypress
   # Wait for a SPACE keypress
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_q:  # Check if 'q' is pressed
                    pygame.quit()
                    return False  # Return False when 'q' is pressed
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

# Initialize the game speed
game_speed = SNAKE_SPEED

def waiting_screen():
    # Clear the screen
    WINDOW.fill(GRAY)

    # Render a line of instructions
    line = FONT.render('Press SPACEBAR to start next game!', True, WHITE)

    # Blit the line on the window, centered horizontally and slightly above the middle vertically
    WINDOW.blit(line, (WIDTH // 2 - line.get_width() // 2, HEIGHT // 2 - line.get_height() - 10))

    # Update the display
    pygame.display.update()

    # Wait for a SPACE keypress
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True
            if event.type == pygame.QUIT:
                pygame.quit()
                return False


def game_loop():
     # Initialize the score
    score = 0
    # Set up the initial game state
    snake = [[300, 150], [90, 50], [80, 50]]
    direction = 'RIGHT'
    fruit = generate_fruit(snake)
    score = 0  # Initialize score
    global game_speed  # Initialize game speed
    game_speed = SNAKE_SPEED  # Reset game speed

    clock = pygame.time.Clock()
    game_started = False
    play_again = False  # Add this line

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_started:
                        game_started = False  # If game is running, pause it
                    elif play_again:
                        return True  # If game is over, start a new game
                    else:
                        game_started = True  # If game is paused, resume it
                if event.key == pygame.K_q:
                    return False  # If 'q' is pressed, quit the game

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
            # Move the snake according to the direction
            move_snake(snake, direction)

            if check_collision(snake, fruit):
                # Increase the score
                if fruit.type == 'GOLDEN':
                    score += 100
                elif fruit.type == 'SPECIAL':
                    score += 5
                else:  # 'NORMAL'
                    score += 1
                # Generate new fruit and don't remove the tail of the snake, so it grows
                fruit = generate_fruit(snake)
                # Adjust game speed based on the score
                game_speed = SNAKE_SPEED + (score // 50) * 5
            else:
                # If the snake didn't eat the fruit, move as normal by removing the last segment
                snake.pop()
                
            # Check for game over
            if check_game_over(snake):
                play_again = game_over_screen(score)  # Pass the score to the game over screen
                if not play_again:
                    return  # Exit the game loop if player doesn't want to play again
                else:
                    game_started = False  # Game is over, so it's not currently started
                    snake = [[300, 150], [90, 50], [80, 50]]  # Reset the snake
                    direction = 'RIGHT'  # Reset the direction
                    fruit = generate_fruit(snake)  # Generate a new fruit
                    score = 0  # Reset the score
            else:
                play_again = False  # If game is not over, reset play_again flag

            # Draw everything
            WINDOW.fill(GRAY)
            draw_snake(snake)
            draw_fruit(fruit)
            
            # Display the score
            score_text = FONT.render(f'Score: {score}', True, WHITE)
            WINDOW.blit(score_text, (10, 10))  # Display the score at the top left corner
            
            pygame.display.update()
            clock.tick(game_speed)  # Use the variable game speed here

if __name__ == "__main__":
    while True:  # Keep playing games until player wants to quit
        play_again = game_loop()
        if not play_again:
            pygame.quit()  # Quit the game when player doesn't want to play again
            break
