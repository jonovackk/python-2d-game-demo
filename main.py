import sys
import os
import random
import re
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
RUN_ANIM_INTERVAL = 0.12  # Intervalo entre frames de corrida
PLAYER_BASE_SIZE = (60, 60)

# Sprites do player (direita - será espelhado para esquerda)
PLAYER_IDLE_RIGHT = "images/player/player_idle_right.png"
PLAYER_RUN1_RIGHT = "images/player/player_run1_right.png"
PLAYER_RUN2_RIGHT = "images/player/player_run2_right.png"

# Sprite sheet warpgal (player principal)
WARPGAL_SHEET    = "images/player/warpgal-anim-sheet-alpha.png"
WARPGAL_FRAME_W  = 72    # largura de cada frame no sheet
WARPGAL_FRAME_H  = 72    # altura de cada frame no sheet
WARPGAL_IDLE_ROW = 0     # row 0 = animação idle
WARPGAL_RUN_ROW  = 1     # row 1 = animação de corrida

# Fallback para sprites recortados manualmente (arquivos individuais)
PLAYER_SPLIT_GLOB = "images/player/Layer 1_sprite_*.png"
PLAYER_SPLIT_IDLE_IDX = 1
PLAYER_SPLIT_RUN1_IDX = 3
PLAYER_SPLIT_RUN2_IDX = 6

# Frames de animação do player (índices dos arquivos Layer 1_sprite_XXX.png)
# ─────────────────────────────────────────────────────────────────────────────
# Ajuste os índices abaixo para trocar poses sem mexer em física/código
ANIM_RUN_FRAMES          = [121, 123, 125, 127]  # correndo mirando (RUN_AIM)
ANIM_IDLE_WAIT_FRAME     = 117                             # frame de repouso
ANIM_IDLE_FRAMES         = [143, 169, 195, 169, 143]       # sequência ping-pong
ANIM_CROUCH_FRAMES       = [118]                 # agachado (S/↓ sem F)
ANIM_CROUCH_SHOOT_FRAMES = [131]                 # agachado + F
ANIM_JUMP_FRAMES         = [150]                   # no ar
ANIM_SHOOT_FRAMES        = [130]                 # tiro em pé (F sem agachar)

RUN_ANIM_INTERVAL   = 0.10   # segundos por frame de corrida  ← ajuste aqui
IDLE_ANIM_INTERVAL  = 0.25   # segundos por frame de idle     ← ajuste aqui
IDLE_WAIT_DURATION  = 3.0    # segundos de espera antes de animar ← ajuste aqui
SHOOT_ANIM_INTERVAL = 0.06   # segundos por frame de tiro     ← ajuste aqui

# Sprite sheet bullet
BULLET_SHEET     = "images/bullets/shooties-alpha.png"
BULLET_FRAME_W   = 16    # largura de cada frame de bullet
BULLET_FRAME_H   = 32    # altura de cada frame de bullet
BULLET_FRAME_IDX = 3     # índice do frame a usar (0–6)

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
SCORE_KILL        = 20   # pontos por matar um inimigo     ← ajuste aqui
SCORE_COLLECTIBLE = 50   # pontos por coletar um item      ← ajuste aqui

