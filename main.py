import pygame 
from pygame.locals import * 
import numpy as np 
from math import sqrt
import numba as nb

pygame.init()

# COLORS 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the window 
RES = WIN_WIDTH, WIN_HEIGHT = 800, 600
win = pygame.display.set_mode(RES, pygame.SCALED)

# Offset array 
offset = np.array([1.3 * WIN_WIDTH, WIN_HEIGHT]) // 2

# Maximum number of iterations
max_iter = 30

# Zoom level 
zoom = 2.2 / WIN_HEIGHT

# Texture 
texture = pygame.image.load("texture.jpg")
texture_size = min(texture.get_size()) - 1
texture_array = pygame.surfarray.array3d(texture)

# Fractal class 
class Fractal:
    def __init__(self):
        self.screen_array = np.full((WIN_WIDTH, WIN_HEIGHT, 3), [0, 0, 0], dtype=np.uint8)
        self.x = np.linspace(0, WIN_WIDTH, num=WIN_WIDTH, dtype=np.float32)
        self.y = np.linspace(0, WIN_HEIGHT, num=WIN_HEIGHT, dtype=np.float32)
        self.offset = offset 
        # Control settings 
        self.vel = 200
        self.zoom, self.scale = 2.2 / WIN_HEIGHT, 0.993 
        self.zoom_ratio = self.zoom / self.vel 
        self.max_iter, self.max_iter_limit = 30, 1000

    @staticmethod
    @nb.jit(fastmath=True, parallel=True)
    def render(screen_array, offset, zoom, max_iter):
        for x in nb.prange(WIN_WIDTH):
            for y in range(WIN_HEIGHT):
                c = (x - offset[0]) * zoom + 1j * (y - offset[1]) * zoom
                z = 0
                n = 0
                for i in range(max_iter):
                    z = z ** 2 + c 
                    if z.real**2 + z.imag**2 > 4:
                        break
                    n += 1 
                col = int(texture_size * n / max_iter)
                screen_array[x, y] = texture_array[col, col]
        return screen_array

    def control(self):
        global offset 
        pressed_key = pygame.key.get_pressed()
        # movement
        if pressed_key[K_a]:
            self.offset[0] += self.vel
        if pressed_key[K_d]:
            self.offset[0] -= self.vel
        if pressed_key[K_w]:
            self.offset[1] += self.vel 
        if pressed_key[K_s]:
            self.offset[1] -= self.vel 
        # stable zooming 
        if pressed_key[K_UP]:
            self.zoom *= self.scale
            self.offset[0] = (self.offset[0] + WIN_WIDTH / 2) * self.scale - WIN_WIDTH / 2
            self.offset[1] = (self.offset[1] + WIN_HEIGHT / 2) * self.scale - WIN_HEIGHT / 2
        if pressed_key[K_DOWN]:
            self.zoom /= self.scale
            self.offset[0] = (self.offset[0] + WIN_WIDTH / 2) / self.scale - WIN_WIDTH / 2
            self.offset[1] = (self.offset[1] + WIN_HEIGHT / 2) / self.scale - WIN_HEIGHT / 2
        # mandelbrot resolution 
        if pressed_key[K_LEFT]:
            self.max_iter -= 1 
        if pressed_key[K_RIGHT]:
            self.max_iter += 1 
        self.max_iter = min(max(self.max_iter, 2), self.max_iter_limit)

    def update(self):
        self.control()
        self.screen_array = self.render(self.screen_array, self.offset, self.zoom, self.max_iter) 

    def draw(self):
        pygame.surfarray.blit_array(win, self.screen_array)
    
    def run(self):
        self.update()
        self.draw()

# Main program loop
running = True
clock = pygame.time.Clock()
mandelbrot = Fractal()
while running:
    win.fill(BLACK)

    mandelbrot.run()

    pygame.display.set_caption(f"Mandelbrot Set Visualisation | FPS: {clock.get_fps()}")

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            pygame.quit()
            exit()

    pygame.display.update()
    clock.tick()