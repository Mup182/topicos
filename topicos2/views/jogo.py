# views/jogo.py
import os
import arcade
from typing import Optional
from core.settings import LARGURA, ALTURA, DEFAULT_BG_PATH, COR_FUNDO_JOGO
from core.utils import safe_load_texture
from views.dialogos import TelaDialogos

class TelaJogo(arcade.View):
    def __init__(self, largura: int = LARGURA, altura: int = ALTURA, font_name: str = None, bg_path: str = DEFAULT_BG_PATH):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.font_name = font_name or "Arial"
        self.bg_path = bg_path
        self.bg_texture = safe_load_texture(self.bg_path)
        self.fade_in = 255

        # Inicializa objetos de texto aqui para evitar AttributeError
        texto = ("Capítulo 1 - Brasília, 1964\n\n"
                 "O filhote acordou e saiu em busca de comida. (substitua por seu texto completo se quiser.)")
        self.chapter_text = arcade.Text(
            texto,
            self.largura // 2, self.altura // 2,
            color=(255, 230, 200),
            font_size=28,
            anchor_x="center",
            anchor_y="center",
            width=max(100, self.largura - 120),
            align="center",
            font_name=self.font_name
        )

        self.instr_text = arcade.Text(
            "Clique ou pressione [Enter] para continuar.",
            20, 20,
            color=arcade.color.LIGHT_GRAY,
            font_size=14,
            anchor_x="left",
            anchor_y="bottom",
            font_name=self.font_name
        )

    def on_show(self) -> None:
        # configura cor de fundo (seguindo settings)
        arcade.set_background_color(COR_FUNDO_JOGO)
        # (opcional) recarregar bg_texture caso o caminho tenha mudado
        self.bg_texture = safe_load_texture(self.bg_path)

    def on_draw(self) -> None:
        # Sempre usar self.clear() dentro de Views
        self.clear()

        if self.bg_texture:
            arcade.draw_lrwh_rectangle_textured(0, 0, self.largura, self.altura, self.bg_texture)
        else:
            # ordem: left, right, bottom, top (lrbt)
            arcade.draw_lrbt_rectangle_filled(0, self.largura, 0, self.altura, COR_FUNDO_JOGO)

        # atualiza posição e largura caso a janela tenha sido redimensionada
        self.chapter_text.position = (self.largura // 2, self.altura // 2)
        self.chapter_text.width = max(100, self.largura - 120)
        self.chapter_text.draw()

        # Fade-in overlay: desenha um retângulo com alpha decrescente
        if self.fade_in > 0:
            # draw_lrbt_rectangle_filled(left, right, bottom, top, color)
            arcade.draw_lrbt_rectangle_filled(0, self.largura, 0, self.fade_in_overlay_top(), (0, 0, 0, int(self.fade_in)))

        self.instr_text.draw()

    def fade_in_overlay_top(self) -> int:
        # retorna o top do overlay (padrão: altura da janela)
        return self.altura

    def on_update(self, delta_time: float) -> None:
        if self.fade_in > 0:
            self.fade_in -= 10
            if self.fade_in < 0:
                self.fade_in = 0

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        dialogos = TelaDialogos(font_name=self.font_name, bg_path=self.bg_path)
        dialogos.window = self.window
        self.window.show_view(dialogos)

    def on_key_press(self, symbol, modifiers) -> None:
        if symbol == arcade.key.ESCAPE:
            if hasattr(self.window, "menu_view") and self.window.menu_view:
                self.window.show_view(self.window.menu_view)
        elif symbol in (arcade.key.ENTER, arcade.key.RETURN, arcade.key.SPACE):
            dialogos = TelaDialogos(font_name=self.font_name, bg_path=self.bg_path)
            dialogos.window = self.window
            self.window.show_view(dialogos)
