# ui/botao.py — versão universal compatível com Arcade antigo
import arcade
from typing import Tuple


class Botao:
    def __init__(self, label: str, cx: int, cy: int, width: int, height: int, acao: str = ""):
        self.label = label
        self.cx = cx
        self.cy = cy
        self.width = width
        self.height = height
        self.acao = acao
        self.hover = False

    def contains(self, x: int, y: int) -> bool:
        left = self.cx - self.width / 2
        right = self.cx + self.width / 2
        bottom = self.cy - self.height / 2
        top = self.cy + self.height / 2
        return left <= x <= right and bottom <= y <= top

    def update_hover(self, mouse_pos: Tuple[int, int]):
        self.hover = self.contains(*mouse_pos)

    def draw_rect(self, left, right, top, bottom, color):
        """Desenha um retângulo usando linhas (compatível com Arcade 3.3.3)."""
        step = 4
        for y in range(int(bottom), int(top), step):
            arcade.draw_line(int(left), y, int(right), y, color, step)

    def draw_outline(self, left, right, top, bottom, color):
        """Desenha o contorno usando draw_line."""
        # Topo
        arcade.draw_line(left, top, right, top, color, 2)
        # Base
        arcade.draw_line(left, bottom, right, bottom, color, 2)
        # Esquerda
        arcade.draw_line(left, bottom, left, top, color, 2)
        # Direita
        arcade.draw_line(right, bottom, right, top, color, 2)

    def draw(self, mouse_pos: Tuple[int, int], font_name: str = "Arial"):
        left = self.cx - self.width / 2
        right = self.cx + self.width / 2
        top = self.cy + self.height / 2
        bottom = self.cy - self.height / 2

        bg_normal = (60, 60, 70)
        bg_hover = (110, 110, 140)
        bg = bg_hover if self.hover else bg_normal

        # Retângulo preenchido com linhas
        self.draw_rect(left, right, top, bottom, bg)

        # Contorno
        self.draw_outline(left, right, top, bottom, arcade.color.WHITE)

        # Texto centralizado
        text = arcade.Text(
            self.label,
            self.cx,
            self.cy,
            arcade.color.WHITE,
            22,
            anchor_x="center",
            anchor_y="center",
            font_name=font_name
        )
        text.draw()
