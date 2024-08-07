import pygame
import neat
import sys
from config import *
from birds import Birds
from pipes import Pipes

class AI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((DISPLAY_WIGHT, DISPLAY_HEIGHT))
        self.bg = (pygame.transform.scale2x(pygame.image.load('images/BACK1.png')))
        self.bg2 = (pygame.transform.scale2x(pygame.image.load('images/BACK2.png')))
        self.anim_bg = 0
        self.clock = pygame.time.Clock()
        self.gen = 0


    def eval_genomes(self, genomes, config):
        self.gen += 1
        self.score = 0
        self.birds = []
        self.ge = []
        self.nets = []
        self.pipe_group = [Pipes(DISPLAY_WIGHT)]
        for genome_id, genome in genomes:
            self.birds.append(Birds(self))
            self.net = neat.nn.FeedForwardNetwork.create(genome, config)
            self.nets.append(self.net)
            genome.fitness = 0
            self.ge.append(genome)

        while len(self.birds):
            self._check_events()
            self._update_screen()

        print("BEST: ", self.score)
    def _update_screen(self):

        self.screen.blit(self.bg, (0, -100))
        if abs(self.anim_bg) > 144:
            self.anim_bg = 0
        self.anim_bg -= 5
        pipe_ind = 0
        if len(self.birds):
            if len(self.pipe_group) > 1 and self.birds[0].rect.x > self.pipe_group[0].x + self.pipe_group[0].pipe_top.get_width():
                pipe_ind = 1

        for i, bird in enumerate(self.birds):
            self.ge[i].fitness += 0.1
            bird._moving_bird()

            output = self.nets[self.birds.index(bird)].activate((bird.rect.y, abs(bird.rect.y - self.pipe_group[pipe_ind].height), abs(bird.rect.y - self.pipe_group[pipe_ind].bottom)))
            if output[0] > 0.5:
                bird.vel = -14
        self.pipe_update()
        self.screen.blit(self.bg2, (self.anim_bg, 700))


        for i, bird in enumerate(self.birds):
            if bird.lose and not bird.flying:
                self.birds.pop(i)
                self.nets.pop(i)
                self.ge.pop(i)
        for bird in self.birds:
            bird.update()
        self.clock.tick(900)
        self.print_text(15, 110, str(self.change_score(self.pipe_group)))
        pygame.display.flip()

    def change_score(self, list):
        for i in range(0, len(list), 1):
            if self.pipe_group[i].x == 100:
                self.score += 1
                for g in self.ge:
                    g.fitness += 5
        return self.score
    def print_text(self, x, y, text):
        txt = SCORE_FONT.render(text, 0, pygame.Color(255, 255, 255))
        self.screen.blit(txt, (x, y))
        score_label = SCORE_FONT.render("Alive: " + str(len(self.birds)), 1, (255, 255, 255))
        self.screen.blit(score_label, (10, 60))
        score_label = SCORE_FONT.render("Gens: " + str(self.gen - 1), 1, (255, 255, 255))
        self.screen.blit(score_label, (8, 10))
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()

    def pipe_update(self):
        for pipe in self.pipe_group:
            pipe.draw(self.screen)

        if not len(self.pipe_group) or self.pipe_group[len(self.pipe_group) - 1].x < DISPLAY_WIGHT - 400:
            self.pipe_group.append(Pipes(DISPLAY_WIGHT))

        for pipe in self.pipe_group:
            for i, bird in enumerate(self.birds):
                if pipe.collide(bird, self.screen) or bird.rect.bottom >= 700:
                    bird.lose = True
                    self.ge[i].fitness -= 1
                    self.birds.pop(i)
                    self.nets.pop(i)
                    self.ge.pop(i)


        for i in range(len(self.pipe_group) - 1, -1, -1):
            pipe = self.pipe_group[i]
            pipe.update(5)
            if pipe.x < -100:
                self.pipe_group.remove(pipe)

    def run(self, config_file):
        self.config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                             neat.DefaultSpeciesSet, neat.DefaultStagnation,
                             config_file)

        self.population = neat.Population(self.config)
        self.population.add_reporter(neat.StdOutReporter(True))
        self.stats = neat.StatisticsReporter()
        self.population.add_reporter(self.stats)
        self.winner = self.population.run(self.eval_genomes, 7)
        print('\nГеномы :\n{!s}'.format(self.winner))

if __name__ == "__main__":
    fb = AI()
    fb.run('config_ai.txt')
