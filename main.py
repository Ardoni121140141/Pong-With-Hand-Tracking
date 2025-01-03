import cv2
import mediapipe as mp
import pygame
import time
import sys
from paddle import Paddle
from game import Game

# Inisialisasi Pygame
pygame.init()

# Konstanta permainan
WIDTH, HEIGHT = 1000, 800  # Ukuran layar
FPS = 120  # Frame per detik

# Warna menggunakan format RGB
BALL_COLOR = (0, 0, 255)  # Warna bola (merah)
PADDLE_COLOR = (0, 255, 0)  # Warna paddle (hijau)
SCORE_COLOR = (255, 255, 0)  # Warna skor (kuning)
WINNER_COLOR = (255, 0, 0)  # Warna teks pemenang (merah)
TIMER_COLOR = (255, 255, 255)  # Warna teks (putih)
BACKGROUND_COLOR = (0, 0, 0)  # Latar belakang (hitam)

# Kecepatan bola default
DEFAULT_BALL_SPEED = 5

# Inisialisasi layar permainan
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong with Hand Tracking")

# Inisialisasi MediaPipe untuk deteksi tangan
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Menggunakan kamera sebagai input
cap = cv2.VideoCapture(0)


def display_text_centered(screen, text, font, color, y_offset=0):
    """
    Menampilkan teks di tengah layar dengan font dan warna tertentu.
    """
    text_surface = font.render(text, True, color)
    screen.blit(
        text_surface,
        (
            WIDTH // 2 - text_surface.get_width() // 2,
            HEIGHT // 2 - text_surface.get_height() // 2 + y_offset,
        ),
    )


def countdown():
    """
    Menghitung mundur sebelum permainan dimulai (3, 2, 1).
    """
    font = pygame.font.Font(None, 74)
    for i in range(3, 0, -1):
        screen.fill(BACKGROUND_COLOR)  # Membersihkan layar
        display_text_centered(screen, str(i), font, TIMER_COLOR)  # Tampilkan angka
        pygame.display.flip()
        pygame.time.wait(1000)  # Tunggu selama 1 detik


def main_menu(ball_speed):
    """
    Menampilkan menu utama permainan

    Args:
        ball_speed: Kecepatan bola saat ini
    
    Return: 
        Kecepatan bola yang dipilih
    """
    font = pygame.font.Font(None, 74)

    while True:
        # Tampilkan menu utama
        screen.fill(BACKGROUND_COLOR)
        display_text_centered(screen, "Pong Game", font, TIMER_COLOR, y_offset=-100)
        display_text_centered(screen, "Press ENTER to Start", font, TIMER_COLOR, y_offset=-50)
        display_text_centered(screen, "Press S for Settings", font, TIMER_COLOR)
        display_text_centered(screen, "Press ESC to Quit", font, TIMER_COLOR, y_offset=50)
        pygame.display.flip()

        # Periksa input dari pemain
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Jika pengguna menutup jendela
                clean_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Memulai permainan
                    return ball_speed
                if event.key == pygame.K_s:  # Masuk ke menu pengaturan
                    ball_speed = settings_menu(ball_speed)
                if event.key == pygame.K_ESCAPE:  # Keluar dari permainan
                    clean_exit()


def settings_menu(ball_speed):
    """
    Menampilkan menu pengaturan untuk mengubah kecepatan bola

    Args:
        ball_speed: Kecepatan bola saat ini
    
    Return: 
        Kecepatan bola yang diperbarui
    """
    font = pygame.font.Font(None, 74)

    while True:
        # Tampilkan menu pengaturan
        screen.fill(BACKGROUND_COLOR)
        display_text_centered(screen, "Settings", font, TIMER_COLOR, y_offset=-100)
        display_text_centered(screen, f"Ball Speed: {ball_speed}", font, TIMER_COLOR, y_offset=-50)
        display_text_centered(screen, "Press UP/DOWN to Adjust", font, TIMER_COLOR)
        display_text_centered(screen, "Press B to Go Back", font, TIMER_COLOR, y_offset=50)
        pygame.display.flip()

        # Periksa input dari pemain
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Jika jendela ditutup
                clean_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:  # Kembali ke menu utama
                    return ball_speed
                if event.key == pygame.K_UP:  # Meningkatkan kecepatan bola
                    ball_speed += 1
                if event.key == pygame.K_DOWN:  # Mengurangi kecepatan bola
                    ball_speed = max(1, ball_speed - 1)  # Tidak kurang dari 1


