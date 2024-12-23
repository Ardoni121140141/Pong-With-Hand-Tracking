import pygame

class Game:
    """
    Representasi permainan Pong.

    Atribut:
        WIDTH (int): Lebar layar permainan.
        HEIGHT (int): Tinggi layar permainan.
        BALL_COLOR (tuple): Warna bola.
        PADDLE_COLOR (tuple): Warna paddle.
        BACKGROUND_COLOR (tuple): Warna latar belakang.
        ball_x (int): Posisi horizontal bola.
        ball_y (int): Posisi vertikal bola.
        ball_dx (int): Kecepatan bola di sumbu X.
        ball_dy (int): Kecepatan bola di sumbu Y.
        left_score (int): Skor pemain kiri.
        right_score (int): Skor pemain kanan.
        game_start_time (float): Waktu mulai permainan.

    Metode:
        draw_game: Menampilkan elemen permainan pada layar.
        update_ball: Memperbarui posisi bola.
        check_ball_paddle_collision: Mengecek apakah bola bertabrakan dengan paddle.
        check_ball_out_of_bounds: Mengecek apakah bola keluar batas dan memperbarui skor.
        reset_ball: Mengatur ulang posisi bola.
        check_for_winner: Mengecek jika ada pemenang.
    """

    def __init__(self, width, height, ball_color, paddle_color, background_color, ball_speed=5):
        """Inisialisasi atribut permainan.

        Args:
            width (int): Lebar layar permainan.
            height (int): Tinggi layar permainan.
            ball_color (tuple): Warna bola.
            paddle_color (tuple): Warna paddle.
            background_color (tuple): Warna latar belakang.
            ball_speed (int): Kecepatan bola.
        """
        self.WIDTH = width
        self.HEIGHT = height
        self.BALL_COLOR = ball_color
        self.PADDLE_COLOR = paddle_color
        self.BACKGROUND_COLOR = background_color
        
        # Inisialisasi posisi bola dan kecepatan
        self.ball_x = self.WIDTH // 2
        self.ball_y = self.HEIGHT // 2
        self.ball_dx = ball_speed
        self.ball_dy = ball_speed

        # Inisialisasi skor
        self.left_score = 0
        self.right_score = 0

        # Timer untuk game
        self.game_start_time = None

    def draw_game(self, frame, left_paddle, right_paddle, elapsed_time=None):
        """
        Menampilkan semua elemen permainan pada frame webcam.

        Args:
            frame (ndarray): Gambar frame webcam.
            left_paddle (Paddle): Objek paddle kiri.
            right_paddle (Paddle): Objek paddle kanan.
            elapsed_time (float, optional): Waktu yang telah berlalu sejak permainan dimulai.
        """
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)

        # Menggambar bola
        pygame.draw.circle(overlay, self.BALL_COLOR, (self.ball_x, self.ball_y), 10)

        # Menggambar paddles
        pygame.draw.rect(overlay, self.PADDLE_COLOR, (left_paddle.x, left_paddle.y, left_paddle.width, left_paddle.height))
        pygame.draw.rect(overlay, self.PADDLE_COLOR, (right_paddle.x, right_paddle.y, right_paddle.width, right_paddle.height))

        # Menggambar skor
        font = pygame.font.Font(None, 74)
        left_text = font.render(str(self.left_score), True, (255, 255, 0))  # Warna kuning
        right_text = font.render(str(self.right_score), True, (255, 255, 0))  # Warna kuning
        overlay.blit(left_text, (self.WIDTH // 4, 20))
        overlay.blit(right_text, (3 * self.WIDTH // 4, 20))

        # Menggambar timer
        if elapsed_time is not None:
            small_font = pygame.font.Font(None, 36)  # Font lebih kecil untuk timer
            timer_text = small_font.render(f"{elapsed_time:.1f}", True, (255, 255, 255))  # Warna putih
            overlay.blit(timer_text, (self.WIDTH - 80, 10))

        # Mengubah frame menjadi surface Pygame
        frame_surface = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")

        # Menampilkan frame dan overlay di layar
        pygame.display.get_surface().blit(frame_surface, (0, 0))
        pygame.display.get_surface().blit(overlay, (0, 0))

        pygame.display.flip()

    def update_ball(self):
        """
        Memperbarui posisi bola berdasarkan kecepatan dan mendeteksi tabrakan dengan dinding.

        Mengubah posisi bola dan mengubah arah bola jika mengenai dinding atas/bawah.
        """
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        # Bola bertabrakan dengan dinding atas dan bawah
        if self.ball_y - 10 <= 0 or self.ball_y + 10 >= self.HEIGHT:
            self.ball_dy *= -1

    def check_ball_paddle_collision(self, left_paddle, right_paddle):
        """
        Mengecek apakah bola bertabrakan dengan paddle.

        Args:
            left_paddle (Paddle): Paddle kiri.
            right_paddle (Paddle): Paddle kanan.
        """
        if (self.ball_x - 10 <= left_paddle.x + left_paddle.width and
            left_paddle.y <= self.ball_y <= left_paddle.y + left_paddle.height):
            self.ball_dx *= -1
        if (self.ball_x + 10 >= right_paddle.x and
            right_paddle.y <= self.ball_y <= right_paddle.y + right_paddle.height):
            self.ball_dx *= -1

    def check_ball_out_of_bounds(self):
        """
        Mengecek apakah bola keluar dari batas permainan dan memperbarui skor.

        Menambahkan skor ke pemain yang berhasil memanfaatkan bola keluar dari batas.
        """
        if self.ball_x < 0:
            self.right_score += 1
            self.reset_ball()
        if self.ball_x > self.WIDTH:
            self.left_score += 1
            self.reset_ball()

    def reset_ball(self):
        """
        Mengatur ulang posisi bola ke tengah dan mengubah arah bola.

        Digunakan setelah bola keluar dari batas permainan.
        """
        self.ball_x = self.WIDTH // 2
        self.ball_y = self.HEIGHT // 2
        self.ball_dx *= -1  # Invert direction
        self.ball_dy *= -1  # Invert direction

    def check_for_winner(self):
        """
        Mengecek apakah ada pemain yang memenangkan permainan.

        Returns:
            str: Nama pemain yang menang ("Left Player" atau "Right Player") jika ada pemenang.
            None: Jika belum ada pemenang.
        """
        if self.left_score == 5:
            return "Left Player"
        elif self.right_score == 5:
            return "Right Player"
        return None
