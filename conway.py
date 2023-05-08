import pygame
import random


pygame.init()

WIDTH = 800
HEIGHT = 600
CELL_SIZE = 20

BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)

MENU_FONT = pygame.font.SysFont('Cooper black', 30)

rows = WIDTH // CELL_SIZE
columns = HEIGHT // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
background_color = (0, 0, 0)

pygame.key.set_repeat(10)
game_clock = pygame.time.Clock()


def check_neighbours(x_pos, y_pos, grid):
    neighbour_count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            try:
                if 0 <= x_pos + i <= len(grid) and 0 <= y_pos + j <= len(grid[0]):
                    if grid[x_pos + i][y_pos + j] == 1 or grid[x_pos + i][y_pos + j] == 2:
                        neighbour_count += 1

            except IndexError:
                continue

    return neighbour_count if grid[x_pos][y_pos] != 1 else neighbour_count - 1


def finish_generation(grid):
    cell_values = {
        0: 0,  # dead
        1: 1,  # alive
        2: 0,  # about to die
        3: 1   # to become alive
    }

    alive_count = 0

    for row_index in range(len(grid)):
        for col_index in range(len(grid[0])):
            grid[row_index][col_index] = cell_values[grid[row_index][col_index]]
            if grid[row_index][col_index] == 1:
                alive_count += 1

    return grid, alive_count


def run_generation(grid):
    for row_index in range(len(grid)):
        for col_index in range(len(grid[0])):
            cell_neighbours_count = check_neighbours(row_index, col_index, grid)
            if cell_neighbours_count < 2 and grid[row_index][col_index] == 1:
                grid[row_index][col_index] = 2
            elif cell_neighbours_count == 3 and grid[row_index][col_index] == 0:
                grid[row_index][col_index] = 3
            elif cell_neighbours_count >= 4 and grid[row_index][col_index] == 1:
                grid[row_index][col_index] = 2

    return grid


def draw_grid(grid):
    for row_index in range(len(grid)):
        for col_index in range(len(grid[0])):
            if grid[row_index][col_index] == 1:
                pygame.draw.rect(screen, WHITE, (row_index*CELL_SIZE, col_index*CELL_SIZE,
                                                 CELL_SIZE, CELL_SIZE))

    for horizontal_pos in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (horizontal_pos, 0), (horizontal_pos, HEIGHT))

    for vertical_pos in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, vertical_pos), (WIDTH, vertical_pos))


def update_screen(grid):
    screen.fill(BLACK)
    draw_grid(grid)
    pygame.display.update()


