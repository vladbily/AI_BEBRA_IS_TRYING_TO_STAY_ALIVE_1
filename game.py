import pygame
import sys
from config import *
from birds import Birds
from pipes import Pipes
from menu import Menu
from ai_game import AI

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((DISPLAY_WIGHT, DISPLAY_HEIGHT))
        self.bg = (pygame.transform.scale2x(pygame.image.load('images/BACK1.png')))
        self.bg2 = (pygame.transform.scale2x(pygame.image.load('images/BACK2.png')))
        pygame.display.set_icon(pygame.image.load('images/icon.bmp'))
        pygame.display.set_caption('FLAPPY BEBRA AI')
        self.birrd = Birds(self)
        self.anim_bg = 0
        self.click = False
        self.clock = pygame.time.Clock()
        self.pipe_group = [Pipes(DISPLAY_WIGHT)]
        self.m = Menu(self)
        self.score = 0

    def run_game(self):
        while not self.m.start:
            self.m.show()
        while self.m.mode == 2:
            self._check_events()
            self._update_screen()
        while self.m.mode == 1:
            ai = AI()
            ai.run('config_ai.txt')
            break
    def _update_screen(self):

        if not self.birrd.lose:
            self.screen.blit(self.bg, (0, -100))
            self.pipe_update()
            self.screen.blit(self.bg2, (self.anim_bg, 700))
            if abs(self.anim_bg) > 144:
                self.anim_bg = 0
            self.anim_bg -= 5

        else:
            self.screen.blit(self.bg, (0, -100))
            for pipe in self.pipe_group:
                pipe.draw(self.screen)
                pipe.update(0)
            txt = SCORE_FONT.render('press R to restart', 0, pygame.Color('black'))
            self.screen.blit(txt, (45, 600))
            self.screen.blit(self.bg2, (0, 700))
            if self.keys[pygame.K_r]:
                if not self.click:
                    self.reset_game()


        self.birrd.update()
        self.clock.tick(60)
        self.print_text(10, 10, str(self.change_score(self.pipe_group)))
        pygame.display.flip()


    def change_score(self, list):
        for i in range(0, len(list), 1):
            if self.pipe_group[i].x == 100 and not self.birrd.lose:
                self.score += 1
        return self.score
    def print_text(self, x, y, text):
        txt = SCORE_FONT.render(text, 0, pygame.Color(255, 255, 255))
        self.screen.blit(txt, (x, y))
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and not self.birrd.flying and not self.birrd.lose:
                self.birrd.flying = True

        self.pressed()

    def pipe_update(self):
        if self.birrd.flying:
            for pipe in self.pipe_group:
                pipe.draw(self.screen)
            if (not len(self.pipe_group) or self.pipe_group[len(self.pipe_group) - 1].x < DISPLAY_WIGHT - 400) and self.birrd.flying:
                self.pipe_group.append(Pipes(DISPLAY_WIGHT))
                print(len(self.pipe_group), self.score)

            for pipe in self.pipe_group:
                if pipe.collide(self.birrd, self.screen):
                    self.birrd.lose = True
                    self.birrd.flying = False
            if self.birrd.rect.bottom >= 700:
                self.birrd.lose = True
                self.birrd.flying = False

            for i in range(len(self.pipe_group) - 1, -1, -1):
                pipe = self.pipe_group[i]
                pipe.update(5)
                if pipe.x < -90:
                    self.pipe_group.remove(pipe)



    def pressed(self):
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_q]:
            sys.exit()
        elif self.keys[pygame.K_SPACE] == 1 and self.birrd.clicked == False:
            self.birrd.clicked = True
            self.birrd.vel = -14
            self.birrd.start = True
        elif self.keys[pygame.K_SPACE] == 0:
            self.birrd.clicked = False


    def reset_game(self):
        self.click = False
        self.birrd.rect.x = 120
        self.pipe_group.clear()
        self.birrd.rect.y = int(DISPLAY_HEIGHT / 2 - 30)
        self.birrd.lose = False
        self.birrd._rotate_bird(360)
        self.score = 0



if __name__ == '__main__':
    fb = Game()
    fb.run_game()