ENEMY_CONFIG = {
    "hp": 3,
    "score": SCORE_KILL,
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
    def __init__(self, sprites=None):
        """
        sprites: dict com idle_right, idle_left, run1_right, run1_left, run2_right, run2_left,
                 width, height — e opcionalmente 'all_frames' (dict idx->Surface) e 'size'.
        """
        if sprites:
            self.sprites = sprites
            self.w = sprites['width']
            self.h = sprites['height']
            # Suporte a multi-frame: todos os frames recortados
            self._all_frames_r = sprites.get('all_frames', {})
            self._all_frames_l = {
                k: pygame.transform.flip(v, True, False)
                for k, v in self._all_frames_r.items()
            }
        else:
            self.w = int(PLAYER_BASE_SIZE[0] * PLAYER_SCALE)
            self.h = int(PLAYER_BASE_SIZE[1] * PLAYER_SCALE)
            self.sprites = None
            self._all_frames_r = {}
            self._all_frames_l = {}

        self.x = 140
        self.y = GROUND_Y - self.h + PLAYER_FEET_OFFSET
        self.vx = 0
        self.vy = 0
        self.speed = PLAYER_SPEED
        self.jump_force = PLAYER_JUMP_FORCE
        self.on_ground = True
        self.crouching = False

        # Animação
        self.direction = "right"         # "right" | "left"
        self.state = "idle"              # idle | running | crouching | airborne
        self.anim_frame = 0              # índice dentro da sequência atual
        self.anim_timer = 0.0            # acumulador de tempo
        self.is_shooting = False         # True apenas durante animação de tiro
        self._shoot_crouching = False    # se o tiro foi acionado agachado
        self._prev_state_key = "idle"    # detecta troca de estado para resetar frame
        self.idle_phase = 'wait'         # 'wait' | 'anim'
        self.idle_wait_timer = 0.0       # acumulador da espera em idle

        self.rect = pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, keys, world_w, platforms, dt):
        # Agachar: bloqueia movimento horizontal e pulo
        self.crouching = (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.on_ground

        # Movimento horizontal (bloqueado ao agachar)
        self.vx = 0
        if not self.crouching:
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.vx = -self.speed
                self.direction = "left"
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.vx = self.speed
                self.direction = "right"

        self.x += self.vx
        self.x = max(0, min(world_w - self.w, self.x))

        # Máquina de estados de movimento
        if self.crouching:
            self.state = "crouching"
        elif not self.on_ground:
            self.state = "airborne"
        elif abs(self.vx) > 0:
            self.state = "running"
        else:
            self.state = "idle"

        # Avança animação
        if self._all_frames_r:
            if self.is_shooting:
                # Timer de tiro (mais rápido)
                self.anim_timer += dt
                if self.anim_timer >= SHOOT_ANIM_INTERVAL:
                    self.anim_timer -= SHOOT_ANIM_INTERVAL
                    self.anim_frame += 1
                    seq = self.get_anim_seq()
                    if self.anim_frame >= len(seq):
                        # Animação de tiro terminou — volta ao estado normal
                        self.is_shooting = False
                        self.anim_frame = 0
                        self.anim_timer = 0.0
                        self._prev_state_key = self.state
            else:
                # Resetar frame quando estado muda
                state_key = self.state
                if state_key != self._prev_state_key:
                    self.anim_frame = 0
                    self.anim_timer = 0.0
                    if state_key == 'idle':
                        self.idle_phase = 'wait'
                        self.idle_wait_timer = 0.0
                self._prev_state_key = state_key

                if self.state == 'idle':
                    if self.idle_phase == 'wait':
                        self.idle_wait_timer += dt
                        if self.idle_wait_timer >= IDLE_WAIT_DURATION:
                            self.idle_phase = 'anim'
                            self.anim_frame = 0
                            self.anim_timer = 0.0
                    else:  # 'anim'
                        self.anim_timer += dt
                        if self.anim_timer >= IDLE_ANIM_INTERVAL:
                            self.anim_timer -= IDLE_ANIM_INTERVAL
                            self.anim_frame += 1
                            if self.anim_frame >= len(ANIM_IDLE_FRAMES):
                                self.idle_phase = 'wait'
                                self.idle_wait_timer = 0.0
                                self.anim_frame = 0
                else:
                    # Timer de corrida/pulo
                    self.anim_timer += dt
                    if self.anim_timer >= RUN_ANIM_INTERVAL:
                        self.anim_timer -= RUN_ANIM_INTERVAL
                        seq = self.get_anim_seq()
                        self.anim_frame = (self.anim_frame + 1) % len(seq)

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

    def jump(self):
        if self.on_ground and not self.crouching:
            self.vy = self.jump_force
            self.on_ground = False

    def get_anim_seq(self):
        """Retorna a lista de índices de frames para o estado atual."""
        if self.is_shooting:
            return ANIM_CROUCH_SHOOT_FRAMES if self._shoot_crouching else ANIM_SHOOT_FRAMES
        if self.state == "idle":
            if self.idle_phase == 'wait':
                return [ANIM_IDLE_WAIT_FRAME]
            return ANIM_IDLE_FRAMES
        if self.state == "crouching":
            return ANIM_CROUCH_FRAMES
        if self.state == "airborne":
            return ANIM_JUMP_FRAMES
        if self.state == "running":
            return ANIM_RUN_FRAMES
        return [ANIM_IDLE_WAIT_FRAME]

    def trigger_shoot(self):
        """Inicia a animação de tiro (chamado apenas na tecla F)."""
        self.is_shooting = True
        self._shoot_crouching = self.crouching
        self.anim_frame = 0
        self.anim_timer = 0.0

    def draw(self, surface, camera):
        screen_rect = camera.apply_rect(self.rect)

        # --- Multi-frame sprites (PNGs recortados) ---
        if self._all_frames_r:
            seq = self.get_anim_seq()
            fi = self.anim_frame % len(seq)
            idx = seq[fi]
            fd = self._all_frames_r if self.direction == "right" else self._all_frames_l
            sprite = fd.get(idx)
            if sprite:
                # Centraliza horizontalmente e ancora o pé na base do rect
                sw, sh = sprite.get_size()
                draw_x = screen_rect.x + (screen_rect.w - sw) // 2
                draw_y = screen_rect.bottom - sh
                surface.blit(sprite, (draw_x, draw_y))
                return

        # --- Legacy sprites dict (idle/run1/run2) ---
        if self.sprites:
            if self.state == "running":
                # Alterna run1/run2 usando anim_frame (0=run1, 1=run2)
                frame_name = "run1" if (self.anim_frame % 2 == 0) else "run2"
                sprite_key = f"{frame_name}_{self.direction}"
            else:
                sprite_key = f"idle_{self.direction}"
            sprite = self.sprites.get(sprite_key, self.sprites['idle_right'])
            surface.blit(sprite, screen_rect.topleft)
        else:
            # Fallback: retângulo azul
            pygame.draw.rect(surface, BLUE, screen_rect, border_radius=8)
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
    def __init__(self, x, y, direction=1, sprite=None):
        self.sprite    = sprite
        self.direction = direction
        if sprite:
            self.w = sprite.get_width()
            self.h = sprite.get_height()
        else:
            self.w = 10
            self.h = 4
        self.x = x
        self.y = y - self.h // 2   # centraliza verticalmente no ponto passado
        self.speed = 10 * direction
        self.rect = pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self):
        self.x += self.speed
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surface, camera):
        screen_rect = camera.apply_rect(self.rect)
        if self.sprite:
            spr = self.sprite if self.direction >= 0 else pygame.transform.flip(self.sprite, True, False)
            surface.blit(spr, screen_rect.topleft)
        else:
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


