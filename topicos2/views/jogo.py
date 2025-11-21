# views/jogo.py
import arcade
from typing import Optional
from core.settings import LARGURA, ALTURA, DEFAULT_BG_PATH, COR_FUNDO_JOGO
from core.utils import safe_load_texture
from views.dialogos import TelaDialogos


class TelaJogo(arcade.View):
    def __init__(self, largura: int = LARGURA, altura: int = ALTURA, font_name: Optional[str] = None, bg_path: str = DEFAULT_BG_PATH):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.font_name = font_name or "Arial"
        self.bg_path = bg_path
        self.bg_texture = safe_load_texture(self.bg_path)
        self.fade_in = 255

        # texto do capítulo — use arcade.Text com width e align para quebra/centralização
        texto = (
            "Capítulo 1 - Brasília, 1964\n\n"
            "O filhote acordou e saiu em busca de comida. (substitua por seu texto completo se quiser.)"
        )
        # font_size inicial, pode ser ajustado dinamicamente em on_resize
        self.chapter_font_size = 28
        self.chapter_text = arcade.Text(
            texto,
            self.largura // 2,
            self.altura // 2,
            color=(255, 230, 200),
            font_size=self.chapter_font_size,
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
        arcade.set_background_color(COR_FUNDO_JOGO)
        self.bg_texture = safe_load_texture(self.bg_path)

    def on_draw(self) -> None:
        self.clear()

        width = self.window.width if self.window else self.largura
        height = self.window.height if self.window else self.altura

        if self.bg_texture:
            arcade.draw_lrwh_rectangle_textured(0, 0, width, height, self.bg_texture)
        else:
            arcade.draw_lrbt_rectangle_filled(0, width, 0, height, COR_FUNDO_JOGO)

        # atualiza posição e largura caso a janela tenha sido redimensionada
        self.chapter_text.position = (width // 2, height // 2)
        self.chapter_text.width = max(100, width - 120)
        self.chapter_text.font_size = self.chapter_font_size
        self.chapter_text.draw()

        # Fade-in overlay: desenha um retângulo com alpha decrescente
        if self.fade_in > 0:
            arcade.draw_lrbt_rectangle_filled(0, width, 0, height, (0, 0, 0, int(self.fade_in)))

        self.instr_text.draw()

    def on_update(self, delta_time: float) -> None:
        if self.fade_in > 0:
            self.fade_in -= 10
            if self.fade_in < 0:
                self.fade_in = 0

    def _open_dialogos(self) -> None:
        dialogos = TelaDialogos(font_name=self.font_name, bg_path=self.bg_path)
        # não é necessário setar dialogos.window manualmente — show_view faz isso
        self.window.show_view(dialogos)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        self._open_dialogos()

    def on_key_press(self, symbol, modifiers) -> None:
        if symbol == arcade.key.ESCAPE:
            if hasattr(self.window, "menu_view") and self.window.menu_view:
                self.window.show_view(self.window.menu_view)
        elif symbol in (arcade.key.ENTER, arcade.key.RETURN, arcade.key.SPACE):
            self._open_dialogos()

    def on_resize(self, width: int, height: int) -> None:
        # atualiza dims e recalcula tamanhos responsivos
        self.largura = width
        self.altura = height
        # reduz o tamanho da fonte em telas muito pequenas para evitar overflow
        ideal_font = max(14, int(width * 0.03))
        # limita para um máximo razoável
        self.chapter_font_size = min(36, ideal_font)
        self.chapter_text.font_size = self.chapter_font_size
        self.chapter_text.width = max(100, width - 120)
        self.chapter_text.position = (width // 2, height // 2)