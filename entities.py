import pygame
import random
from utilis import GameConfig

class Bird:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect(center=(100, 300))
        self.movement = 0

    def update(self):
        self.movement += GameConfig.GRAVITY
        self.rect.centery += self.movement

    def flap(self):
        self.movement = -6

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Pipe:
    GAP = 200
    SPEED = 5
    PIPE_WIDTH = 52  # Giả định chiều rộng chuẩn của ống Flappy Bird là 52px

    def __init__(self, image, x):
        self.image = image
        self.height = random.randint(200, 400)
        
        
        self.top_rect = pygame.Rect(0, 0, self.PIPE_WIDTH, GameConfig.SCREEN_HEIGHT)
        self.top_rect.right = x
        self.top_rect.bottom = self.height - Pipe.GAP // 2
        
        # 2. TẠO RECT CHO ỐNG DƯỚI:
        
        self.bottom_rect = pygame.Rect(0, 0, self.PIPE_WIDTH, GameConfig.SCREEN_HEIGHT)
        self.bottom_rect.right = x
        self.bottom_rect.top = self.height + Pipe.GAP // 2
        
        

    def move(self):
        # Logic di chuyển là chính xác
        self.top_rect.centerx -= Pipe.SPEED
        self.bottom_rect.centerx -= Pipe.SPEED

    def draw(self, screen):
        flip_pipe = pygame.transform.flip(self.image, False, True)
        # Khi vẽ (blit), Pygame sẽ tự động kéo giãn (stretch) ảnh chiều dọc để lấp đầy Rect đã định.
        screen.blit(flip_pipe, self.top_rect)      # ống trên
        screen.blit(self.image, self.bottom_rect)  # ống dưới

    def off_screen(self):
        return self.top_rect.right < -50