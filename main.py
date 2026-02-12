import sys
import os
import random
import pygame
from pathlib import Path

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"

# =========================
# Configurações gerais
# =========================
WIDTH, HEIGHT = 960, 540
FPS = 60
TITLE = "Python 2D Game Demo"

WORLD_W = 7000
WORLD_H = HEIGHT

GROUND_HEIGHT = 60
GROUND_Y = HEIGHT - GROUND_HEIGHT
GRAVITY = 0.75

PLAYER_SPEED = 5.2
PLAYER_JUMP_FORCE = -14.2
PLAYER_FRAME_TIME = 0.18
PLAYER_SCALE = 1.8
PLAYER_FEET_OFFSET = 0
PLAYER_BASE_SIZE = (46, 60)
PLAYER_FRAMES = [
    "images/player/soldier_walk1.png",
    "images/player/soldier_walk2.png",
]

MAX_JUMP_HEIGHT = int((abs(PLAYER_JUMP_FORCE) ** 2) / (2 * GRAVITY))
MAX_JUMP_DISTANCE = int(PLAYER_SPEED * (2 * (abs(PLAYER_JUMP_FORCE) / GRAVITY)))

PLATFORM_DENSITY = 0.45
PLATFORM_MIN_WIDTH = 80
PLATFORM_MAX_WIDTH = 150
PLATFORM_MIN_GAP_X = 90
PLATFORM_MAX_GAP_X = 220
PLATFORM_MIN_STEP_UP = 20
PLATFORM_MAX_STEP_UP = int(MAX_JUMP_HEIGHT * 0.7)
PLATFORM_MAX_STEP_DOWN = 90
PLATFORM_MARGIN_TOP = 80
PLATFORM_MARGIN_BOTTOM = 120
MAX_CONSECUTIVE_HIGH = 2
BREAK_ZONE_MIN = 700
BREAK_ZONE_MAX = 1100
BREAK_ZONE_LENGTH_MIN = 220
BREAK_ZONE_LENGTH_MAX = 320
PLATFORM_CHUNK_SIZE = 500
PLATFORM_MAX_PER_CHUNK = 3

DEBUG_PLATFORMS = False  # Desativa overlays de debug: índices, linhas conectadas, info de chunk
DEBUG_HITBOX = False     # Mostra contornos das hitboxes em amarelo
DEBUG_UI = False         # Desativa informações técnicas na HUD (Active/CD, Jump H/D)

GOAL_WIDTH = 60
GOAL_HEIGHT = 90
GOAL_X_OFFSET = 250
GOAL_SAFE_ZONE = 280
GOAL_CLEAR_ZONE = 420
GOAL_IMAGE_PATH = "images/goal/terminal.png"

BG_PATH = "images/background/bg_gameplay.png"

# Estados do jogo
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"
LEVEL_COMPLETE = "level_complete"

# Cores
WHITE = (240, 240, 240)
BLACK = (20, 20, 20)
BG_COLOR = (28, 30, 38)
GREEN = (80, 170, 110)
BLUE = (70, 130, 220)
RED = (220, 90, 90)
YELLOW = (240, 200, 80)
GRAY = (120, 120, 120)

# Cores das plataformas - Neon Cyber
PLATFORM_FILL = (36, 52, 92)         # azul escuro
PLATFORM_TOP = (0, 232, 255)         # ciano neon
PLATFORM_GLOW = (178, 68, 255)       # roxo neon (detalhe)
PLATFORM_SHADOW = (12, 18, 40)       # sombra

CAMERA_DEAD_LEFT_RATIO = 0.28
CAMERA_DEAD_RIGHT_RATIO = 0.52

ENEMY_TYPE = "zombie"
MIN_ACTIVE_ENEMIES = 3
MAX_ACTIVE_ENEMIES = 6
DIST_MIN_FROM_PLAYER_X = 350
SPAWN_CLUSTER_MIN_DIST = 120
SPAWN_RIGHT_OFFSET_MIN = 80
SPAWN_RIGHT_OFFSET_MAX = 360
GLOBAL_SPAWN_CD_START = 1.2
GLOBAL_SPAWN_CD_MIN = 0.55
TYPE_CD_ENEMY = 1.2
DESPAWN_BEHIND_DISTANCE = 500
RESPITE_AFTER_HIT = 1.0
PROGRESSION_INTERVAL = 25.0
ENEMY_CONFIG = {
    "hp": 3,
    "score": 20,
    "speed": 2.2,
    "size": (40, 54),
    "cooldown": TYPE_CD_ENEMY,
    "color": (120, 220, 140),
    "frames": [
        "images/enemies/zombie_action1.png",
        "images/enemies/zombie_action2.png",
    ],
}
ENEMY_FRAME_TIME = 0.18
HIT_FLASH_TIME = 0.18