def draw_button(x, y, width, height, text, color):
    pygame.draw.rect(screen, color, (x, y, width, height), 2)
    text_img = MENU_FONT.render(text, True, color)
    text_width = text_img.get_width()
    screen.blit(text_img,
                (x + width // 2 - text_width // 2,
                 y + height // 2 - text_img.get_height() // 2))

    return pygame.Rect(x, y, width, height)


def draw_custom_grid(grid):
    screen.fill(BLACK)

    pos = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed(3)[0] == 1:
        x = pos[0] // CELL_SIZE
        y = pos[1] // CELL_SIZE
        grid[x][y] = 1

    if pygame.mouse.get_pressed(3)[2] == 1:
        x = pos[0] // CELL_SIZE
        y = pos[1] // CELL_SIZE
        grid[x][y] = 0

    for row_index in range(len(grid)):
        for col_index in range(len(grid[0])):
            if grid[row_index][col_index] == 1:
                pygame.draw.rect(screen, WHITE, (row_index*CELL_SIZE, col_index*CELL_SIZE,
                                                 CELL_SIZE, CELL_SIZE))

    return grid


def generate_grid(rows, columns, chance):
    grid = [[0 for i in range(columns)] for j in range(rows)]
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            grid[row][col] = 1 if random.randint(0, chance) == 1 else 0

    return grid


def button_collision(x, y, width, height, text, pos):
    custom_button = draw_button(x, y, width, height, text, WHITE)
    if custom_button.collidepoint(pos):
        if pygame.mouse.get_pressed(3)[0] == 1:
            return text

    return 0


def draw_menu():
    screen.fill(BLACK)
    pos = pygame.mouse.get_pos()
    WIDTH = 800
    HEIGHT = 600

    selected = 0

    x_shift = WIDTH // 3
    y_shift = HEIGHT // 4

    x = 50
    y = 50
    width = WIDTH // 4
    height = HEIGHT // 6
    if selected == 0:
        selected = button_collision(x, y, width, height, 'Custom', pos)

    y += y_shift
    if selected == 0:
        selected = button_collision(x, y, width, height, 'Random Generate', pos)

    x += x_shift
    if selected == 0:
        selected = button_collision(x, y, width, height, 'Change chance', pos)

    x -= x_shift
    y += y_shift
    if selected == 0:
        selected = button_collision(x, y, width, height, 'Seeded Generation', pos)

    x += x_shift
    if selected == 0:
        selected = button_collision(x, y, width, height, 'Custom Seed', pos)

    pygame.display.update()
    return selected


def draw_text(msg, y, font_size, color):
    screen.fill(BLACK)

    font = pygame.font.Font(None, font_size)
    text = font.render(msg, True, color)
    text_rect = text.get_rect(center=(WIDTH//2, y))
    screen.blit(text, text_rect)

    pygame.display.update()


def main():
    grid = None
    user_seed = ''
    user_chance = ''
    selected = 0
    custom_seed = False
    run_custom_seed_generation = False
    custom_chance = False
    game_over = False
    generated_seed = None
    generation = 0

    while not game_over:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True

                if event.key == pygame.K_RETURN:
                    if selected == 'Custom':
                        selected = None

                    if custom_seed:
                        selected = None
                        run_custom_seed_generation = True

                    if custom_chance:
                        selected = None
                        if user_chance != '':
                            grid = generate_grid(rows, columns, int(user_chance)-1)
                        else:
                            game_over = True

            if event.type == pygame.KEYUP:
                if custom_seed:
                    if event.unicode in '0123456789':
                        user_seed += event.unicode

                if custom_chance:
                    if event.unicode in '0123456789':
                        user_chance += event.unicode

                if event.key == pygame.K_BACKSPACE:
                    user_seed = user_seed[:-1] if user_seed != '' else ''
                    user_chance = user_chance[:-1] if user_chance != '' else ''

        if selected == 0:
            selected = draw_menu()

        elif selected == 'Custom':
            if not grid:
                grid = [[0 for i in range(columns)] for j in range(rows)]
            grid = draw_custom_grid(grid)

        elif selected == 'Random Generate':
            if not grid:
                grid = generate_grid(rows, columns, 1)

        elif selected == 'Seeded Generation':
            if not generated_seed:
                generated_seed = random.randint(0, 100)
                random.seed(generated_seed)
                print(f'Generating on seed {generated_seed}')

            if not grid:
                grid = generate_grid(rows, columns, 1)

        elif selected == 'Custom Seed':
            custom_seed = True
            draw_text(f'On seed {user_seed}', HEIGHT//2, 40, WHITE)

        elif selected == 'Change chance':
            custom_chance = True
            draw_text(f'1 in {user_chance}', HEIGHT//2, 40, WHITE)

        if run_custom_seed_generation:
            try:
                user_seed = int(user_seed)
                random.seed(user_seed)

                if not grid:
                    print(f'Generating on seed {user_seed}')
                    grid = generate_grid(rows, columns, 1)

            except:
                user_seed = ''
                selected = 'Custom Seed'
                run_custom_seed_generation = False

        if grid:
            if selected != 'Custom':
                new_gen = run_generation(grid)
                grid, alive_count = finish_generation(new_gen)
                generation += 1

                if alive_count == 0:
                    game_over = True

                game_clock.tick(5)

            else:
                game_clock.tick(100)

            update_screen(grid)

        else:
            game_clock.tick(100)

        pygame.display.set_caption(f'Game of life: GENERATION {generation}')


if __name__ == '__main__':
    main()
