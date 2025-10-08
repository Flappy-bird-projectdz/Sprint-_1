import pygame

# Khởi tạo Pygame
pygame.init()

# Thiết lập kích thước màn hình
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Background")

# Định nghĩa màu sắc (RGB)
BLUE_SKY = (135, 206, 235)  # Màu xanh da trời
GREEN_GROUND = (124, 252, 0) # Màu xanh lá cây
BROWN_GROUND = (139, 69, 19) # Màu nâu đất
WHITE = (255, 255, 255)     # Màu trắng cho mây