def load_background(rel_path: str, screen_w: int, screen_h: int):
    """
    Carrega fundo simples e opaco, escalado para tamanho da tela.
    Fallback seguro: Surface opaca escura.
    """
    full = ASSETS_DIR / rel_path
    if not full.exists():
        print(f"[BG] Arquivo nao encontrado: {full}. Usando fallback.")
        surf = pygame.Surface((screen_w, screen_h))
        surf.fill((10, 12, 22))
        return surf.convert()

    try:
        img = pygame.image.load(str(full))
        # Escalar para tamanho exato da tela
        if img.get_size() != (screen_w, screen_h):
            img = pygame.transform.smoothscale(img, (screen_w, screen_h))
        img = img.convert()
        print(f"[BG] Carregado: {full.name} size={img.get_size()}")
        return img
    except Exception as e:
        print(f"[BG] Erro ao carregar {full}: {e}")
        surf = pygame.Surface((screen_w, screen_h))
        surf.fill((10, 12, 22))
        return surf.convert()


class Camera:
    def __init__(self, screen_w, screen_h, world_w, world_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.world_w = world_w
        self.world_h = world_h
        self.x = 0.0
        self.y = 0.0
        self.dead_left = self.screen_w * CAMERA_DEAD_LEFT_RATIO
        self.dead_right = self.screen_w * CAMERA_DEAD_RIGHT_RATIO

    def update(self, player_rect):
        player_screen_x = player_rect.centerx - self.x
        if player_screen_x > self.dead_right:
            self.x = player_rect.centerx - self.dead_right
        if player_screen_x < self.dead_left:
            self.x = player_rect.centerx - self.dead_left

        max_x = max(0, self.world_w - self.screen_w)
        self.x = max(0, min(max_x, self.x))

    def apply_rect(self, rect):
        return rect.move(-int(self.x), -int(self.y))

    def apply_pos(self, x, y):
        return int(x - self.x), int(y - self.y)


class Player:
    def __init__(self, frames=None):
        scaled_w = int(PLAYER_BASE_SIZE[0] * PLAYER_SCALE)
        scaled_h = int(PLAYER_BASE_SIZE[1] * PLAYER_SCALE)
        self.w = scaled_w
        self.h = scaled_h
        self.x = 140
        self.y = GROUND_Y - self.h + PLAYER_FEET_OFFSET
        self.vx = 0
        self.vy = 0
        self.speed = PLAYER_SPEED
        self.jump_force = PLAYER_JUMP_FORCE
        self.on_ground = True
        self.frames = frames or []
        if self.frames:
            self.w, self.h = self.frames[0].get_size()
            self.y = GROUND_Y - self.h + PLAYER_FEET_OFFSET
        self.frame_index = 0
        self.frame_timer = 0.0
        self.facing = 1
        self.rect = pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, keys, world_w, platforms, dt):
        # Movimento horizontal
        self.vx = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vx = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vx = self.speed

        self.x += self.vx
        self.x = max(0, min(world_w - self.w, self.x))

        if self.vx < 0:
            self.facing = -1
        elif self.vx > 0:
            self.facing = 1

        # Gravidade / vertical
        prev_bottom = self.y + self.h
        self.vy += GRAVITY
        self.y += self.vy
        self.rect.topleft = (int(self.x), int(self.y))

        # Colisão com chão
        if self.y + self.h >= GROUND_Y:
            self.y = GROUND_Y - self.h + PLAYER_FEET_OFFSET
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False

        # Colisão com plataformas (apenas aterrissagem)
        if self.vy >= 0:
            for platform in platforms:
                if self.rect.right <= platform.rect.left or self.rect.left >= platform.rect.right:
                    continue
                if prev_bottom <= platform.rect.top and self.y + self.h >= platform.rect.top:
                    self.y = platform.rect.top - self.h + PLAYER_FEET_OFFSET
                    self.vy = 0
                    self.on_ground = True
                    break

        self.rect.topleft = (int(self.x), int(self.y))

        if len(self.frames) > 1 and abs(self.vx) > 0:
            self.frame_timer += dt
            if self.frame_timer >= PLAYER_FRAME_TIME:
                self.frame_timer = 0.0
                self.frame_index = (self.frame_index + 1) % len(self.frames)
        elif abs(self.vx) == 0:
            self.frame_index = 0

    def jump(self):
        if self.on_ground:
            self.vy = self.jump_force
            self.on_ground = False

    def draw(self, surface, camera):
        screen_rect = camera.apply_rect(self.rect)
        if self.frames:
            frame = self.frames[self.frame_index]
            if self.facing < 0:
                frame = pygame.transform.flip(frame, True, False)
            surface.blit(frame, screen_rect.topleft)
        else:
            pygame.draw.rect(surface, BLUE, screen_rect, border_radius=8)
            # detalhe simples
            eye = pygame.Rect(screen_rect.x + 28, screen_rect.y + 14, 8, 8)
            pygame.draw.rect(surface, WHITE, eye, border_radius=2)


