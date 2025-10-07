import pygame, sys, os, json
from utilis import GameConfig, Images, load_scores, save_score
from entities import Bird, Pipe

pygame.init()
screen = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Demo")
clock = pygame.time.Clock()

# Font
font = pygame.font.Font(None, 40)

# Load ảnh
images = Images()
images.load()

bird = Bird(images.bird)
pipes = []

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

game_active = True
score = 0
scores = load_scores()
high_score = max([s["score"] for s in scores]) if scores else 0
show_leaderboard = False

# Lấy username từ config.json
username = "guest"
if os.path.exists("config.json"):
    with open("config.json", "r") as f:
        try:
            cfg = json.load(f)
            username = cfg.get("username", "guest")
        except:
            pass

def check_collision():
    for pipe in pipes:
        if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
            return False
    if bird.rect.top <= -50 or bird.rect.bottom >= 550:
        return False
    return True

def draw_text(text, size, x, y, color=(255,255,255)):
    font_local = pygame.font.Font(None, size)
    label = font_local.render(text, True, color)
    rect = label.get_rect(center=(x, y))
    screen.blit(label, rect)

last_score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird.flap()
            if event.key == pygame.K_SPACE and not game_active:
                # Reset game
                bird = Bird(images.bird)
                pipes.clear()
                game_active = True
                score = 0
                show_leaderboard = False
            if event.key == pygame.K_l and not game_active:
                show_leaderboard = not show_leaderboard
        if event.type == SPAWNPIPE and game_active:
            pipes.append(Pipe(images.pipe, GameConfig.SCREEN_WIDTH + 50))

    screen.blit(images.background, (0, 0))

    if game_active:
        bird.update()
        bird.draw(screen)

        for pipe in pipes[:]:
            pipe.move()
            pipe.draw(screen)
            if pipe.off_screen():
                pipes.remove(pipe)
                score += 0.5

        game_active = check_collision()

        draw_text(f"Score: {int(score)}", 40, GameConfig.SCREEN_WIDTH//2, 50, (255,255,0))
        draw_text(f"High Score: {high_score}", 30, GameConfig.SCREEN_WIDTH//2, 90, (255,255,255))

    else:
        if score > 0:
            scores = save_score(username, int(score))
            high_score = max([s["score"] for s in scores])
            last_score = int(score)
            score = 0

        draw_text("GAME OVER", 50, GameConfig.SCREEN_WIDTH//2, 100, (255,0,0))
        draw_text(f"Your Score: {last_score}", 40, GameConfig.SCREEN_WIDTH//2, 160, (255,255,0))
        draw_text("Press SPACE to Restart", 30, GameConfig.SCREEN_WIDTH//2, 500, (0,255,0))
        draw_text("Press L to View Leaderboard", 25, GameConfig.SCREEN_WIDTH//2, 540, (255,255,255))

        if show_leaderboard:
            draw_text("Leaderboard", 40, GameConfig.SCREEN_WIDTH//2, 240, (255,255,255))
            for i, s in enumerate(scores[:5], start=1):
                draw_text(f"{i}. {s['user']} - {s['score']}", 35, GameConfig.SCREEN_WIDTH//2, 270 + i*40, (255,255,0))

    screen.blit(images.base, (0, GameConfig.SCREEN_HEIGHT - 50))
    pygame.display.update()
    clock.tick(GameConfig.FPS)
