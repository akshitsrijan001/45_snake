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
        self.font = pygame.font.SysFont("Arial", 30)

        self.moves_per_second = 8
        self.frame_counter = 0

        self.game_over = False
        self.game_over_logged = False

    def handle_keydown(self, key):
        # If the game is already over, any key closes the game.
        if self.game_over:
            return True

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
        # Reserved for continuously-held-key input.
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
            return

        # Self collision
        if self.snake.collides_with_self():
            self.game_over = True
            return

        # Food collision
        if self.snake.head_rect().colliderect(self.food.rect()):
            self.snake.grow()
            self.score += 1
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

        # Draw Game Over screen
        if self.game_over:
            game_over_text = self.font.render(
                "GAME OVER",
                True,
                RED
            )

            final_score_text = self.font.render(
                f"Final Score: {self.score}",
                True,
                WHITE
            )

            instruction_text = self.font.render(
                "Press any key to exit",
                True,
                WHITE
            )

            screen.blit(
                game_over_text,
                game_over_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 - 60
                    )
                )
            )

            screen.blit(
                final_score_text,
                final_score_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2
                    )
                )
            )

            screen.blit(
                instruction_text,
                instruction_text.get_rect(
                    center=(
                        self.width // 2,
                        self.height // 2 + 60
                    )
                )
            )