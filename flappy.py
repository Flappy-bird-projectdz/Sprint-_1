import pygame, sys, os, json
from utilis import GameConfig, Images
from controller.game_controller import GameController

# === Khởi tạo pygame ===
pygame.init()
screen = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird - OOP Version")
clock = pygame.time.Clock()

# === Load hình ảnh ===
images = Images()
images.load()

# === Lấy username từ config.json ===
username = "guest"
if os.path.exists("config.json"):
    try:
        with open("config.json", "r") as f:
            cfg = json.load(f)
            username = cfg.get("username", "guest")
    except:
        pass

# === Khởi tạo bộ điều khiển trò chơi ===
controller = GameController(screen, images, username=username)

# === Font để vẽ chữ ===
def draw_text(text, size, x, y, color=(255,255,255)):
    font_local = pygame.font.Font(None, size)
    label = font_local.render(text, True, color)
    rect = label.get_rect(center=(x, y))
    screen.blit(label, rect)

# === Vòng lặp game chính ===
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                controller.xu_ly_nhay()
            if event.key == pygame.K_l and not controller.active:
                controller.show_leaderboard = not controller.show_leaderboard
        if event.type == controller.SPAWNPIPE and controller.active:
            controller.them_ong()

    # === Vẽ nền ===
    screen.blit(images.background, (0, 0))

    # === Cập nhật game ===
    controller.cap_nhat()

    # === Hiển thị điểm ===
    if controller.active:
        draw_text(f"Score: {int(controller.score)}", 40, GameConfig.SCREEN_WIDTH//2, 50, (255,255,0))
        draw_text(f"High Score: {controller.high_score}", 30, GameConfig.SCREEN_WIDTH//2, 90, (255,255,255))
    else:
        draw_text("GAME OVER", 50, GameConfig.SCREEN_WIDTH//2, 100, (255,0,0))
        draw_text(f"Your Score: {int(controller.score)}", 40, GameConfig.SCREEN_WIDTH//2, 160, (255,255,0))
        draw_text("Press SPACE to Restart", 30, GameConfig.SCREEN_WIDTH//2, 500, (0,255,0))
        draw_text("Press L to View Leaderboard", 25, GameConfig.SCREEN_WIDTH//2, 540, (255,255,255))

        if controller.show_leaderboard:
            draw_text("Leaderboard", 40, GameConfig.SCREEN_WIDTH//2, 240, (255,255,255))
            for i, s in enumerate(controller.scores[:5], start=1):
                draw_text(f"{i}. {s['user']} - {s['score']}", 35, GameConfig.SCREEN_WIDTH//2, 270 + i*40, (255,255,0))

    # === Vẽ nền đất ===
    screen.blit(images.base, (0, GameConfig.SCREEN_HEIGHT - 50))

    pygame.display.update()
    clock.tick(GameConfig.FPS)
