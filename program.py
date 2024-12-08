import cv2
import mediapipe as mp
import pygame
import time

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
FPS = 60
WINNING_SCORE = 5

# Colors
BALL_COLOR = (0, 0, 255)  # Red
PADDLE_COLOR = (0, 255, 0)  # Green
SCORE_COLOR = (255, 255, 0)  # Yellow
WINNER_COLOR = (255, 0, 0)  # Bright Red
TIMER_COLOR = (255, 255, 255)  # White

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong with Hand Tracking")

# Ball position and velocity
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx, ball_dy = 5, 5

# Paddle positions
left_paddle_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
right_paddle_y = HEIGHT // 2 - PADDLE_HEIGHT // 2

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Video Capture for MediaPipe
cap = cv2.VideoCapture(0)

# Scores
left_score = 0
right_score = 0

# Timer
game_start_time = None  # To store the start time of the game


def draw_game(frame, ball_x, ball_y, left_paddle_y, right_paddle_y, left_score, right_score, elapsed_time=None):
    """Draw all game elements on the webcam frame."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # Transparent overlay for game elements

    # Ball
    pygame.draw.circle(overlay, BALL_COLOR, (ball_x, ball_y), BALL_RADIUS)

    # Paddles
    pygame.draw.rect(overlay, PADDLE_COLOR, (10, left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(overlay, PADDLE_COLOR, (WIDTH - 10 - PADDLE_WIDTH, right_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))

    # Scores
    font = pygame.font.Font(None, 74)
    left_text = font.render(str(left_score), True, SCORE_COLOR)
    right_text = font.render(str(right_score), True, SCORE_COLOR)
    overlay.blit(left_text, (WIDTH // 4, 20))
    overlay.blit(right_text, (3 * WIDTH // 4, 20))

    # Timer
    if elapsed_time is not None:
        small_font = pygame.font.Font(None, 36)  # Smaller font for timer
        timer_text = small_font.render(f"{elapsed_time:.1f}", True, TIMER_COLOR)
        overlay.blit(timer_text, (WIDTH - 80, 10))  # Timer at the top-right corner

    # Convert frame to Pygame surface
    frame_surface = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")

    # Blit frame and overlay to the screen
    screen.blit(frame_surface, (0, 0))
    screen.blit(overlay, (0, 0))

    pygame.display.flip()


def countdown():
    """Display a countdown on the screen before the game starts."""
    font = pygame.font.Font(None, 74)
    for i in range(3, 0, -1):
        screen.fill((0, 0, 0))  # Clear the screen
        countdown_text = font.render(str(i), True, TIMER_COLOR)
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(1000)  # Wait for 1 second


# Countdown before the game starts
countdown()

# Start the timer
game_start_time = time.time()

while True:
    # Capture frame from webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame to match the game window
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    frame = cv2.flip(frame, 1)  # Flip frame for mirror effect

    # Convert the BGR image to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame with MediaPipe
    results = hands.process(frame)

    # Draw hand landmarks on the frame
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the Y-coordinate of the index finger tip (landmark 8)
            index_finger_tip_y = hand_landmarks.landmark[8].y * HEIGHT

            # Control left paddle with left hand
            if hand_landmarks.landmark[8].x < 0.5:  # Left hand
                left_paddle_y = int(index_finger_tip_y - PADDLE_HEIGHT // 2)

            # Control right paddle with right hand
            else:  # Right hand
                right_paddle_y = int(index_finger_tip_y - PADDLE_HEIGHT // 2)

    # Ball movement
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball collision with top and bottom walls
    if ball_y - BALL_RADIUS <= 0 or ball_y + BALL_RADIUS >= HEIGHT:
        ball_dy *= -1

    # Ball collision with paddles
    if (ball_x - BALL_RADIUS <= 10 + PADDLE_WIDTH and
        left_paddle_y <= ball_y <= left_paddle_y + PADDLE_HEIGHT):
        ball_dx *= -1
    if (ball_x + BALL_RADIUS >= WIDTH - 10 - PADDLE_WIDTH and
        right_paddle_y <= ball_y <= right_paddle_y + PADDLE_HEIGHT):
        ball_dx *= -1

    # Ball out of bounds
    if ball_x < 0:
        right_score += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_dx *= -1
    if ball_x > WIDTH:
        left_score += 1
        ball_x, ball_y = WIDTH // 2, HEIGHT // 2
        ball_dx *= -1

    # Check if someone has won
    if left_score == WINNING_SCORE or right_score == WINNING_SCORE:
        winner = "Left Player" if left_score == WINNING_SCORE else "Right Player"
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        font = pygame.font.Font(None, 74)
        winner_text = font.render(f"{winner} Wins!", True, WINNER_COLOR)
        overlay.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2))
        frame_surface = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")
        screen.blit(frame_surface, (0, 0))
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        pygame.time.wait(3000)  # Pause for 3 seconds
        break  # Exit the game loop

    # Keep paddles on screen
    left_paddle_y = max(0, min(HEIGHT - PADDLE_HEIGHT, left_paddle_y))
    right_paddle_y = max(0, min(HEIGHT - PADDLE_HEIGHT, right_paddle_y))

    # Calculate elapsed time
    elapsed_time = time.time() - game_start_time

    # Draw everything
    draw_game(frame, ball_x, ball_y, left_paddle_y, right_paddle_y, left_score, right_score, elapsed_time)

    # Control frame rate
    clock.tick(FPS)

# Release resources
cap.release()
pygame.quit()
cv2.destroyAllWindows()