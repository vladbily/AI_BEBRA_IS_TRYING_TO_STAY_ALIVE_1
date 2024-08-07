import pygame
import random
from config import *

class Pipes:
    def __init__(self, x):
        self.img = pygame.transform.scale2x(pygame.image.load('images/pipe.png'))
        self.x = x
        self.bottom = 0
        self.top = 0
        self.pipe_gap = 200
        self.pipe_top = pygame.transform.flip(self.img, False, True)
        self.pipe_bottom = self.img
        self.rect_top = self.pipe_top.get_rect()
        self.rect_bottom = self.pipe_bottom.get_rect()
        self.passed = False
        self.set_height()

    def update(self, arg):
        self.x -= arg

    def set_height(self):
        self.height = random.randint(50, 450)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.pipe_gap

    def draw(self, win):
        win.blit(self.pipe_top, (self.x, self.top))
        win.blit(self.pipe_bottom, (self.x, self.bottom))

    def collide(self, bird, win):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)
        top_offset = (self.x - bird.rect.x, self.top - round(bird.rect.y))
        bottom_offset = (self.x - bird.rect.x, self.bottom - round(bird.rect.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if b_point or t_point:
            return True

        return False
