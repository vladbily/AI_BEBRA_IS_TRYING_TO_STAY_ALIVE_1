import pygame
from config import *

class Menu:
    def __init__(self, display):
        self.display = display.screen
        self.selected = 0
        self.mode = 1
        self.start = False
        self.menu_bg = pygame.image.load('images/mmenu.png')
        self.button_list = [MENU_FONT.render('AI mode', True, FONT_COLOR), MENU_FONT.render('Play', True, FONT_COLOR),
                            MENU_FONT.render('Quit', True, FONT_COLOR)]

    def show(self):
        self.display.blit(self.menu_bg, (0, 0))
        pygame.draw.rect(self.display, 'Yellow', pygame.Rect(150, 500 + self.selected * 50 + 5, 40, 40))
        pygame.draw.rect(self.display, 'black', pygame.Rect(150, 500 + self.selected * 50 + 5, 40, 40), 3)
        self.check_events()

        pygame.display.flip()

    def check_events(self):
        for n, i in enumerate(self.button_list):
            self.display.blit(i, (200, 500 + 50 * n))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.selected + 1 < len(self.button_list):
                        self.selected += 1
                if event.key == pygame.K_UP:
                    if self.selected - 1 >= 0:
                        self.selected -= 1
                if event.key == pygame.K_RETURN:
                    if self.selected == 1:
                        self.mode = 2
                        self.start = True
                    elif self.selected == 0:
                        self.mode = 1
                        self.start = True
                    else:
                        quit()