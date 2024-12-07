import pygame
import random

pygame.init()

width, height = 600, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Generator")

Entry = int(input("Number of grid columns: "))
w = width // Entry
# w = 100

cols = width // w
rows = height // w
grid = []
stack = []
current = None

class Cell:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.walls = [True, True, True, True]
        self.visited = False

    def check_neighbors(self):
        neighbors = []

        top_index = index(self.i, self.j - 1)
        right_index = index(self.i + 1, self.j)
        bottom_index = index(self.i, self.j + 1)
        left_index = index(self.i - 1, self.j)

        if top_index is not None and not grid[top_index].visited:
            neighbors.append(grid[top_index])
        if right_index is not None and not grid[right_index].visited:
            neighbors.append(grid[right_index])
        if bottom_index is not None and not grid[bottom_index].visited:
            neighbors.append(grid[bottom_index])
        if left_index is not None and not grid[left_index].visited:
            neighbors.append(grid[left_index])

        if neighbors:
            return random.choice(neighbors)
        else:
            return None

    def show(self, win):
        x = self.i * w
        y = self.j * w
        if self.walls[0]:
            pygame.draw.line(win, (255, 255, 255), (x, y), (x + w, y))
        if self.walls[1]:
            pygame.draw.line(win, (255, 255, 255), (x + w, y), (x + w, y + w))
        if self.walls[2]:
            pygame.draw.line(win, (255, 255, 255), (x + w, y + w), (x, y + w))
        if self.walls[3]:
            pygame.draw.line(win, (255, 255, 255), (x, y + w), (x, y))

        if self.visited:
            pygame.draw.rect(win, (0, 0, 0), (x, y, w, w), 0)

def index(i, j):
    if i < 0 or j < 0 or i >= cols or j >= rows:
        return None
    return i + j * cols

def remove_walls(a, b):
    dx = a.i - b.i
    if dx == 1:
        a.walls[3] = False
        b.walls[1] = False
    elif dx == -1:
        a.walls[1] = False
        b.walls[3] = False

    dy = a.j - b.j
    if dy == 1:
        a.walls[0] = False
        b.walls[2] = False
    elif dy == -1:
        a.walls[2] = False
        b.walls[0] = False

for j in range(rows):
    for i in range(cols):
        cell = Cell(i, j)
        grid.append(cell)

current = grid[0]

run = True
while run:
    # pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    win.fill((255, 0, 0))
    for cell in grid:
        cell.show(win)

    current.visited = True
    next_cell = current.check_neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append(current)
        remove_walls(current, next_cell)
        current = next_cell
    elif stack:
        current = stack.pop()

    if not stack and current == grid[0]:
        run = False

    pygame.display.update()

for cell in grid:
    cell.visited = False
    cell.show(win)
    if cell == grid[0]:
        pygame.draw.circle(win, (255, 0, 0), (cell.i * w + w // 2, cell.j * w + w // 2), w // 4)
    pygame.display.update()

    if cell == grid[-1]:
        pygame.draw.circle(win, (0, 255, 0), (cell.i * w + w // 2, cell.j * w + w // 2), w // 4)
    pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
