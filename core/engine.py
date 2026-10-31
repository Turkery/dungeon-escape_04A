from enum import Enum, auto
import pygame
from loaders.level_loader import load_level_data
from models.level import Level


class GameState(Enum):
    START_MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    VICTORY = auto()


class GameEngine:
    def __init__(self, level_path: str):
        pygame.init()
        pygame.display.set_caption("Dungeon Escape (04A)")
        
        # 1. Incarcare nivel
        raw_level = load_level_data(level_path)
        self.level = Level(raw_level)

        # 2. Fereastra si display bazat pe tile_size
        self.screen_width = self.level.grid_width * self.level.tile_size
        self.screen_height = self.level.grid_height * self.level.tile_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.clock = pygame.time.Clock()
        self.is_running = True
        self.state = GameState.PLAYING

        # Coordonate jucator in pixeli (pentru demonstrare delta-time)
        self.player_x = float(self.level.player_start[0] * self.level.tile_size)
        self.player_y = float(self.level.player_start[1] * self.level.tile_size)
        self.player_speed = 150.0  # pixeli pe secunda

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    # Comutare Pauza
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                elif event.key == pygame.K_ESCAPE:
                    self.is_running = False

    def update(self, dt: float):
        """Actualizeaza logica doar cand jocul este in starea PLAYING."""
        if self.state != GameState.PLAYING:
            return

        keys = pygame.key.get_pressed()
        dx, dy = 0.0, 0.0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1.0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1.0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1.0
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1.0

        # Miscare independenta de framerate prin delta time
        self.player_x += dx * self.player_speed * dt
        self.player_y += dy * self.player_speed * dt

    def render(self):
        self.screen.fill((20, 20, 25))  # Fundal dungeon

        # Desenare pereti (patrate gri)
        for wx, wy in self.level.walls:
            rect = pygame.Rect(
                wx * self.level.tile_size,
                wy * self.level.tile_size,
                self.level.tile_size,
                self.level.tile_size
            )
            pygame.draw.rect(self.screen, (80, 80, 90), rect)

        # Desenare jucator (patrat albastru deschis)
        p_size = self.level.tile_size - 4
        player_rect = pygame.Rect(self.player_x + 2, self.player_y + 2, p_size, p_size)
        pygame.draw.rect(self.screen, (60, 160, 240), player_rect)

        # Overlay cand jocul e in pauza
        if self.state == GameState.PAUSED:
            font = pygame.font.SysFont(None, 48)
            pause_surface = font.render("PAUZA (Apasa P)", True, (240, 240, 240))
            self.screen.blit(pause_surface, (self.screen_width // 2 - 120, self.screen_height // 2 - 24))

        pygame.display.flip()

    def run(self):
        """Bucla principala a jocului (Game Loop)."""
        while self.is_running:
            # dt in secunde (ex: 1/60 ~ 0.016s)
            dt = self.clock.tick(60) / 1000.0
            self.handle_events()
            self.update(dt)
            self.render()

        pygame.quit()