import pygame
import random
from utilis import GameConfig


# ======= CLASS NHÂN VẬT =======
class Bird:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect(center=(100, 300))
        self.movement = 0

    def update(self, gravity):
        self.movement += gravity
        self.rect.centery += self.movement

    def flap(self, power):
        self.movement = -power

    def draw(self, screen):
        screen.blit(self.image, self.rect)


# ======= CLASS ỐNG =======
class Pipe:
    GAP = 200
    SPEED = 5
    WIDTH = 52

    def __init__(self, image, x):
        self.image = image
        self.height = random.randint(200, 400)
        self.top_rect = pygame.Rect(0, 0, self.WIDTH, GameConfig.SCREEN_HEIGHT)
        self.top_rect.right = x
        self.top_rect.bottom = self.height - Pipe.GAP // 2

        self.bottom_rect = pygame.Rect(0, 0, self.WIDTH, GameConfig.SCREEN_HEIGHT)
        self.bottom_rect.right = x
        self.bottom_rect.top = self.height + Pipe.GAP // 2

    def move(self):
        self.top_rect.centerx -= Pipe.SPEED
        self.bottom_rect.centerx -= Pipe.SPEED

    def draw(self, screen):
        flip_pipe = pygame.transform.flip(self.image, False, True)
        screen.blit(flip_pipe, self.top_rect)
        screen.blit(self.image, self.bottom_rect)

    def off_screen(self):
        return self.top_rect.right < -50


# ======= CLASS NGƯỜI CHƠI =======
class User:
    def __init__(self, username, password, email, skin="red"):
        self.username = username
        self.password = password
        self.email = email
        self.skin = skin
        self.scores = []

    def add_score(self, score):
        self.scores.append(score)


# ======= CLASS ĐIỂM =======
class Score:
    def __init__(self, user, score_value):
        self.user = user
        self.score_value = score_value

    def to_dict(self):
        return {"user": self.user, "score": self.score_value}