def load_menu_bg(rel_path: str, screen_w: int, screen_h: int):
    """
    Carrega background do menu com fallback seguro.
    """
    full = ASSETS_DIR / rel_path
    if not full.exists():
        print(f"[Menu BG] Arquivo nao encontrado: {full}. Usando fallback.")
        surf = pygame.Surface((screen_w, screen_h))
        surf.fill((15, 20, 35))  # Azul escuro para fallback
        try:
            return surf.convert()
        except:
            return surf

    try:
        img = pygame.image.load(str(full))
        if img.get_size() != (screen_w, screen_h):
            img = pygame.transform.smoothscale(img, (screen_w, screen_h))
        try:
            img = img.convert()
        except:
            pass  # Fallback para imagem sem convert em headless mode
        print(f"[Menu BG] Carregado: {full.name} size={img.get_size()}")
        return img
    except Exception as e:
        print(f"[Menu BG] Erro ao carregar {full}: {e}")
        surf = pygame.Surface((screen_w, screen_h))
        surf.fill((15, 20, 35))
        try:
            return surf.convert()
        except:
            return surf


class Button:
    """Botão do menu com suporte a mouse e teclado."""
    def __init__(self, label, x, y, width=200, height=50):
        self.label = label
        self.rect = pygame.Rect(x, y, width, height)
        self.is_hovered = False
        self.is_selected = False
    
    def update_hover(self, mouse_pos):
        """Atualiza estado de hover baseado em posição do mouse."""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def draw(self, surface, font, selected=False):
        """Desenha botão com estilo cyber."""
        # Cores base
        if selected or self.is_hovered:
            fill_color = (20, 70, 150)  # Azul mais claro no hover
            border_color = (0, 255, 255)  # Ciano neon
            border_width = 3
            text_color = (255, 255, 255)  # Branco brilhante
        else:
            fill_color = (25, 45, 90)  # Azul escuro
            border_color = (0, 180, 220)  # Ciano opaco
            border_width = 2
            text_color = (200, 200, 200)  # Branco opaco
        
        # Desenhar fundo
        pygame.draw.rect(surface, fill_color, self.rect, border_radius=8)
        
        # Desenhar borda neon
        pygame.draw.rect(surface, border_color, self.rect, width=border_width, border_radius=8)
        
        # Desenhar texto
        text_img = font.render(self.label, True, text_color)
        text_rect = text_img.get_rect(center=self.rect.center)
        surface.blit(text_img, text_rect)


def draw_button(surface, button, font, selected=False):
    """Desenha um botão do menu."""
    button.draw(surface, font, selected)


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


