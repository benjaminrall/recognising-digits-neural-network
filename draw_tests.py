import pygame
import os
import random

# Constants
WIN_WIDTH = 1200
WIN_HEIGHT = 800
FRAMERATE = 240
ICON_IMG = pygame.image.load(os.path.join("imgs", "icon.png"))

# Pygame Setup
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("NAME")
pygame.display.set_icon(ICON_IMG)
clock = pygame.time.Clock()
drawingSize = 22
drawingSurface = pygame.Surface((28 * drawingSize, 28 * drawingSize))
pygame.font.init()
font = pygame.font.SysFont("georgia", 40)
resultText = font.render("Result: ", True, (0, 0, 0))
certaintyText = font.render("Certainty: ", True, (0, 0, 0))

# Variables
running = True
canvas = [[0 for i in range(28)] for j in range(28)]
buttons = {1: False, 3: False}

def draw_canvas(canvas, surface, size):
    for r, row in enumerate(canvas):
        for c, col in enumerate(row):
            col = (-col) + 1
            pygame.draw.rect(surface, (255 * col, 255 * col, 255 * col), (c * size, r * size, size, size))

def in_canvas(pos, surface, size):
    xmin = (WIN_HEIGHT // 2) - (surface.get_height() // 2)
    ymin = (WIN_HEIGHT // 2) - (surface.get_height() // 2)
    xmax = xmin + (size * 28)
    ymax = ymin + (size * 28)
    return pos[0] >= xmin and pos[0] < xmax and pos[1] >= ymin and pos[1] < ymax

def get_canvas_index(pos, surface, size):
    xmin = (WIN_HEIGHT // 2) - (surface.get_height() // 2)
    ymin = (WIN_HEIGHT // 2) - (surface.get_height() // 2)
    pos = ((pos[0] - xmin) // size, (pos[1] - ymin) // size)
    return pos[1], pos[0]

def draw(canvas, indexes):
    for i in range(-1, 2):
        for j in range(-1, 2):
            row = indexes[0] + i
            col = indexes[1] + j
            if 0 <= row < 28 and 0 <= col < 28:
                canvas[row][col] += (1 - canvas[row][col]) / 2
    canvas[indexes[0]][indexes[1]] = 1

def erase(canvas, indexes):
    for i in range(-1, 2):
        for j in range(-1, 2):
            row = indexes[0] + i
            col = indexes[1] + j
            if 0 <= row < 28 and 0 <= col < 28:
                canvas[row][col] -= canvas[row][col] / 2
    canvas[indexes[0]][indexes[1]] = 0

def feed_forward():
    pass

# Main Loop
if __name__ == '__main__':
    win.fill((150, 150, 150))
    while running:

        dt = clock.tick(FRAMERATE) * 0.001

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in buttons:
                    buttons[event.button] = True
                elif event.button == 2:
                    canvas = [[0 for i in range(28)] for j in range(28)]
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in buttons:
                    buttons[event.button] = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    network.feed_forward([row[j] for row in canvas for j in range(28)])
                    values = network.outputLayer.values
                    answer = values.index(max(values))
                    resultText = font.render(f"Result: {answer}", True, (0, 0, 0))
                    certaintyText = font.render(f"Certainty: {round(values[answer] * 100, 1)}%", True, (0, 0, 0))

        mousePos = pygame.mouse.get_pos()

        if in_canvas(mousePos, drawingSurface, drawingSize):
            if buttons[1] and not buttons[3]:
                i, j = get_canvas_index(mousePos, drawingSurface, drawingSize)
                draw(canvas, (i, j))
            elif buttons[3] and not buttons[1]:
                i, j = get_canvas_index(mousePos, drawingSurface, drawingSize)
                erase(canvas, (i, j))

        win.fill((150, 150, 150))
        drawingSurface.fill((255, 255, 255))
        draw_canvas(canvas, drawingSurface, drawingSize)
        win.blit(drawingSurface, ((WIN_HEIGHT // 2) - (drawingSurface.get_height() // 2), (WIN_HEIGHT // 2) - (drawingSurface.get_height() // 2)))
        win.blit(resultText, (800, 100))
        win.blit(certaintyText, (800, 150))
        pygame.display.update()