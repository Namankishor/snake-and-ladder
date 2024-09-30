import pygame
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 10
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
FONT = pygame.font.Font(None, 30)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake and Ladder")

# Dice roll function
def roll_dice():
    return random.randint(1, 6)

# Snakes and ladders
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

# Function to get (x, y) position from a number
def get_position(number):
    row = (number - 1) // GRID_SIZE
    col = (number - 1) % GRID_SIZE
    if row % 2 == 1:  # Reverse direction for every other row
        col = GRID_SIZE - 1 - col
    x = col * CELL_SIZE
    y = (GRID_SIZE - 1 - row) * CELL_SIZE
    return x, y

# Player class
class Player:
    def __init__(self, color, name):
        self.position = 1
        self.color = color
        self.name = name

    def move(self, steps):        
        self.position += steps
        if self.position in snakes:
            self.position = snakes[self.position]
        elif self.position in ladders:
            self.position = ladders[self.position]
        if self.position > 100:
            self.position = 100

    def draw(self):
        x, y = get_position(self.position)
        pygame.draw.circle(screen, self.color, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 4)

# Main game loop
def main():
    clock = pygame.time.Clock()

    # Two players, red and blue
    player1 = Player(RED, "Player 1")
    player2 = Player(BLUE, "Player 2")
    current_player = player1

    dice_value = 0
    running = True

    while running:
        screen.fill(WHITE)

        # Draw grid and numbers
        for i in range(1, 101):
            x, y = get_position(i)
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)
            text = FONT.render(str(i), True, BLACK)
            screen.blit(text, (x + 10, y + 10))

        # Draw snakes (Green lines) and ladders (Blue lines)
        for start, end in snakes.items():
            start_pos = get_position(start)
            end_pos = get_position(end)
            pygame.draw.line(screen, GREEN, (start_pos[0] + CELL_SIZE // 2, start_pos[1] + CELL_SIZE // 2),
                             (end_pos[0] + CELL_SIZE // 2, end_pos[1] + CELL_SIZE // 2), 5)

        for start, end in ladders.items():
            start_pos = get_position(start)
            end_pos = get_position(end)
            pygame.draw.line(screen, BLUE, (start_pos[0] + CELL_SIZE // 2, start_pos[1] + CELL_SIZE // 2),
                             (end_pos[0] + CELL_SIZE // 2, end_pos[1] + CELL_SIZE // 2), 5)

        # Draw players
        player1.draw()
        player2.draw()

        # Display current dice value
        dice_text = FONT.render(f"Dice: {dice_value}", True, BLACK)
        screen.blit(dice_text, (10, 10))

        # Display current player's turn
        turn_text = FONT.render(f"Turn: {current_player.name}", True, BLACK)
        screen.blit(turn_text, (400, 10))

        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dice_value = roll_dice()
                    current_player.move(dice_value)
                    if current_player.position >= 100:
                        print(f"{current_player.name} wins!")
                        running = False
                    current_player = player2 if current_player == player1 else player1

        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
  
