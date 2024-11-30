class Paddle:
    """
    Representasi paddle dalam permainan Pong.

    Atribut:
        x (int): Posisi horizontal paddle.
        y (int): Posisi vertikal paddle.
        width (int): Lebar paddle.
        height (int): Tinggi paddle.
        color (tuple): Warna paddle.
    """

    def __init__(self, x, y, width, height, color):
        """
        Inisialisasi objek Paddle.

        Args:
            x (int): Posisi horizontal paddle.
            y (int): Posisi vertikal paddle.
            width (int): Lebar paddle.
            height (int): Tinggi paddle.
            color (tuple): Warna paddle.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
