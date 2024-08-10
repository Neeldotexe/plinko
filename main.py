import ctypes, pygame, pymunk, random, sys
from ball import Ball
from board import *
from multis import *
from settings import *

# Maintain resolution regardless of Windows scaling settings
ctypes.windll.user32.SetProcessDPIAware()

class Game:
    def __init__(self):
        # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE_STRING)
        self.clock = pygame.time.Clock()
        self.delta_time = 0

        # Pymunk
        self.space = pymunk.Space()
        self.space.gravity = (0, 1800)

        # Plinko setup
        self.ball_group = pygame.sprite.Group()
        self.board = Board(self.space)

        # Betting setup
        self.balance = 1000
        self.bet_amount = 100
        self.min_bet = 1
        self.max_bet = 1000
        self.win_streak = 0 
        self.recent_outcomes = []
        # Load button images
        self.increase_bet_img = pygame.image.load("graphics/increase.png").convert_alpha()
        self.decrease_bet_img = pygame.image.load("graphics/decrease.png").convert_alpha()
        self.button_width = 50  # New width
        self.button_height = 50  # New height
        self.increase_img = pygame.transform.scale(self.increase_bet_img, (self.button_width, self.button_height))
        self.decrease_img = pygame.transform.scale(self.decrease_bet_img, (self.button_width, self.button_height))
        # Create button rectangles
        self.increase_bet_rect = self.increase_bet_img.get_rect(center=(WIDTH / 6+80, HEIGHT // 2+200))
        self.decrease_bet_rect = self.decrease_bet_img.get_rect(center=(WIDTH // 6-80, HEIGHT // 2+200 ))

        # Debugging
        self.balls_played = 0
    # def increase_bet(self):
    #     if self.bet < 800:
    #         self.bet += 100  # Increase bet normally
    #     else:
    #         self.player_money -= 100  # Start losing money when bet is 5000 or more

    #     self.check_player_money()

    # def decrease_bet(self):
    #     if self.bet > 0:
    #         self.bet -= 100  # Decrease bet

    #     self.check_player_money()

    # def player_wins(self, amount_won):
    #     """Call this method when the player wins."""
    #     self.player_money += amount_won
    #     self.win_streak += 1

    #     self.recent_outcomes.append('win')
    #     if len(self.recent_outcomes) > 4:
    #         self.recent_outcomes.pop(0)  # Keep the list to the last 4 outcomes

    #     if self.win_streak >= 4:
    #         # If the player has won 4 times in a row, they lose more than they won
    #         self.player_money -= amount_won * 1.5  # Adjust multiplier as needed
    #         print(f"Win streak penalty! Lost {amount_won * 1.5} money.")
    #     self.check_player_money()

    # def player_loses(self, amount_lost):
    #     """Call this method when the player loses."""
    #     self.player_money -= amount_lost
    #     self.win_streak = 0  # Reset the win streak
    #     self.recent_outcomes.append('lose')
    #     if len(self.recent_outcomes) > 4:
    #         self.recent_outcomes.pop(0)  # Keep the list to the last 4 outcomes

    #     self.check_player_money()

    # def check_player_money(self):
    #     if self.player_money <= 0:
    #         self.player_money = 0  # Prevent negative money
    #         # Trigger game over or similar logic
    #         print("Game Over: You're out of money!")
    
    # def check_recent_outcomes(self):
    #     """Check if the player has recently won or lost."""
    #     if 'win' in self.recent_outcomes[-1:]:  # Last outcome was a win
    #         return 'win'
    #     elif 'lose' in self.recent_outcomes[-1:]:  # Last outcome was a loss
    #         return 'lose'
    #     else:
    #         return None  # No recent outcomes or other cases
    
    def run(self):
        self.start_time = pygame.time.get_ticks()

        while True:
            # Handle quit operation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.increase_bet_rect.collidepoint(mouse_pos) and self.bet_amount < self.max_bet:
                        self.bet_amount += 1
                    elif self.decrease_bet_rect.collidepoint(mouse_pos) and self.bet_amount > self.min_bet:
                        self.bet_amount -= 1
                    elif self.board.play_rect.collidepoint(mouse_pos):
                        self.board.pressing_play = True
                    else:
                        self.board.pressing_play = False
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.board.pressing_play:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.board.play_rect.collidepoint(mouse_pos):
                        if self.balance >= self.bet_amount:
                            random_x = WIDTH//2 + random.choice([random.randint(-20, -1), random.randint(1, 20)])
                            click.play()
                            self.ball = Ball((random_x, 20), self.space, self.board, self.delta_time, self)
                            self.ball_group.add(self.ball)
                            self.board.pressing_play = False
                            self.balance -= self.bet_amount
                        else:
                            print("Insufficient balance")
                    else:
                        self.board.pressing_play = False

            self.screen.fill(BG_COLOR)

            # Time variables
            self.delta_time = self.clock.tick(FPS) / 1000.0

            # Pymunk
            self.space.step(self.delta_time)
            self.board.update()
            self.ball_group.update()

            # Display balance and bet amount
            self.display_balance_and_bet()

            # Display buttons
            self.screen.blit(self.increase_bet_img, self.increase_bet_rect)
            self.screen.blit(self.decrease_bet_img, self.decrease_bet_rect)

            pygame.display.update()

    def display_balance_and_bet(self):
        font = pygame.font.SysFont(None, 36)
        balance_text = font.render(f"Balance: {self.balance}", True, (255, 255, 255))
        bet_text = font.render(f"Bet Amount: {self.bet_amount}", True, (255, 255, 255))
        self.screen.blit(balance_text, (WIDTH // 12, HEIGHT // 2 - 100))
        self.screen.blit(bet_text, (WIDTH // 12, HEIGHT // 2 - 50))

if __name__ == '__main__':
    game = Game()
    game.run()
