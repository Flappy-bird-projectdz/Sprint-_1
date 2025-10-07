import pygame
import os
import json

class GameConfig:
    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 600
    FPS = 60
    GRAVITY = 0.25

SCORES_FILE = "scores.json"
CONFIG_FILE = "config.json"

class Images:
    def __init__(self):
        self.background = None
        self.base = None
        self.bird = None
        self.pipe = None

    def load(self):
        # Background
        raw_bg = pygame.image.load(os.path.join("assets", "background-night.png")).convert()
        self.background = pygame.transform.scale(raw_bg, (GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))

        # Base
        self.base = pygame.image.load(os.path.join("assets", "base.png")).convert()

        # Bird theo màu từ config.json
        bird_color = "red"
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    cfg = json.load(f)
                    bird_color = cfg.get("bird_color", "red")
            except:
                pass

        bird_file = {
            "red": "redbird-midflap.png",
            "blue": "bluebird-downflap.png",
            "yellow": "yellowbird-midflap.png"
        }.get(bird_color, "redbird-midflap.png")

        raw_bird = pygame.image.load(os.path.join("assets", bird_file)).convert_alpha()
        self.bird = pygame.transform.scale(raw_bird, (34, 24))

        # Pipe
        raw_pipe = pygame.image.load(os.path.join("assets", "pipe-green.png")).convert_alpha()
        self.pipe = pygame.transform.scale(raw_pipe, (52, 600))

# ==== Xử lý điểm ====
def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_score(username, new_score):
    scores = load_scores()
    scores.append({"user": username, "score": new_score})
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f)
    return scores
def reset_scores():
    if os.path.exists(SCORES_FILE):
        os.remove(SCORES_FILE)  