class Enemy:
    def __init__(self, x, frames=None):
        self.type = ENEMY_TYPE
        self.w, self.h = ENEMY_CONFIG["size"]
        self.x = x
        self.y = GROUND_Y - self.h
        self.base_speed = ENEMY_CONFIG["speed"]
        self.speed = self.base_speed
        self.hp = ENEMY_CONFIG["hp"]
        self.score_value = ENEMY_CONFIG["score"]
        self.direction = random.choice([-1, 1])
        self.frames = frames or []
        self.frame_index = 0
        self.frame_timer = 0.0
        self.rect = pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, world_w, speed_multiplier=1.0, dt=0.0):
        self.speed = self.base_speed * speed_multiplier
        self.x += self.speed * self.direction
        if self.x <= 0:
            self.x = 0
            self.direction = 1
        if self.x + self.w >= world_w:
            self.x = world_w - self.w
            self.direction = -1
        self.rect.topleft = (int(self.x), int(self.y))

        if len(self.frames) > 1:
            self.frame_timer += dt
            if self.frame_timer >= ENEMY_FRAME_TIME:
                self.frame_timer = 0.0
                self.frame_index = (self.frame_index + 1) % len(self.frames)

    def draw(self, surface, camera, fallback_color):
        screen_rect = camera.apply_rect(self.rect)
        if self.frames:
            frame = self.frames[self.frame_index]
            if self.direction < 0:
                frame = pygame.transform.flip(frame, True, False)
            surface.blit(frame, screen_rect.topleft)
        else:
            pygame.draw.rect(surface, fallback_color, screen_rect, border_radius=6)


class Coin:
    def __init__(self, world_w):
        self.r = 12
        self.x = random.randint(220, world_w - 60)
        self.y = random.randint(200, GROUND_Y - 40)
        self.rect = pygame.Rect(int(self.x - self.r), int(self.y - self.r), self.r * 2, self.r * 2)

    def update(self):
        self.x = self.x
        self.rect.topleft = (int(self.x - self.r), int(self.y - self.r))

    def draw(self, surface, camera):
        cx, cy = camera.apply_pos(self.x, self.y)
        pygame.draw.circle(surface, YELLOW, (cx, cy), self.r)
        pygame.draw.circle(surface, BLACK, (cx, cy), self.r, 2)


class Bullet:
    def __init__(self, x, y, direction=1):
        self.w = 10
        self.h = 4
        self.x = x
        self.y = y
        self.speed = 10 * direction
        self.rect = pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self):
        self.x += self.speed
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surface, camera):
        screen_rect = camera.apply_rect(self.rect)
        pygame.draw.rect(surface, YELLOW, screen_rect, border_radius=2)

    def is_offscreen(self, world_w):
        return self.x > world_w or self.x + self.w < 0


class Platform:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(int(x), int(y), int(w), int(h))

    def draw(self, surface, camera):
        screen_rect = camera.apply_rect(self.rect)
        
        # Sombra deslocada (3 px para baixo)
        shadow_rect = screen_rect.copy()
        shadow_rect.y += 3
        pygame.draw.rect(surface, PLATFORM_SHADOW, shadow_rect, border_radius=6)
        
        # Corpo principal - azul escuro
        pygame.draw.rect(surface, PLATFORM_FILL, screen_rect, border_radius=6)
        
        # Linha superior neon - 3 px de altura
        if screen_rect.h >= 3:
            top_line = pygame.Rect(screen_rect.x, screen_rect.y, screen_rect.w, 3)
            pygame.draw.rect(surface, PLATFORM_TOP, top_line)
        
        # Detalhe roxo neon no centro (1 linha curta, 60% da largura)
        if screen_rect.h >= 8 and screen_rect.w >= 20:
            center_y = screen_rect.centery
            detail_w = int(screen_rect.w * 0.6)
            detail_x = screen_rect.x + (screen_rect.w - detail_w) // 2
            detail_rect = pygame.Rect(detail_x, center_y - 1, detail_w, 2)
            pygame.draw.rect(surface, PLATFORM_GLOW, detail_rect)
        
        # Debug: desenhar hitbox contorno em amarelo
        if DEBUG_HITBOX:
            pygame.draw.rect(surface, YELLOW, screen_rect, width=2)


