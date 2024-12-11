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

# Inisialisasi Game dan Paddles
game = Game(WIDTH, HEIGHT, BALL_COLOR, PADDLE_COLOR, BACKGROUND_COLOR)
left_paddle = Paddle(10, game.HEIGHT // 2 - 50, 20, 100, PADDLE_COLOR)
right_paddle = Paddle(game.WIDTH - 30, game.HEIGHT // 2 - 50, 20, 100, PADDLE_COLOR)

# Video Capture untuk MediaPipe
cap = cv2.VideoCapture(0)

def countdown():
    """
    Menghitung mundur sebelum permainan dimulai.
    Menampilkan angka 3, 2, 1 di layar untuk persiapan permainan.
    """
    font = pygame.font.Font(None, 74)
    for i in range(3, 0, -1):
        screen.fill(BACKGROUND_COLOR)  # Membersihkan layar
        countdown_text = font.render(str(i), True, TIMER_COLOR)
        screen.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(1000)  # Menunggu selama 1 detik

# Countdown sebelum permainan dimulai
countdown()

# Timer Game
game_start_time = time.time()

# Main Game Loop
while True:
    # Capture frame dari webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame untuk menyesuaikan dengan ukuran game
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    frame = cv2.flip(frame, 1)  # Membalikkan frame untuk efek mirror

    # Mengubah gambar BGR ke RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Proses frame dengan MediaPipe
    results = hands.process(frame)

    # Mengontrol pergerakan paddle menggunakan tangan
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Mendapatkan koordinat Y dari ujung jari telunjuk (landmark 8)
            index_finger_tip_y = hand_landmarks.landmark[8].y * HEIGHT

            # Mengontrol paddle kiri dengan tangan kiri
            if hand_landmarks.landmark[8].x < 0.5:  # Tangan kiri
                left_paddle.y = int(index_finger_tip_y - left_paddle.height // 2)

            # Mengontrol paddle kanan dengan tangan kanan
            else:  # Tangan kanan
                right_paddle.y = int(index_finger_tip_y - right_paddle.height // 2)

    # Pergerakan bola
    game.update_ball()

    # Periksa tabrakan bola dengan paddle
    game.check_ball_paddle_collision(left_paddle, right_paddle)

    # Periksa bola keluar batas
    game.check_ball_out_of_bounds()

    # Periksa pemenang
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
        pygame.time.wait(3000)  # Pause selama 3 detik
        break  # Keluar dari loop permainan

    # Pastikan paddle tetap berada di layar
    left_paddle.y = max(0, min(game.HEIGHT - left_paddle.height, left_paddle.y))
    right_paddle.y = max(0, min(game.HEIGHT - right_paddle.height, right_paddle.y))

    # Hitung waktu yang telah berlalu
    elapsed_time = time.time() - game_start_time

    # Gambar semua elemen
    game.draw_game(frame, left_paddle, right_paddle, elapsed_time)

    # Atur frame rate
    pygame.time.Clock().tick(FPS)

# Lepaskan resource
cap.release()
pygame.quit()
cv2.destroyAllWindows()