def game_loop(ball_speed):
    """
    Logika utama permainan.
    
    Args:
        ball_speed: Kecepatan bola yang dipilih
    """
    # Inisialisasi game dan paddle
    game = Game(WIDTH, HEIGHT, BALL_COLOR, PADDLE_COLOR, BACKGROUND_COLOR, ball_speed)
    left_paddle = Paddle(10, HEIGHT // 2 - 50, 20, 100, PADDLE_COLOR)
    right_paddle = Paddle(WIDTH - 30, HEIGHT // 2 - 50, 20, 100, PADDLE_COLOR)

    # Countdown hanya dilakukan sekali di awal
    countdown()

    paused = False  # Status jeda
    start_time = time.time()  # Waktu awal permainan

    while True:
        # Periksa event dari pemain
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Jika pengguna menutup jendela
                clean_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Pause jika ESC ditekan
                    paused = not paused  # Toggle status jeda

        if paused:
            # Jika permainan dijeda, tampilkan layar pause
            if pause_screen():  # Jika pemain memilih kembali ke menu utama
                return  # Kembali ke menu utama
            else:
                paused = False  # Lanjutkan permainan
            continue  # Lewati loop utama jika dijeda

        ret, frame = cap.read()  # Membaca frame dari kamera
        if not ret:
            break  # Jika kamera gagal membaca, keluar dari loop

        # Proses frame video
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame)

        # Kontrol paddle berdasarkan posisi tangan
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                control_paddles(left_paddle, right_paddle, hand_landmarks)

        # Perbarui bola dan periksa kondisi permainan
        game.update_ball()
        game.check_ball_paddle_collision(left_paddle, right_paddle)
        game.check_ball_out_of_bounds()

        winner = game.check_for_winner()
        if winner:
            display_winner(winner)
            break  # Jika ada pemenang, keluar dari loop permainan

        game.draw_game(frame, left_paddle, right_paddle, time.time() - start_time)
        pygame.time.Clock().tick(FPS)  # Kontrol kecepatan frame


def pause_screen():
    """
    Menampilkan layar pause.
    """
    font = pygame.font.Font(None, 74)
    while True:
        screen.fill(BACKGROUND_COLOR)
        display_text_centered(screen, "Paused", font, TIMER_COLOR, y_offset=-50)
        display_text_centered(screen, "Press ENTER to Resume", font, TIMER_COLOR)
        display_text_centered(screen, "Press ESC to Quit", font, TIMER_COLOR, y_offset=50)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                clean_exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Kembali ke permainan
                    return False
                if event.key == pygame.K_ESCAPE:  # Keluar dari permainan
                    return True


def control_paddles(left_paddle, right_paddle, hand_landmarks):
    """
    Mengontrol paddle berdasarkan posisi tangan.
    """
    index_finger_tip_y = hand_landmarks.landmark[8].y * HEIGHT
    if hand_landmarks.landmark[8].x < 0.5:
        left_paddle.y = int(index_finger_tip_y - left_paddle.height // 2)
    else:
        right_paddle.y = int(index_finger_tip_y - right_paddle.height // 2)


def display_winner(winner):
    """
    Menampilkan pemenang permainan.
    """
    font = pygame.font.Font(None, 74)
    screen.fill(BACKGROUND_COLOR)
    display_text_centered(screen, f"{winner} Wins!", font, WINNER_COLOR)
    pygame.display.flip()
    pygame.time.wait(3000)  # Tampilkan teks selama 3 detik


def clean_exit():
    """
    Membersihkan resource dan keluar dari program.
    """
    cap.release()
    pygame.quit()
    cv2.destroyAllWindows()
    sys.exit()


# Program utama
if __name__ == "__main__":
    while True:
        ball_speed = main_menu(DEFAULT_BALL_SPEED)
        game_loop(ball_speed)