class Goal:
    def __init__(self, x, y, image=None):
        self.w = GOAL_WIDTH
        self.h = GOAL_HEIGHT
        self.x = x
        self.y = y
        self.image = image
        self.rect = pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def draw(self, surface, camera, font):
        screen_rect = camera.apply_rect(self.rect)
        if self.image:
            surface.blit(self.image, screen_rect.topleft)
        else:
            pygame.draw.rect(surface, (160, 210, 255), screen_rect, border_radius=6)
            draw_text(surface, "EXIT", font, BLACK, screen_rect.centerx, screen_rect.centery, center=True)


def draw_text(surface, text, font, color, x, y, center=False):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(img, rect)


def load_image(relative_path, size=None, alpha=True, fallback_color=(60, 60, 60), fallback_size=None):
    full_path = os.path.join(os.path.dirname(__file__), "assets", relative_path)
    if not os.path.exists(full_path):
        size = fallback_size or size or (64, 64)
        print(f"[img] Arquivo nao encontrado: {relative_path}. Usando fallback.")
        surface = pygame.Surface(size, pygame.SRCALPHA) if alpha else pygame.Surface(size)
        surface.fill(fallback_color)
        return surface.convert_alpha() if alpha else surface.convert()
    try:
        image = pygame.image.load(full_path)
        image = image.convert_alpha() if alpha else image.convert()
        if size:
            image = pygame.transform.smoothscale(image, size)
        return image
    except pygame.error:
        size = fallback_size or size or (64, 64)
        print(f"[img] Falha ao carregar: {relative_path}. Usando fallback.")
        surface = pygame.Surface(size, pygame.SRCALPHA) if alpha else pygame.Surface(size)
        surface.fill(fallback_color)
        return surface.convert_alpha() if alpha else surface.convert()


def load_sound(relative_path):
    full_path = os.path.join(os.path.dirname(__file__), "assets", relative_path)
    if not os.path.exists(full_path):
        return None
    try:
        return pygame.mixer.Sound(full_path)
    except pygame.error:
        return None


def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


