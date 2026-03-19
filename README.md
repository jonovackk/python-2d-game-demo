# 🎮 Neon Firewall — Python 2D Game

> Side-scrolling action game built with Python and Pygame as a university project.  
> Discipline: *Linguagem de Programação Aplicada* — UNINTER

---

## 📸 Preview

| Menu | Gameplay |
|---|---|
| ![Menu](docs/Screenshot%20from%202026-03-19%2010-11-14.png) | ![Gameplay](docs/Screenshot%20from%202026-03-19%2010-11-37.png) |
---

## 🕹️ Gameplay

You play as a hacker navigating a neon-lit cyberpunk world, shooting through waves of enemies to reach the exit terminal. The difficulty scales as you progress.

**Controls:**

| Key | Action |
|---|---|
| `A` / `←` | Move left |
| `D` / `→` | Move right |
| `W` / `↑` / `Space` | Jump |
| `S` / `↓` | Crouch |
| `F` | Shoot |
| `Esc` | Pause / Back to menu |

---

## ⚙️ Features

- **4 enemy types** — each with unique HP, speed, sprite animations, and spawn weight
- **Procedural level generation** — segments dynamically generated as plain ground, cover obstacles, and elevated reachable platforms
- **Custom physics engine** — gravity, jumping, and platform collision built from scratch
- **Camera with dead zone** — smooth horizontal scrolling that follows the player
- **Sprite animation state machine** — idle (with wait phase), run, crouch, shoot, airborne — all frame-timed
- **Progressive difficulty** — enemy spawn cooldown decreases and speed multiplier increases over time
- **Full HUD** — score, lives, timer, and game states (menu, playing, game over, level complete)
- **Keyboard & mouse navigation** — menus work with both input methods
- **Neon visual style** — custom color palette with glow effects on platforms and UI

---

## 🏗️ Architecture

The game is structured around a set of independent, reusable classes:

```
main.py
├── Camera          — tracks player position with configurable dead zone
├── Player          — movement, physics, animation state machine, hitbox
├── Enemy           — per-type config, frame animation, hitbox, slow factor
├── Bullet          — directional projectile with sprite support
├── Platform        — collidable/decorative tiles with 3 visual kinds
├── Coin            — collectible item with image or fallback rendering
├── Goal            — level exit with collision detection
└── Button          — interactive menu button with hover and keyboard states
```

Supporting functions: `load_image`, `load_font`, `load_sound`, `load_background`, `load_player_sprites`, `load_warpgal_sprites`, `cut_sheet` (sprite sheet slicing).

---

## 🛠️ Tech Stack

- **Python 3.x**
- **Pygame** — rendering, input, sound, sprite handling
- **PyInstaller** — Windows executable packaging (`.spec` included)
- **GitHub Actions** — CI/CD workflow

---

## 🚀 How to Run

```bash
# Clone the repository
git clone https://github.com/jonovackk/python-2d-game-demo.git
cd python-2d-game-demo

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

**Requirements:** Python 3.8+ and Pygame (see `requirements.txt`)

---

## 📦 Build (Windows Executable)

```bash
pyinstaller main_windows.spec
```

The packaged executable will be in the `dist/` folder.

---

## 📁 Project Structure

```
python-2d-game-demo/
├── main.py                        # Game source (all logic, ~2000 lines)
├── requirements.txt
├── main_windows.spec              # PyInstaller build config
├── assets/
│   ├── images/
│   │   ├── player/                # Player sprite sheet and frames
│   │   ├── enemies/               # enemy1–4 sprite sequences
│   │   ├── bullets/
│   │   ├── coin/
│   │   ├── goal/
│   │   └── background/
│   └── fonts/                     # Orbitron (HUD and title)
├── .github/workflows/             # CI/CD pipeline
└── *.md                           # Design and change documentation
```

---

## 📝 Design Documentation

The repository includes detailed markdown docs tracking design decisions made during development:

- `MODIFICATIONS.md` — general changes log
- `MENU_GUIDE.md` / `MENU_UPDATE.md` — menu system design
- `MAPPING_CHANGES.md` — level generation adjustments
- `COMPONENT_REUSABILITY.md` — notes on reusable component structure
- `GAME_OVER_STANDARDIZATION.md` — game state flow standardization
- `PLAYER_SPRITES_INTEGRATION.md` — sprite sheet integration notes

---

## 👤 Author

**Jonathan Novack**  
Systems Analysis & Development — UNINTER  
42 Luxembourg (C/C++ track)

[LinkedIn](https://linkedin.com/in/jonathan-novack-dev) · [GitHub](https://github.com/jonovackk)

---

## 📄 License

This project was developed for academic purposes. Asset licenses may vary — see individual asset sources for details.