def cut_sheet(sheet, col, row, frame_w, frame_h):
    """Extrai uma subimagem de um sprite sheet baseado em coluna e linha."""
    return sheet.subsurface(pygame.Rect(col * frame_w, row * frame_h, frame_w, frame_h)).copy()


def load_player_sprites(scale=1.8, feet_offset=0):
    """
    Carrega sprites do player (idle, run1, run2) para direita e cria versões espelhadas para esquerda.
    Retorna: dict com {
        'idle_right', 'idle_left',
        'run1_right', 'run1_left',
        'run2_right', 'run2_left',
        'width', 'height'
    }
    """
    # Calcular tamanho final
    scaled_w = int(PLAYER_BASE_SIZE[0] * scale)
    scaled_h = int(PLAYER_BASE_SIZE[1] * scale)
    size = (scaled_w, scaled_h)
    
    # Carregar sprites da direita (usando função load_image que já tem fallback robusto)
    idle_right = load_image(PLAYER_IDLE_RIGHT, size=size, alpha=True, 
                           fallback_color=(70, 130, 220), fallback_size=size)
    run1_right = load_image(PLAYER_RUN1_RIGHT, size=size, alpha=True,
                           fallback_color=(70, 130, 220), fallback_size=size)
    run2_path = os.path.join(os.path.dirname(__file__), "assets", PLAYER_RUN2_RIGHT)
    if os.path.exists(run2_path):
        run2_right = load_image(PLAYER_RUN2_RIGHT, size=size, alpha=True,
                               fallback_color=(70, 130, 220), fallback_size=size)
    else:
        print(f"[img] Arquivo nao encontrado: {PLAYER_RUN2_RIGHT}. Usando run1 como fallback.")
        run2_right = run1_right
    
    # Criar versões espelhadas para esquerda (flip horizontal)
    try:
        idle_left = pygame.transform.flip(idle_right, True, False)
        run1_left = pygame.transform.flip(run1_right, True, False)
        run2_left = pygame.transform.flip(run2_right, True, False)
    except pygame.error:
        # Fallback: copiar as mesmas imagens se flip falhar
        idle_left = idle_right
        run1_left = run1_right
        run2_left = run2_right
    
    return {
        'idle_right': idle_right,
        'idle_left': idle_left,
        'run1_right': run1_right,
        'run1_left': run1_left,
        'run2_right': run2_right,
        'run2_left': run2_left,
        'width': scaled_w,
        'height': scaled_h,
    }


def _make_fallback_surface(size):
    """Cria uma surface de fallback azul com alpha."""
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill((70, 130, 220, 255))
    return surf


def load_warpgal_sprites(scale=PLAYER_SCALE, feet_offset=PLAYER_FEET_OFFSET):
    """
    Carrega sprites do player a partir do warpgal sprite sheet.
    Extrai frames usando WARPGAL_IDLE_ROW (idle) e WARPGAL_RUN_ROW (corrida).
    Ajuste WARPGAL_IDLE_ROW / WARPGAL_RUN_ROW nas constantes para trocar linhas.
    Retorna mesmo formato de dict que load_player_sprites().
    """
    scaled_w = int(PLAYER_BASE_SIZE[0] * scale)
    scaled_h = int(PLAYER_BASE_SIZE[1] * scale)
    size = (scaled_w, scaled_h)

    sheet_path = os.path.join(os.path.dirname(__file__), "assets", WARPGAL_SHEET)
    if os.path.exists(sheet_path):
        try:
            sheet = pygame.image.load(sheet_path).convert_alpha()
            idle_raw  = cut_sheet(sheet, 0, WARPGAL_IDLE_ROW, WARPGAL_FRAME_W, WARPGAL_FRAME_H)
            run1_raw  = cut_sheet(sheet, 0, WARPGAL_RUN_ROW,  WARPGAL_FRAME_W, WARPGAL_FRAME_H)
            run2_raw  = cut_sheet(sheet, 4, WARPGAL_RUN_ROW,  WARPGAL_FRAME_W, WARPGAL_FRAME_H)
            idle_right = pygame.transform.smoothscale(idle_raw, size)
            run1_right = pygame.transform.smoothscale(run1_raw, size)
            run2_right = pygame.transform.smoothscale(run2_raw, size)
            print(f"[warpgal] Sprites carregados: idle(row={WARPGAL_IDLE_ROW}) run(row={WARPGAL_RUN_ROW}, cols 0+4) -> {size}")
        except Exception as e:
            print(f"[warpgal] Erro ao carregar sheet: {e}. Usando fallback.")
            idle_right = run1_right = run2_right = _make_fallback_surface(size)
    else:
        print(f"[warpgal] Sheet nao encontrado: {WARPGAL_SHEET}. Usando fallback.")
        idle_right = run1_right = run2_right = _make_fallback_surface(size)

    idle_left  = pygame.transform.flip(idle_right, True, False)
    run1_left  = pygame.transform.flip(run1_right, True, False)
    run2_left  = pygame.transform.flip(run2_right, True, False)

    return {
        'idle_right': idle_right,
        'idle_left':  idle_left,
        'run1_right': run1_right,
        'run1_left':  run1_left,
        'run2_right': run2_right,
        'run2_left':  run2_left,
        'width':  scaled_w,
        'height': scaled_h,
    }


