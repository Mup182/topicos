# ui/botao.py
from typing import Tuple, Optional
import arcade
from core.settings import COR_BOTAO, COR_HOVER, COR_TEXTO, COR_SOMBRA
from core.utils import fit_font_size_measure

class Botao:
    """Botão simples para menus. Mantém centro, tamanho base e efeito hover."""
    def __init__(self, texto: str, center_x: int, center_y: int, largura: int, altura: int, acao: Optional[str] = None):
        self.texto = texto
        self.center_x = center_x
        self.center_y = center_y
        self.base_largura = largura
        self.base_altura = altura
        self.acao = acao
        self.hover = False
        self.hover_scale = 1.0

    def update_hover(self, mouse_pos: Tuple[int, int]) -> None:
        mx, my = mouse_pos
        half_w = (self.base_largura * self.hover_scale) / 2
        half_h = (self.base_altura * self.hover_scale) / 2
        left = self.center_x - half_w
        right = self.center_x + half_w
        bottom = self.center_y - half_h
        top = self.center_y + half_h
        hovering = (left <= mx <= right) and (bottom <= my <= top)
        self.hover = hovering
        target = 1.06 if hovering else 1.0
        # suaviza a transição
        self.hover_scale += (target - self.hover_scale) * 0.25

    def draw(self, mouse_pos: Tuple[int, int], font_name: str) -> None:
        """Desenha o botão. Observação: usa draw_text (padrão arcade)."""
        self.update_hover(mouse_pos)
        scale = self.hover_scale
        largura = int(self.base_largura * scale)
        altura = int(self.base_altura * scale)
        half_w = largura / 2
        half_h = altura / 2
        left = self.center_x - half_w
        right = self.center_x + half_w
        bottom = self.center_y - half_h
        top = self.center_y + half_h

        cor = COR_HOVER if self.hover else COR_BOTAO

        # A versão do arcade que você usa exige draw_lrbt_rectangle_filled(left, right, bottom, top, color)
        arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, cor)

        # Ajusta tamanho da fonte para caber no botão
        font_size = fit_font_size_measure(self.texto, largura, font_name, start_size=36, min_size=12)

        # Sombra e texto
        arcade.draw_text(self.texto,
                         self.center_x + 2, self.center_y - font_size * 0.05,
                         COR_SOMBRA, font_size=font_size,
                         anchor_x="center", anchor_y="center", font_name=font_name)
        arcade.draw_text(self.texto,
                         self.center_x, self.center_y - font_size * 0.05,
                         COR_TEXTO, font_size=font_size,
                         anchor_x="center", anchor_y="center", font_name=font_name)

    def contains(self, x: int, y: int) -> bool:
        largura = int(self.base_largura * self.hover_scale)
        altura = int(self.base_altura * self.hover_scale)
        half_w = largura / 2
        half_h = altura / 2
        return (self.center_x - half_w <= x <= self.center_x + half_w) and \
               (self.center_y - half_h <= y <= self.center_y + half_h)
