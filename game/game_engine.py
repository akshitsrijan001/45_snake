import math
from array import array

import pygame

from .snake import Snake
from .food import Food


WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (220, 60, 60)


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell_size = 20

        self.grid_width = width // self.cell_size
        self.grid_height = height // self.cell_size

        self.font = pygame.font.SysFont("Arial", 30)

        self.difficulties = {
            "Easy": 5,
            "Medium": 8,
            "Hard": 12
        }

        self.difficulty = "Medium"
        self.moves_per_second = self.difficulties[self.difficulty]

        # Initialize mixer for sound effects
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        self.eat_sound = self.create_tone(800, 0.08)
        self.game_over_sound = self.create_tone(220, 0.25)

        self.reset_game()

    def create_tone(self, frequency, duration):
        sample_rate = 44100
        samples = array("h")

        for i in range(int(sample_rate * duration)):
            value = int(
                16000 * math.sin(
                    2 * math.pi * frequency * i / sample_rate
                )
            )
            samples.append(value)

        return pygame.mixer.Sound(buffer=samples)

    def reset_game(self):
        self.snake = Snake(
            self.grid_width // 2,
            self.grid_height // 2,
            self.cell_size
        )

        self.food = Food(
            self.grid_width,
            self.grid_height,
            self.cell_size
        )

        self.score = 0
        self.frame_counter = 0
        self.game_over = False

    def start_new_game(self, difficulty):
        self.difficulty = difficulty
        self.moves_per_second = self.difficulties[difficulty]
        self.reset_game()

    def handle_keydown(self, key):
        # Game-over menu
        if self.game_over:
            if key in (pygame.K_1, pygame.K_KP1):
                self.start_new_game("Easy")
            elif key in (pygame.K_2, pygame.K_KP2):
                self.start_new_game("Medium")
            elif key in (pygame.K_3, pygame.K_KP3):
                self.start_new_game("Hard")
            elif key in (pygame.K_4, pygame.K_KP4, pygame.K_ESCAPE):
                return True

            return False

        # Normal game controls
        if key in (pygame.K_UP, pygame.K_w):
            self.snake.set_direction(0, -1)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.snake.set_direction(0, 1)
        elif key in (pygame.K_LEFT, pygame.K_a):
            self.snake.set_direction(-1, 0)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.snake.set_direction(1, 0)

        return False

    def handle_input(self):
        pass

    def update(self):
        if self.game_over:
            return

        self.frame_counter += 1

        frames_per_move = max(
            1,
            int(60 / self.moves_per_second)
        )

        if self.frame_counter < frames_per_move:
            return

        self.frame_counter = 0

        self.snake.move()

        # Wall collision
        if self.snake.collides_with_wall(
            self.grid_width,
            self.grid_height
        ):
            self.game_over = True
            self.game_over_sound.play()
            return

        # Self collision
        if self.snake.collides_with_self():
            self.game_over = True
            self.game_over_sound.play()
            return

        # Food collision
        if self.snake.head_rect().colliderect(self.food.rect()):
            self.snake.grow()
            self.score += 1
            self.eat_sound.play()
            self.food.respawn(self.snake.body)

    def render(self, screen):
        # Draw food
        pygame.draw.rect(
            screen,
            RED,
            self.food.rect()
        )

        # Draw snake
        for rect in self.snake.segment_rects():
            pygame.draw.rect(
                screen,
                GREEN,
                rect
            )

        # Draw score
        score_text = self.font.render(
            f"Score: {self.score}",
            True,
            WHITE
        )
        screen.blit(score_text, (10, 10))

        # Draw Game Over menu
        if self.game_over:
            title = self.font.render(
                "GAME OVER",
                True,
                RED
            )

            final_score = self.font.render(
                f"Final Score: {self.score}",
                True,
                WHITE
            )

            menu1 = self.font.render(
                "1 - Easy",
                True,
                WHITE
            )

            menu2 = self.font.render(
                "2 - Medium",
                True,
                WHITE
            )

            menu3 = self.font.render(
                "3 - Hard",
                True,
                WHITE
            )

            menu4 = self.font.render(
                "4 - Exit",
                True,
                WHITE
            )

            screen.blit(
                title,
                title.get_rect(
                    center=(self.width // 2, self.height // 2 - 120)
                )
            )

            screen.blit(
                final_score,
                final_score.get_rect(
                    center=(self.width // 2, self.height // 2 - 70)
                )
            )

            screen.blit(
                menu1,
                menu1.get_rect(
                    center=(self.width // 2, self.height // 2 - 20)
                )
            )

            screen.blit(
                menu2,
                menu2.get_rect(
                    center=(self.width // 2, self.height // 2 + 20)
                )
            )

            screen.blit(
                menu3,
                menu3.get_rect(
                    center=(self.width // 2, self.height // 2 + 60)
                )
            )

            screen.blit(
                menu4,
                menu4.get_rect(
                    center=(self.width // 2, self.height // 2 + 100)
                )
            )