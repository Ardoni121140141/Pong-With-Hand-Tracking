import cv2
import mediapipe as mp
import pygame
import time
from paddle import Paddle
from game import Game

# Inisialisasi Pygame
pygame.init()

# Konstanta Game
WIDTH, HEIGHT = 800, 600
FPS = 60

# Warna menggunakan format RGB
BALL_COLOR = (0, 0, 255)  # Merah
PADDLE_COLOR = (0, 255, 0)  # Hijau
SCORE_COLOR = (255, 255, 0)  # Kuning
WINNER_COLOR = (255, 0, 0)  # Merah
TIMER_COLOR = (255, 255, 255)  # Putih
BACKGROUND_COLOR = (0, 0, 0)  # Latar belakang hitam

# Inisialisasi layar
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong with Hand Tracking")

# Inisialisasi MediaPipe Hand Tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Video Capture untuk MediaPipe
cap = cv2.VideoCapture(0)

def countdown():
    font = pygame.font.Font(None, 74)
    for i in range(3, 0, -1):
        screen.fill(BACKGROUND_COLOR)
        countdown_text = font.render(str(i), True, TIMER_COLOR)
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(1000)

def main_menu():
    font = pygame.font.Font(None, 74)
    while True:
        screen.fill(BACKGROUND_COLOR)
        title_text = font.render("Pong Game", True, TIMER_COLOR)
        start_text = font.render("Press ENTER to Start", True, TIMER_COLOR)
        settings_text = font.render("Press S for Settings", True, TIMER_COLOR)

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        screen.blit(settings_text, (WIDTH // 2 - settings_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # Start the game
                if event.key == pygame.K_s:
                    ball_speed = settings_menu()  # Get the ball speed from settings
                    continue  # Return to the main menu after settings

def settings_menu():
    ball_speed = 5  # Default ball speed
    font = pygame.font.Font(None, 74)
    while True:
        screen.fill(BACKGROUND_COLOR)
        settings_text = font.render("Settings", True, TIMER_COLOR)
        speed_text = font.render(f"Ball Speed: {ball_speed}", True, TIMER_COLOR)
        back_text = font.render("Press B to go Back", True, TIMER_COLOR)

        screen.blit(settings_text, (WIDTH // 2 - settings_text.get_width() // 2, HEIGHT // 4))
        screen.blit(speed_text, (WIDTH // 2 - speed_text.get_width() // 2, HEIGHT // 2))
        screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return ball_speed  # Return the current ball speed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    return ball_speed  # Go back to main menu and return ball speed
                if event.key == pygame.K_UP:
                    ball_speed += 1  # Increase ball speed
                if event.key == pygame.K_DOWN:
                    ball_speed = max(1, ball_speed - 1)  # Decrease ball speed, minimum 1

# Main Game Loop
def game_loop(ball_speed):
    if ball_speed is None:  # Ensure ball_speed is not None
        ball_speed = 5  # Default value if somehow it is None
    # Inisialisasi Game dan Paddles
    game = Game(WIDTH, HEIGHT, BALL_COLOR, PADDLE_COLOR, BACKGROUND_COLOR, ball_speed)
    left_paddle = Paddle(10, game.HEIGHT // 2 - 50, 20, 100, PADDLE_COLOR)
    right_paddle = Paddle(game.WIDTH - 30, game.HEIGHT // 2 - 50, 20, 100, PADDLE_COLOR)

    countdown()

    # Timer Game
    game_start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                index_finger_tip_y = hand_landmarks.landmark[8].y * HEIGHT

                if hand_landmarks.landmark[8].x < 0.5:
                    left_paddle.y = int(index_finger_tip_y - left_paddle.height // 2)
                else:
                    right_paddle.y = int(index_finger_tip_y - right_paddle.height // 2)

        game.update_ball()

        game.check_ball_paddle_collision(left_paddle, right_paddle)
        game.check_ball_out_of_bounds()

        winner = game.check_for_winner()
        if winner:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            font = pygame.font.Font(None, 74)
            winner_text = font.render(f"{winner} Wins!", True, WINNER_COLOR)
            overlay.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2))
            frame_surface = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")
            screen.blit(frame_surface, (0, 0))
            screen.blit(overlay, (0, 0))
            pygame.display.flip()
            pygame.time.wait(3000)
            break

        left_paddle.y = max(0, min(game.HEIGHT - left_paddle.height, left_paddle.y))
        right_paddle.y = max(0, min(game.HEIGHT - right_paddle.height, right_paddle.y))

        elapsed_time = time.time() - game_start_time

        game.draw_game(frame, left_paddle, right_paddle, elapsed_time)

        pygame.time.Clock().tick(FPS)


# Start the game
while True:
    ball_speed = main_menu()  # Get the ball speed from the settings menu
    game_loop(ball_speed)  # Start the game loop

# Lepaskan resource
cap.release()
pygame.quit()
cv2.destroyAllWindows()