def generate_reachable_platforms(world_w, ground_y, goal_x, seed=None):
    rng = random.Random(seed) if seed is not None else random
    platforms = []
    main_route = []

    chunk_counts = {}
    high_streak = 0
    next_break_at = rng.randint(BREAK_ZONE_MIN, BREAK_ZONE_MAX)
    break_until_x = -1

    playable_y_min = PLATFORM_MARGIN_TOP
    playable_y_max = ground_y - PLATFORM_MARGIN_BOTTOM
    if playable_y_max <= playable_y_min:
        playable_y_max = ground_y - 40

    low = playable_y_max
    mid = clamp(playable_y_max - int(MAX_JUMP_HEIGHT * 0.5), playable_y_min, playable_y_max)
    high = clamp(playable_y_max - int(MAX_JUMP_HEIGHT * 0.9), playable_y_min, playable_y_max)
    lanes = [(low, 0.5), (mid, 0.35), (high, 0.15)]

    def pick_lane():
        roll = rng.random()
        acc = 0.0
        for lane_y, weight in lanes:
            acc += weight
            if roll <= acc:
                return lane_y
        return low

    x = 120
    y = low
    width = rng.randint(PLATFORM_MIN_WIDTH, PLATFORM_MAX_WIDTH)
    platform = Platform(x, y, width, 16)
    platforms.append(platform)
    main_route.append(platform)

    end_limit = max(300, int(goal_x - GOAL_CLEAR_ZONE))
    while x + width < end_limit:
        gap_x = rng.randint(PLATFORM_MIN_GAP_X, PLATFORM_MAX_GAP_X)
        gap_x = min(gap_x, max(PLATFORM_MIN_GAP_X, int(MAX_JUMP_DISTANCE * 0.85)))
        x = x + width + gap_x

        if x >= next_break_at:
            break_until_x = x + rng.randint(BREAK_ZONE_LENGTH_MIN, BREAK_ZONE_LENGTH_MAX)
            next_break_at = break_until_x + rng.randint(BREAK_ZONE_MIN, BREAK_ZONE_MAX)

        if break_until_x > x:
            target_y = rng.choice([low, mid])
        else:
            target_y = pick_lane()

        if target_y == high:
            high_streak += 1
        else:
            high_streak = 0
        if high_streak > MAX_CONSECUTIVE_HIGH:
            target_y = rng.choice([low, mid])
            high_streak = 0

        step = clamp(target_y - y, -PLATFORM_MAX_STEP_DOWN, PLATFORM_MAX_STEP_UP)
        y = clamp(y + step, playable_y_min, playable_y_max)
        width = rng.randint(PLATFORM_MIN_WIDTH, PLATFORM_MAX_WIDTH)

        chunk_index = int(x // PLATFORM_CHUNK_SIZE)
        chunk_counts.setdefault(chunk_index, 0)

        should_spawn = rng.random() <= PLATFORM_DENSITY
        if chunk_counts[chunk_index] >= PLATFORM_MAX_PER_CHUNK:
            should_spawn = False

        if should_spawn and x < end_limit:
            platform = Platform(x, y, width, 16)
            platforms.append(platform)
            main_route.append(platform)
            chunk_counts[chunk_index] += 1

        if rng.random() < 0.18 and break_until_x <= x:
            branch_x = x + rng.randint(20, 80)
            branch_y = clamp(y - rng.randint(0, PLATFORM_MAX_STEP_UP // 2), playable_y_min, playable_y_max)
            branch_w = rng.randint(PLATFORM_MIN_WIDTH, int(PLATFORM_MAX_WIDTH * 0.8))
            branch_chunk = int(branch_x // PLATFORM_CHUNK_SIZE)
            chunk_counts.setdefault(branch_chunk, 0)
            if branch_x < end_limit and branch_x + branch_w < world_w - 50 and chunk_counts[branch_chunk] < PLATFORM_MAX_PER_CHUNK:
                platforms.append(Platform(branch_x, branch_y, branch_w, 16))
                chunk_counts[branch_chunk] += 1

    for index in range(1, len(main_route)):
        prev = main_route[index - 1].rect
        cur = main_route[index].rect
        gap = cur.left - prev.right
        if gap > MAX_JUMP_DISTANCE:
            cur.x = prev.right + int(MAX_JUMP_DISTANCE * 0.9)

        step_up = prev.top - cur.top
        if step_up > MAX_JUMP_HEIGHT:
            cur.y = prev.top - int(MAX_JUMP_HEIGHT * 0.85)

        step_down = cur.top - prev.top
        if step_down > PLATFORM_MAX_STEP_DOWN:
            cur.y = prev.top + PLATFORM_MAX_STEP_DOWN

        cur.y = clamp(cur.y, playable_y_min, playable_y_max)

    debug_info = {
        "chunk_counts": chunk_counts,
        "high_streak": high_streak,
        "density": PLATFORM_DENSITY,
    }
    return platforms, main_route, debug_info


def build_level():
    coins = [Coin(WORLD_W) for _ in range(18)]
    goal_x = WORLD_W - GOAL_X_OFFSET
    goal_y = GROUND_Y - GOAL_HEIGHT
    platforms, main_route, platform_debug = generate_reachable_platforms(WORLD_W, GROUND_Y, goal_x)
    goal = Goal(goal_x, goal_y)
    return coins, platforms, main_route, platform_debug, goal


def spawn_x():
    return random.randint(220, WORLD_W - 120)


def spawn_enemy(frames):
    x = spawn_x()
    return Enemy(x, frames=frames)


class SpawnManager:
    def __init__(self, world_w, screen_w, goal_x):
        self.world_w = world_w
        self.screen_w = screen_w
        self.goal_x = goal_x
        self.global_timer = 0.0
        self.last_spawn_x = None
        self.respite_timer = 0.0

    def notify_player_hit(self):
        self.respite_timer = RESPITE_AFTER_HIT

    def _global_cooldown(self, elapsed_time):
        span = max(1.0, 120.0)
        cd = GLOBAL_SPAWN_CD_START - (elapsed_time / span) * (GLOBAL_SPAWN_CD_START - GLOBAL_SPAWN_CD_MIN)
        return max(GLOBAL_SPAWN_CD_MIN, cd)

    def _speed_multiplier(self, elapsed_time):
        return 1.0 + min(elapsed_time / 180.0, 0.35)

    def _target_limit(self, elapsed_time):
        increments = int(elapsed_time // PROGRESSION_INTERVAL)
        return min(MAX_ACTIVE_ENEMIES, MIN_ACTIVE_ENEMIES + increments)

    def _valid_spawn_x(self, player_x, camera_x):
        min_x = camera_x + self.screen_w + SPAWN_RIGHT_OFFSET_MIN
        max_x = camera_x + self.screen_w + SPAWN_RIGHT_OFFSET_MAX
        max_x = min(max_x, self.world_w - 60)
        if min_x >= max_x:
            return None

        for _ in range(4):
            x = random.randint(int(min_x), int(max_x))
            if abs(x - player_x) < DIST_MIN_FROM_PLAYER_X:
                continue
            if x >= self.goal_x - GOAL_SAFE_ZONE:
                continue
            if self.last_spawn_x is not None and abs(x - self.last_spawn_x) < SPAWN_CLUSTER_MIN_DIST:
                continue
            return x
        return None

    def update(self, dt, elapsed_time, enemies, player, camera, enemy_frames):
        self.global_timer = max(0.0, self.global_timer - dt)
        self.respite_timer = max(0.0, self.respite_timer - dt)

        enemies = [
            enemy
            for enemy in enemies
            if enemy.x + enemy.w >= camera.x - DESPAWN_BEHIND_DISTANCE
        ]

        target_limit = self._target_limit(elapsed_time)
        speed_multiplier = self._speed_multiplier(elapsed_time)
        global_cd = self._global_cooldown(elapsed_time)

        max_allowed = min(MAX_ACTIVE_ENEMIES, target_limit)

        spawn_attempts = 0
        max_attempts = 6
        while len(enemies) < MIN_ACTIVE_ENEMIES and spawn_attempts < max_attempts:
            if self.global_timer > 0 or self.respite_timer > 0:
                break
            spawn_x = self._valid_spawn_x(player.x, camera.x)
            if spawn_x is None:
                spawn_attempts += 1
                continue
            enemy = spawn_enemy(enemy_frames)
            enemy.x = spawn_x
            enemy.rect.topleft = (int(enemy.x), int(enemy.y))
            enemies.append(enemy)
            self.last_spawn_x = spawn_x
            self.global_timer = global_cd
            spawn_attempts += 1

        if len(enemies) < max_allowed and self.global_timer <= 0 and self.respite_timer <= 0:
            spawn_x = self._valid_spawn_x(player.x, camera.x)
            if spawn_x is not None:
                enemy = spawn_enemy(enemy_frames)
                enemy.x = spawn_x
                enemy.rect.topleft = (int(enemy.x), int(enemy.y))
                enemies.append(enemy)
                self.last_spawn_x = spawn_x
                self.global_timer = global_cd

        debug = {
            "global_cd": global_cd,
            "active": len(enemies),
        }

        return enemies, debug, speed_multiplier


def main():
    print("\\n" + "="*60)
    print("INICIO DO JOGO - DIAGNOSTICO ATIVADO")
    print("="*60 + "\\n")
    sys.stdout.flush()
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    font_title = pygame.font.SysFont("arial", 54, bold=True)
    font_ui = pygame.font.SysFont("arial", 28)
    font_small = pygame.font.SysFont("arial", 22)

    state = MENU

    player_w = int(PLAYER_BASE_SIZE[0] * PLAYER_SCALE)
    player_h = int(PLAYER_BASE_SIZE[1] * PLAYER_SCALE)
    player_frames = [load_image(frame_path, (player_w, player_h)) for frame_path in PLAYER_FRAMES]
    player_frames = [frame for frame in player_frames if frame is not None]
    player = Player(frames=player_frames)
    coins, platforms, main_route, platform_debug, goal = build_level()
    bullets = []
    enemies = []
    effects = []
    camera = Camera(WIDTH, HEIGHT, WORLD_W, WORLD_H)
    
    # Carregar fundo único e fixo
    bg_gameplay = load_background(BG_PATH, WIDTH, HEIGHT)
    
    goal_image = load_image(GOAL_IMAGE_PATH, (GOAL_WIDTH, GOAL_HEIGHT))
    goal.image = goal_image
    enemy_frames = [
        load_image(frame_path, ENEMY_CONFIG["size"]) for frame_path in ENEMY_CONFIG["frames"]
    ]
    enemy_frames = [frame for frame in enemy_frames if frame is not None]
    hit_sfx = load_sound("sound/hit.wav")
    spawn_manager = SpawnManager(WORLD_W, WIDTH, goal.x)
    kills = 0
    score = 0
    best_score = 0
    time_survived = 0.0
    score_time_acc = 0.0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # segundos por frame

        # ========= Eventos =========
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == MENU:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # iniciar jogo
                        player = Player(frames=player_frames)
                        coins, platforms, main_route, platform_debug, goal = build_level()
                        bullets = []
                        enemies = []
                        effects = []
                        spawn_manager = SpawnManager(WORLD_W, WIDTH, goal.x)
                        goal.image = goal_image
                        kills = 0
                        score = 0
                        time_survived = 0.0
                        score_time_acc = 0.0
                        state = PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            elif state == PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                        player.jump()
                    elif event.key == pygame.K_f:
                        bullets.append(Bullet(player.x + player.w, player.y + player.h * 0.5))
                    elif event.key == pygame.K_ESCAPE:
                        state = MENU

            elif state == GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # reinicia gameplay direto
                        player = Player(frames=player_frames)
                        coins, platforms, main_route, platform_debug, goal = build_level()
                        bullets = []
                        enemies = []
                        effects = []
                        spawn_manager = SpawnManager(WORLD_W, WIDTH, goal.x)
                        goal.image = goal_image
                        kills = 0
                        score = 0
                        time_survived = 0.0
                        score_time_acc = 0.0
                        state = PLAYING
                    elif event.key == pygame.K_m:
                        state = MENU
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            elif state == LEVEL_COMPLETE:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        state = MENU
                    elif event.key == pygame.K_ESCAPE:
                        running = False

        # ========= Update =========
        if state == PLAYING:
            keys = pygame.key.get_pressed()
            player.update(keys, WORLD_W, platforms, dt)
            camera.update(player.rect)

            if player.rect.colliderect(goal.rect):
                state = LEVEL_COMPLETE
                continue

            # Spawn manager + dificuldade
            if state == PLAYING:
                enemies, spawn_debug, speed_multiplier = spawn_manager.update(
                    dt, time_survived, enemies, player, camera, enemy_frames
                )

            # Atualiza inimigos
            for enemy in enemies:
                enemy.update(WORLD_W, speed_multiplier=speed_multiplier, dt=dt)

            # Atualiza moedas
            for c in coins:
                c.update()

            for b in bullets:
                b.update()

            # Remove fora da tela
            bullets = [b for b in bullets if not b.is_offscreen(WORLD_W)]

            # Colisão bullet x enemy
            remaining_bullets = []
            defeated = []
            for b in bullets:
                hit = False
                for enemy in enemies:
                    if b.rect.colliderect(enemy.rect):
                        enemy.hp -= 1
                        effects.append({"x": enemy.rect.centerx, "y": enemy.rect.centery, "ttl": HIT_FLASH_TIME})
                        if hit_sfx:
                            hit_sfx.play()
                        if enemy.hp <= 0:
                            defeated.append(enemy)
                        hit = True
                        break
                if not hit:
                    remaining_bullets.append(b)
            bullets = remaining_bullets
            if defeated:
                for enemy in defeated:
                    if enemy in enemies:
                        enemies.remove(enemy)
                        score += enemy.score_value
                        kills += 1


            # Colisão com inimigos => Game Over
            for enemy in enemies:
                if player.rect.colliderect(enemy.rect):
                    spawn_manager.notify_player_hit()
                    best_score = max(best_score, score)
                    state = GAME_OVER
                    break

            # Coletar moedas
            remaining_coins = []
            for c in coins:
                if player.rect.colliderect(c.rect):
                    score += 15
                else:
                    remaining_coins.append(c)
            coins = remaining_coins

            # Pontuação por tempo - 1 ponto por segundo real
            time_survived += dt
            score_time_acc += dt
            while score_time_acc >= 1.0:
                score += 1
                score_time_acc -= 1.0

            # Efeitos de hit
            updated_effects = []
            for effect in effects:
                effect["ttl"] -= dt
                if effect["ttl"] > 0:
                    updated_effects.append(effect)
            effects = updated_effects

        # ========= Draw =========
        screen.fill(BG_COLOR)

        if state == MENU:
            draw_text(screen, "CyberShield: Virus Hunt ", font_title, WHITE, WIDTH // 2, 110, center=True)
            draw_text(screen, "ENTER - Iniciar", font_ui, WHITE, WIDTH // 2, 220, center=True)
            draw_text(screen, "ESC - Sair", font_ui, WHITE, WIDTH // 2, 260, center=True)

            # Requisito obrigatório: controles no menu
            draw_text(screen, "CONTROLES", font_ui, YELLOW, WIDTH // 2, 340, center=True)
            draw_text(screen, "A/D ou <-/-> : Mover", font_small, WHITE, WIDTH // 2, 380, center=True)
            draw_text(screen, "SPACE / W / ^ : Pular", font_small, WHITE, WIDTH // 2, 410, center=True)
            draw_text(screen, "F : Atirar", font_small, WHITE, WIDTH // 2, 440, center=True)
            draw_text(screen, "ESC : Voltar para o menu / Sair", font_small, WHITE, WIDTH // 2, 470, center=True)

        elif state == PLAYING:
            # Fundo fixo único
            screen.blit(bg_gameplay, (0, 0))

            # Chao (mundo)
            ground_rect = pygame.Rect(0, GROUND_Y, WORLD_W, HEIGHT - GROUND_Y)
            pygame.draw.rect(screen, GREEN, camera.apply_rect(ground_rect))
            line_start = camera.apply_pos(0, GROUND_Y)
            line_end = camera.apply_pos(WORLD_W, GROUND_Y)
            pygame.draw.line(screen, (50, 110, 70), line_start, line_end, 3)

            for platform in platforms:
                platform.draw(screen, camera)

            goal.draw(screen, camera, font_small)

            if DEBUG_PLATFORMS:
                for index, platform in enumerate(platforms):
                    cx, cy = camera.apply_pos(platform.rect.centerx, platform.rect.top - 12)
                    draw_text(screen, f"{index}", font_small, GRAY, cx, cy, center=True)

                for prev, cur in zip(main_route, main_route[1:]):
                    start = camera.apply_pos(prev.rect.right, prev.rect.top)
                    end = camera.apply_pos(cur.rect.left, cur.rect.top)
                    pygame.draw.line(screen, GRAY, start, end, 1)

                if platform_debug:
                    chunk_info = " ".join(
                        f"{chunk}:{count}" for chunk, count in sorted(platform_debug["chunk_counts"].items())
                    )
                    draw_text(
                        screen,
                        f"Chunks {chunk_info}",
                        font_small,
                        GRAY,
                        20,
                        176,
                    )
                    draw_text(
                        screen,
                        f"High streak {platform_debug['high_streak']} | Density {platform_debug['density']:.2f}",
                        font_small,
                        GRAY,
                        20,
                        200,
                    )

            player.draw(screen, camera)

            for enemy in enemies:
                enemy.draw(screen, camera, ENEMY_CONFIG["color"])
            for c in coins:
                c.draw(screen, camera)
            for b in bullets:
                b.draw(screen, camera)

            for effect in effects:
                cx, cy = camera.apply_pos(effect["x"], effect["y"])
                radius = int(10 * (effect["ttl"] / HIT_FLASH_TIME)) + 4
                pygame.draw.circle(screen, WHITE, (cx, cy), radius, 2)

            draw_text(screen, f"Score: {score}", font_ui, WHITE, 20, 18)
            draw_text(screen, f"Tempo: {time_survived:05.1f}s", font_small, WHITE, 20, 52)
            draw_text(screen, f"Zumbis derrotados: {kills}", font_small, WHITE, 20, 78)
            progress = clamp((player.rect.centerx / WORLD_W) * 100, 0, 100)
            draw_text(screen, f"Progresso: {progress:05.1f}%", font_small, WHITE, WIDTH - 220, 52)
            draw_text(screen, "Objetivo: alcançar o terminal no fim do mapa", font_small, GRAY, WIDTH - 420, 78)
            if DEBUG_UI:
                draw_text(
                    screen,
                    f"Active {spawn_debug['active']} | CD {spawn_debug['global_cd']:.2f}s",
                    font_small,
                    GRAY,
                    20,
                    104,
                )
            if DEBUG_PLATFORMS:
                draw_text(
                    screen,
                    f"Jump H {MAX_JUMP_HEIGHT} | Jump D {MAX_JUMP_DISTANCE}",
                    font_small,
                    GRAY,
                    20,
                    152,
                )
            draw_text(screen, "ESC - Menu", font_small, GRAY, WIDTH - 160, 20)

        elif state == GAME_OVER:
            draw_text(screen, "GAME OVER", font_title, WHITE, WIDTH // 2, 140, center=True)
            draw_text(screen, f"Score final: {score}", font_ui, WHITE, WIDTH // 2, 230, center=True)
            draw_text(screen, f"Melhor score: {max(best_score, score)}", font_ui, WHITE, WIDTH // 2, 270, center=True)
            draw_text(screen, "R - Reiniciar", font_ui, YELLOW, WIDTH // 2, 340, center=True)
            draw_text(screen, "M - Menu principal", font_ui, WHITE, WIDTH // 2, 380, center=True)
            draw_text(screen, "ESC - Sair", font_ui, WHITE, WIDTH // 2, 420, center=True)

        elif state == LEVEL_COMPLETE:
            draw_text(screen, "FASE 1 CONCLUÍDA", font_title, WHITE, WIDTH // 2, 150, center=True)
            draw_text(screen, "DEMO FINALIZADA", font_ui, WHITE, WIDTH // 2, 230, center=True)
            draw_text(screen, f"Score final: {score}", font_ui, WHITE, WIDTH // 2, 280, center=True)
            draw_text(screen, "ENTER - Voltar ao menu", font_ui, YELLOW, WIDTH // 2, 360, center=True)
            draw_text(screen, "ESC - Sair", font_ui, WHITE, WIDTH // 2, 400, center=True)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
