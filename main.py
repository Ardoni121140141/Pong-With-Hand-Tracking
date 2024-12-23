import cv2
import mediapipe as mp
import pygame
import time
import sys
from paddle import Paddle
from game import Game

# Inisialisasi Pygame
pygame.init()

# Konstanta Game
WIDTH, HEIGHT = 1000, 800
FPS = 120

# Warna menggunakan format RGB
BALL_COLOR = (0, 0, 255)  # Merah
PADDLE_COLOR = (0, 255, 0)  # Hijau
SCORE_COLOR = (255, 255, 0)  # Kuning
WINNER_COLOR = (255, 0, 0)  # Merah
TIMER_COLOR = (255, 255, 255)  # Putih
BACKGROUND_COLOR = (0, 0, 0)  # Latar belakang hitam

# Initialize ball speed
ball_speed = 5  # Default ball speed

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

def main_menu(ball_speed):
    font = pygame.font.Font(None, 74)
    while True:
        screen.fill(BACKGROUND_COLOR)
        title_text = font.render("Pong Game", True, TIMER_COLOR)
        start_text = font.render("Press ENTER to Start", True, TIMER_COLOR)
        settings_text = font.render("Press S for Settings", True, TIMER_COLOR)
        quit_text = font.render("Press ESC to Quit", True, TIMER_COLOR)

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        screen.blit(settings_text, (WIDTH // 2 - settings_text.get_width() // 2, HEIGHT // 2 + 50))
        screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Exit the program
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return ball_speed  # Start the game
                if event.key == pygame.K_s:
                    ball_speed = settings_menu(ball_speed)  # Pass ball_speed to settings_menu
                if event.key == pygame.K_ESCAPE:  # Quit the game
                    pygame.quit()
                    sys.exit()  # Exit the program

def settings_menu(ball_speed):
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
                return ball_speed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    return ball_speed  # Go back to main menu and return ball speed
                if event.key == pygame.K_UP:
                    ball_speed += 1  # Increase ball speed
                    print(f"Ball speed increased to: {ball_speed}")  # Debugging statement
                if event.key == pygame.K_DOWN:
                    ball_speed = max(1, ball_speed - 1)  # Decrease ball speed, minimum 1
                    print(f"Ball speed decreased to: {ball_speed}")  # Debugging statement

def game_loop(ball_speed):
    if ball_speed is None:  # Ensure ball_speed is not None
        ball_speed = 5  # Default value if somehow it is None

    print(f"Starting game loop with ball speed: {ball_speed}")  # Debugging statement

    # Inisialisasi Game dan Paddles
    game = Game(WIDTH, HEIGHT, BALL_COLOR, PADDLE_COLOR, BACKGROUND_COLOR, ball_speed)
    left_paddle = Paddle(10, game.HEIGHT // 2 - 50, 20, 100, PADDLE_COLOR)
    right_paddle = Paddle(game.WIDTH - 30, game.HEIGHT // 2 - 50, 20, 100, PADDLE_COLOR)

    countdown_done = False  # Flag to indicate if countdown is done

    # Timer Game
    game_start_time = time.time()
    paused = False  # Variable to track if the game is paused
    pause_start_time = 0  # Variable to track when the game was paused

    while True:
        # Inside your event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Detect if the user clicks the close window
                cap.release()
                pygame.quit()
                cv2.destroyAllWindows()
                sys.exit()  # Exit the program
            elif event.type == pygame.KEYDOWN:  # Detect if a keyboard key is pressed
                if event.key == pygame.K_ESCAPE:  # Pause the game if ESC is pressed
                    if paused:
                        paused = False  # Resume the game
                        game_start_time += time.time() - pause_start_time  # Adjust start time
                    else:
                        paused = True  # Pause the game
                        pause_start_time = time.time()  # Record the time when paused

        if not countdown_done:
            countdown()
            countdown_done = True

        if paused:
            # If the game is paused, show the pause screen
            if pause_screen():  # If user chooses to go to main menu
                return  # Return to main menu
            else:
                paused = False  # Resume the game
                print("Game resumed")  # Debugging statement
            continue  # Skip the rest of the loop

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

        if not paused:  # Only calculate elapsed time if not paused
            elapsed_time = time.time() - game_start_time  # Calculate elapsed time
        else:
            elapsed_time = 0  # Set elapsed time to 0 when paused

        game.draw_game(frame, left_paddle, right_paddle, elapsed_time)

        pygame.time.Clock().tick(FPS)

def pause_screen():
    font = pygame.font.Font(None, 74)
    while True:
        screen.fill(BACKGROUND_COLOR)
        pause_text = font.render("Paused", True, TIMER_COLOR)
        mainmenu_confirm_text = font.render("Press ESC to go to Main Menu", True, TIMER_COLOR)
        continue_confirm_text = font.render("ENTER to Continue", True, TIMER_COLOR)

        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 4))
        screen.blit(mainmenu_confirm_text, (WIDTH // 2 - mainmenu_confirm_text.get_width() // 2, HEIGHT // 2))
        screen.blit(continue_confirm_text, (WIDTH // 2 - continue_confirm_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                cv2.destroyAllWindows()
                sys.exit()  # Exit the program
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Go to main menu
                    return True  # Indicate to go to main menu
                if event.key == pygame.K_RETURN:  # Resume game
                    return False  # Continue the game

# Start the game
while True:
    ball_speed = main_menu(ball_speed)  # Pass the current ball speed
    game_loop(ball_speed)  # Start the game loop

# Lepaskan resource
cap.release()
pygame.quit()
cv2.destroyAllWindows()
