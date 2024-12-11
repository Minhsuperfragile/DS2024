import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 540, 540
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (173, 216, 230)
RED = (255, 102, 102)
GREEN = (0, 255, 0)

# Fonts
FONT = pygame.font.Font(None, 40)
LARGE_FONT = pygame.font.Font(None, 80)

# Grid configuration
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE

# Initial Sudoku grid (0 represents empty cells)
GRID = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]

# Track cells that are editable (initially 0)
EDITABLE_CELLS = [[GRID[row][col] == 0 for col in range(GRID_SIZE)] for row in range(GRID_SIZE)]

def draw_grid():
    """Draws the Sudoku grid."""
    for row in range(GRID_SIZE + 1):
        line_width = 3 if row % 3 == 0 else 1
        pygame.draw.line(SCREEN, BLACK, (0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE), line_width)
        pygame.draw.line(SCREEN, BLACK, (row * CELL_SIZE, 0), (row * CELL_SIZE, HEIGHT), line_width)

def draw_numbers():
    """Draws the numbers on the grid."""
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if GRID[row][col] != 0:
                text = FONT.render(str(GRID[row][col]), True, BLACK)
                SCREEN.blit(text, (col * CELL_SIZE + 20, row * CELL_SIZE + 10))

def highlight_cell(row, col, color):
    """Highlights the selected cell with a specific color."""
    pygame.draw.rect(SCREEN, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def is_valid_input(grid, row, col, num):
    """Checks if the number already exists in the row or column."""
    # Check row
    if num in grid[row]:
        return False
    # Check column
    for r in range(GRID_SIZE):
        if grid[r][col] == num:
            return False
    return True

def is_grid_full(grid):
    """Checks if the grid is completely filled."""
    for row in grid:
        if 0 in row:
            return False
    return True

def display_congratulations():
    """Displays a congratulation message."""
    text = LARGE_FONT.render("Congratulations!", True, GREEN)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    SCREEN.blit(text, text_rect)

def main():
    selected_cell = None
    invalid_input = False
    running = True
    game_won = False

    while running:
        SCREEN.fill(WHITE)
        draw_grid()

        if selected_cell:
            row, col = selected_cell
            if EDITABLE_CELLS[row][col]:  # Only highlight editable cells
                highlight_cell(row, col, RED if invalid_input else BLUE)

        draw_numbers()

        # Check for game completion
        if is_grid_full(GRID) and not game_won:
            game_won = True

        if game_won:
            display_congratulations()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_won:
                x, y = pygame.mouse.get_pos()
                selected_cell = (y // CELL_SIZE, x // CELL_SIZE)
                invalid_input = False  # Reset invalid state
            elif event.type == pygame.KEYDOWN and selected_cell and not game_won:
                row, col = selected_cell
                if EDITABLE_CELLS[row][col]:  # Only process input for editable cells
                    if event.key in range(pygame.K_1, pygame.K_9 + 1):  # Keys 1 to 9
                        num = event.key - pygame.K_0
                        if is_valid_input(GRID, row, col, num):
                            GRID[row][col] = num
                            invalid_input = False
                        else:
                            invalid_input = True
                    elif event.key == pygame.K_BACKSPACE:  # Clear cell with BACKSPACE
                        GRID[row][col] = 0
                        invalid_input = False

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
