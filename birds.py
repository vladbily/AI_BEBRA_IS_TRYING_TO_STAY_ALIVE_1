import pygame
from config import *
class Birds:
    def __init__(self, fb_g):
        self.screen = fb_g.screen
        self.screen_rect = fb_g.screen.get_rect()
        self.player = [
            pygame.transform.scale2x(pygame.image.load('images/bebra1.png')),
            pygame.transform.scale2x(pygame.image.load('images/bebra2.png')),
            pygame.transform.scale2x(pygame.image.load('images/bebra3.png'))
        ]
        self.anim_count = 0
        self.image = self.player[self.anim_count]
        self.rect = self.image.get_rect()
        self.rect.center = (150, DISPLAY_HEIGHT // 2)
        self.counter = 0
        self.cooldown = 0
        self.vel = 0
        self.sy = 0
        self.clicked = False
        self.flying = False
        self.lose = False
        self.start = False

    def update(self):
        if self.flying and not self.lose:
            self._moving_bird()
        self._anim_bird()

    def _anim_bird(self):
        if not self.lose:
            self.counter += 1
            self.cooldown = 5
            if self.counter > self.cooldown:
                self.anim_count += 1
                self.counter = 0
                if self.anim_count > 2:
                    self.anim_count = 0
            self.screen.blit(self.image, self.rect)
            self._rotate_bird(self.vel * -2)
        else:
            self.screen.blit(self.image, self.rect)
            if not self.flying:
                self.py = self.rect.y
                self.py += self.sy
                self.sy = (self.vel + 7) * 0.98
                self.rect.y = int(self.py)
                if self.rect.y > 650:
                    self.sy = 0
            self._rotate_bird(-90)
            self.vel = 0


    def _moving_bird(self):
        self.vel += 1
        if self.vel > 13:
            self.vel = 13
        if self.rect.bottom < DISPLAY_HEIGHT:
            self.rect.y += int(self.vel)
        if self.rect.bottom < 0:
            self.flying = False
            self.lose = True
        if self.rect.bottom >= DISPLAY_HEIGHT:
            self.flying = False
            self.lose = True

    def _rotate_bird(self, x):
        self.image = pygame.transform.rotate(self.player[self.anim_count], x)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)