def load_split_player_sprites(scale=PLAYER_SCALE):
    """
    Carrega sprites do player a partir de arquivos individuais no formato:
    assets/images/player/Layer 1_sprite_XXX.png

    Retorna dict com:
      - Chaves legado: idle_right, run1_right, run2_right (e versões _left)
      - Novas chaves: all_frames (idx → Surface direita), size
    """
    scaled_w = int(PLAYER_BASE_SIZE[0] * scale)
    scaled_h = int(PLAYER_BASE_SIZE[1] * scale)
    size = (scaled_w, scaled_h)

    split_dir = ASSETS_DIR / "images" / "player"
    files = sorted(split_dir.glob("Layer 1_sprite_*.png"))
    if not files:
        print(f"[player split] Nenhum arquivo encontrado em: {PLAYER_SPLIT_GLOB}")
        return None

    # Carrega TODOS os frames para suporte a multi-animação
    all_frames: dict = {}
    for sprite_file in files:
        match = re.search(r"sprite_(\d+)\.png$", sprite_file.name)
        if not match:
            continue
        idx = int(match.group(1))
        surf = load_image(
            f"images/player/{sprite_file.name}",
            size=size, alpha=True,
            fallback_color=(70, 130, 220), fallback_size=size,
        )
        all_frames[idx] = surf

    if not all_frames:
        print("[player split] Arquivos encontrados, mas sem índice válido.")
        return None

    available = sorted(all_frames.keys())

    def resolve(target_idx):
        if target_idx in all_frames:
            return all_frames[target_idx]
        best = min(available, key=lambda k: abs(k - target_idx))
        return all_frames[best]

    idle_right = resolve(PLAYER_SPLIT_IDLE_IDX)
    run1_right = resolve(PLAYER_SPLIT_RUN1_IDX)
    run2_right = resolve(PLAYER_SPLIT_RUN2_IDX)

    idle_left = pygame.transform.flip(idle_right, True, False)
    run1_left = pygame.transform.flip(run1_right, True, False)
    run2_left = pygame.transform.flip(run2_right, True, False)

    print(
        f"[player split] {len(all_frames)} frames carregados "
        f"(idle={PLAYER_SPLIT_IDLE_IDX}, run1={PLAYER_SPLIT_RUN1_IDX}, "
        f"run2={PLAYER_SPLIT_RUN2_IDX}) -> {size}"
    )

    return {
        # Chaves legado
        'idle_right': idle_right, 'idle_left': idle_left,
        'run1_right': run1_right, 'run1_left': run1_left,
        'run2_right': run2_right, 'run2_left': run2_left,
        'width': scaled_w, 'height': scaled_h,
        # Novas chaves para multi-frame
        'all_frames': all_frames,
        'size': size,
    }


def load_player_sprite_set(scale=PLAYER_SCALE, feet_offset=PLAYER_FEET_OFFSET):
    """
    Prioridade de carregamento:
    1) Warpgal sprite sheet (legado)
    2) Sprites recortados individuais (Layer 1_sprite_XXX)
    3) Fallback interno
    """
    warpgal_sprites = load_warpgal_sprites(scale=scale, feet_offset=feet_offset)
    split_available = any((ASSETS_DIR / "images/player").glob("Layer 1_sprite_*.png"))

    # Se o warpgal não existir, load_warpgal_sprites cai em fallback azul.
    # Nessa situação, priorizamos os sprites recortados se existirem.
    warpgal_path = ASSETS_DIR / WARPGAL_SHEET
    if not warpgal_path.exists() and split_available:
        split_sprites = load_split_player_sprites(scale=scale)
        if split_sprites is not None:
            return split_sprites

    return warpgal_sprites


