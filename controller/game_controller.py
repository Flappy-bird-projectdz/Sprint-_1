import pygame, sys
from entities import Bird, Pipe
from utilis import GameConfig, save_score, load_scores
from enginephysic import PhysicsEngine


class GameController:
    def __init__(self, screen, images, username="guest"):
        self.screen = screen
        self.images = images
        self.username = username
        self.physics = PhysicsEngine()

        self.bird = Bird(images.bird)
        self.pipes = []
        self.score = 0
        self.active = True
        self.show_leaderboard = False
        self.scores = load_scores()
        self.high_score = max([s["score"] for s in self.scores]) if self.scores else 0

        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE, 1200)

    def bat_dau_game(self):
        self.active = True
        self.score = 0
        self.pipes.clear()
        self.bird = Bird(self.images.bird)

    def xu_ly_nhay(self):
        if self.active:
            self.physics.ap_dung_luc_day(self.bird)
        else:
            self.bat_dau_game()

    def kiem_tra_va_cham(self):
        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.top_rect) or self.bird.rect.colliderect(pipe.bottom_rect):
                return False
        if self.bird.rect.top <= -50 or self.bird.rect.bottom >= 550:
            return False
        return True

    def cap_nhat(self):
        if self.active:
            self.physics.ap_dung_trong_luc(self.bird)
            self.bird.draw(self.screen)

            for pipe in self.pipes[:]:
                pipe.move()
                pipe.draw(self.screen)
                if pipe.off_screen():
                    self.pipes.remove(pipe)
                    self.score += 0.5

            self.active = self.kiem_tra_va_cham()
        else:
            if self.score > 0:
                self.scores = save_score(self.username, int(self.score))
                self.high_score = max([s["score"] for s in self.scores])
            self.score = 0

    def them_ong(self):
        from entities import Pipe
        self.pipes.append(Pipe(self.images.pipe, GameConfig.SCREEN_WIDTH + 50))