def load_bullet_sprite():
    """
    Carrega sprite de bullet do shooties sheet.
    Ajuste BULLET_FRAME_IDX (0-6) para trocar o estilo de projetil.
    Retorna surface ou None (usa retangulo amarelo como fallback).
    """
    path = os.path.join(os.path.dirname(__file__), "assets", BULLET_SHEET)
    if not os.path.exists(path):
        print(f"[bullet] Sheet nao encontrado: {BULLET_SHEET}. Usando fallback retangulo.")
        return None
    try:
        sheet = pygame.image.load(path).convert_alpha()
        frame = cut_sheet(sheet, BULLET_FRAME_IDX, 0, BULLET_FRAME_W, BULLET_FRAME_H)
        print(f"[bullet] Sprite carregado: frame {BULLET_FRAME_IDX} ({BULLET_FRAME_W}x{BULLET_FRAME_H})")
        return frame
    except Exception as e:
        print(f"[bullet] Erro ao carregar bullet sprite: {e}")
        return None


def draw_menu(screen, menu_bg, buttons, selected_button_idx, font_title, font_ui, show_controls=False):
    """
    Renderiza o menu com background, overlay, título, botões e opcionalmente controles.
    """
    # Desenhar background
    screen.blit(menu_bg, (0, 0))
    
    # Aplicar overlay escuro semitransparente para legibilidade
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(100)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Título
    draw_text(screen, "PYTHON 2D GAME DEMO", font_title, WHITE, WIDTH // 2, 80, center=True)
    
    # Desenhar botões
    for idx, button in enumerate(buttons):
        is_selected = (idx == selected_button_idx)
        draw_button(screen, button, font_ui, selected=is_selected)
    
    # Se mostrando controles, exibir no lugar dos botões
    if show_controls:
        draw_text(screen, "CONTROLES", font_ui, YELLOW, WIDTH // 2, 200, center=True)
        draw_text(screen, "A/D ou <-/-> : Mover | SPACE/W/^ : Pular", 
                 pygame.font.SysFont("arial", 20), WHITE, WIDTH // 2, 260, center=True)
        draw_text(screen, "F : Atirar | ESC : Menu", 
                 pygame.font.SysFont("arial", 20), WHITE, WIDTH // 2, 290, center=True)
        draw_text(screen, "[Pressione ESC para voltar]", 
                 pygame.font.SysFont("arial", 18), GRAY, WIDTH // 2, 400, center=True)


def draw_generic_menu_screen(screen, menu_bg, buttons, selected_button_idx, font_title, font_ui,
                             screen_title, subtitle="", title_color=WHITE):
    """
    Renderiza tela genérica (menu, game_over, etc) com background, overlay, título, botões.
    Reutilizável para múltiplas telas com visual consistente.
    """
    # Desenhar background
    screen.blit(menu_bg, (0, 0))
    
    # Aplicar overlay escuro semitransparente para legibilidade
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(100)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Título principal
    draw_text(screen, screen_title, font_title, title_color, WIDTH // 2, 100, center=True)
    
    # Subtítulo se fornecido
    if subtitle:
        draw_text(screen, subtitle, pygame.font.SysFont("arial", 22), YELLOW, 
                 WIDTH // 2, 160, center=True)
    
    # Desenhar botões
    for idx, button in enumerate(buttons):
        is_selected = (idx == selected_button_idx)
        draw_button(screen, button, font_ui, selected=is_selected)


def handle_generic_screen_input(event, screen_state, num_buttons=3):
    """
    Processa input genérico para telas com botões (menu, game_over, etc).
    Retorna: (new_selected_idx, action_index, show_controls)
    action_index: índice do botão pressionado, ou None se nenhum
    """
    selected_idx = screen_state.get("selected", 0)
    show_controls = screen_state.get("show_controls", False)
    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            selected_idx = (selected_idx - 1) % num_buttons
            return selected_idx, None, show_controls
        elif event.key == pygame.K_DOWN:
            selected_idx = (selected_idx + 1) % num_buttons
            return selected_idx, None, show_controls
        elif event.key == pygame.K_RETURN:
            # Retorna índice do botão selecionado como ação
            return selected_idx, selected_idx, show_controls
        elif event.key == pygame.K_ESCAPE:
            # ESC cancela (retorna ação especial -1)
            return selected_idx, -1, show_controls
    
    return selected_idx, None, show_controls


def handle_menu_input(event, menu_state):
    """
    Processa input do menu (teclado e mouse).
    Retorna: (new_selected_idx, action, show_controls)
    Ações: None, 'play', 'controls', 'quit'
    """
    selected_idx = menu_state.get("selected", 0)
    show_controls = menu_state.get("show_controls", False)
    
    if event.type == pygame.KEYDOWN:
        if show_controls:
            if event.key == pygame.K_ESCAPE:
                return selected_idx, None, False
        else:
            if event.key == pygame.K_UP:
                selected_idx = (selected_idx - 1) % 3
                return selected_idx, None, show_controls
            elif event.key == pygame.K_DOWN:
                selected_idx = (selected_idx + 1) % 3
                return selected_idx, None, show_controls
            elif event.key == pygame.K_RETURN:
                actions = ['play', 'controls', 'quit']
                return selected_idx, actions[selected_idx], False
            elif event.key == pygame.K_ESCAPE:
                return selected_idx, 'quit', False
    
    return selected_idx, None, show_controls


def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


def generate_reachable_platforms(world_w, ground_y, goal_x, seed=None):
    rng = random.Random(seed) if seed is not None else random
    platforms = []
    main_route = []

    def overlaps_any(rect, existing, h_pad=8, v_pad=20):
        """Retorna True se 'rect' sobrépõe qualquer plataforma existente."""
        expanded = rect.inflate(h_pad * 2, v_pad * 2)
        return any(expanded.colliderect(p.rect) for p in existing)

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
            candidate = Platform(x, y, width, 16)
            if not overlaps_any(candidate.rect, platforms):
                platform = candidate
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
                candidate_b = Platform(branch_x, branch_y, branch_w, 16)
                if not overlaps_any(candidate_b.rect, platforms):
                    platforms.append(candidate_b)
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

    # Remover sobreposições residuais (ex.: branch perto de plataforma ajustada)
    clean = []
    for p in platforms:
        expanded = p.rect.inflate(8 * 2, 20 * 2)
        if not any(expanded.colliderect(q.rect) for q in clean):
            clean.append(p)
    platforms = clean
    main_route = [p for p in main_route if p in clean]

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

    # Carregar sprites do player (warpgal ou fallback split) e bullet
    player_sprites = load_player_sprite_set(scale=PLAYER_SCALE, feet_offset=PLAYER_FEET_OFFSET)
    bullet_sprite  = load_bullet_sprite()
    player = Player(sprites=player_sprites)
    coins, platforms, main_route, platform_debug, goal = build_level()
    bullets = []
    enemies = []
    effects = []
    camera = Camera(WIDTH, HEIGHT, WORLD_W, WORLD_H)
    
    # Carregar fundo único e fixo
    bg_gameplay = load_background(BG_PATH, WIDTH, HEIGHT)
    
    # Carregar menu background e criar botões
    menu_bg = load_menu_bg("images/ui/menu_bg.png", WIDTH, HEIGHT)
    buttons = [
        Button("JOGAR", WIDTH // 2 - 100, 220, 200, 50),
        Button("CONTROLES", WIDTH // 2 - 100, 290, 200, 50),
        Button("SAIR", WIDTH // 2 - 100, 360, 200, 50),
    ]
    menu_state = {"selected": 0, "show_controls": False}
    
    # Botões para GAME_OVER (mesma posição vertical para consistência)
    game_over_buttons = [
        Button("REINICIAR", WIDTH // 2 - 100, 220, 200, 50),
        Button("MENU PRINCIPAL", WIDTH // 2 - 100, 290, 200, 50),
        Button("SAIR", WIDTH // 2 - 100, 360, 200, 50),
    ]
    game_over_state = {"selected": 0}
    
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

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # segundos por frame

        # ========= Eventos =========
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == MENU:
                selected_idx, action, show_controls = handle_menu_input(event, menu_state)
                menu_state["selected"] = selected_idx
                menu_state["show_controls"] = show_controls
                
                if action == 'play':
                    # Iniciar jogo
                    player = Player(sprites=player_sprites)
                    coins, platforms, main_route, platform_debug, goal = build_level()
                    bullets = []
                    enemies = []
                    effects = []
                    spawn_manager = SpawnManager(WORLD_W, WIDTH, goal.x)
                    goal.image = goal_image
                    kills = 0
                    score = 0
                    time_survived = 0.0
                    state = PLAYING
                elif action == 'controls':
                    menu_state["show_controls"] = True
                elif action == 'quit':
                    running = False
                
                # Atualizar hover do mouse
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    button.update_hover(mouse_pos)
                
                # Verificar clique em botões
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for idx, button in enumerate(buttons):
                        if button.rect.collidepoint(mouse_pos):
                            actions = ['play', 'controls', 'quit']
                            action = actions[idx]
                            if action == 'play':
                                player = Player(sprites=player_sprites)
                                coins, platforms, main_route, platform_debug, goal = build_level()
                                bullets = []
                                enemies = []
                                effects = []
                                spawn_manager = SpawnManager(WORLD_W, WIDTH, goal.x)
                                goal.image = goal_image
                                kills = 0
                                score = 0
                                time_survived = 0.0
                                state = PLAYING
                            elif action == 'controls':
                                menu_state["show_controls"] = True
                            elif action == 'quit':
                                running = False

            elif state == PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                        player.jump()
                    elif event.key == pygame.K_f:
                        bdir = 1 if player.direction == "right" else -1
                        bx = player.x + player.w if bdir == 1 else player.x
                        by_offset = 0.75 if player.crouching else 0.5
                        bullets.append(Bullet(bx, player.y + player.h * by_offset,
                                              direction=bdir, sprite=bullet_sprite))
                        player.trigger_shoot()
                    elif event.key == pygame.K_ESCAPE:
                        state = MENU

            elif state == GAME_OVER:
                # Processar input com função genérica
                selected_idx, action_idx, _ = handle_generic_screen_input(event, game_over_state, num_buttons=3)
                game_over_state["selected"] = selected_idx
                
                # Atualizar hover do mouse
                mouse_pos = pygame.mouse.get_pos()
                for button in game_over_buttons:
                    button.update_hover(mouse_pos)
                
                # Executar ação baseada no índice do botão ou input
                if action_idx is not None:
                    if action_idx == 0:  # REINICIAR
                        player = Player(sprites=player_sprites)
                        coins, platforms, main_route, platform_debug, goal = build_level()
                        bullets = []
                        enemies = []
                        effects = []
                        spawn_manager = SpawnManager(WORLD_W, WIDTH, goal.x)
                        goal.image = goal_image
                        kills = 0
                        score = 0
                        time_survived = 0.0
                        state = PLAYING
                    elif action_idx == 1:  # MENU PRINCIPAL
                        state = MENU
                    elif action_idx == 2:  # SAIR
                        running = False
                    elif action_idx == -1:  # ESC = MENU PRINCIPAL
                        state = MENU
                
                # Verificar clique em botões
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for idx, button in enumerate(game_over_buttons):
                        if button.rect.collidepoint(mouse_pos):
                            if idx == 0:  # REINICIAR
                                player = Player(sprites=player_sprites)
                                coins, platforms, main_route, platform_debug, goal = build_level()
                                bullets = []
                                enemies = []
                                effects = []
                                spawn_manager = SpawnManager(WORLD_W, WIDTH, goal.x)
                                goal.image = goal_image
                                kills = 0
                                score = 0
                                time_survived = 0.0
                                state = PLAYING
                            elif idx == 1:  # MENU PRINCIPAL
                                state = MENU
                            elif idx == 2:  # SAIR
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
                    score += SCORE_COLLECTIBLE
                else:
                    remaining_coins.append(c)
            coins = remaining_coins

            time_survived += dt

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
            draw_menu(screen, menu_bg, buttons, menu_state["selected"], font_title, font_ui, 
                     show_controls=menu_state["show_controls"])

        elif state == PLAYING:
            # Fundo fixo único
            screen.blit(bg_gameplay, (0, 0))

            # Chao (mundo) - estilo neon cyber
            gr = camera.apply_rect(pygame.Rect(0, GROUND_Y, WORLD_W, HEIGHT - GROUND_Y))
            pygame.draw.rect(screen, PLATFORM_SHADOW, gr)                     # fundo escuro
            strip = pygame.Rect(gr.x, gr.y, gr.width, 8)
            pygame.draw.rect(screen, PLATFORM_FILL, strip)                    # faixa azul-escuro
            line_start = camera.apply_pos(0, GROUND_Y)
            line_end   = camera.apply_pos(WORLD_W, GROUND_Y)
            pygame.draw.line(screen, PLATFORM_TOP,  line_start, line_end, 2)  # linha ciano neon
            pygame.draw.line(screen, PLATFORM_GLOW, (line_start[0], line_start[1] + 3),
                             (line_end[0], line_end[1] + 3), 1)               # sublinha roxo neon

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
            # Reutilizar função genérica com dados específicos de GAME_OVER
            best_score = max(best_score, score)
            subtitle = f"Score: {score} | Zumbis: {kills} | Melhor: {best_score}"
            draw_generic_menu_screen(screen, menu_bg, game_over_buttons, game_over_state["selected"],
                                    font_title, font_ui, "GAME OVER", subtitle=subtitle)

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
