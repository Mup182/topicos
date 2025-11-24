# views/jogo.py — versão sem travar (troca de view em on_update)
import arcade
from typing import Optional
from core.settings import LARGURA, ALTURA, DEFAULT_BG_PATH, COR_FUNDO_JOGO
from core.utils import safe_load_texture
from views.dialogos import TelaDialogos


class TelaJogo(arcade.View):
    """
    Tela principal do jogo.
    Troca de view em on_update para evitar deadlock/travamento no Windows/Pyglet.
    """

    def __init__(
        self,
        largura: int = LARGURA,
        altura: int = ALTURA,
        font_name: Optional[str] = None,
        bg_path: str = DEFAULT_BG_PATH
    ):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.font_name = font_name or "Arial"

        self.bg_path = bg_path
        self.bg_texture = safe_load_texture(self.bg_path)

        # Flag para trocar de tela apenas uma vez
        self._trocar = True

    def on_show(self):
        arcade.set_background_color(COR_FUNDO_JOGO)

    def on_update(self, delta_time: float):
        """
        Troca segura de view. O Arcade recomenda trocar a view aqui.
        """
        if self._trocar:
            self._trocar = False
            dialogos_view = TelaDialogos(largura=self.largura, altura=self.altura, font_name=self.font_name)
            self.window.show_view(dialogos_view)

    def on_draw(self):
        # Não desenha nada aqui intencionalmente
        pass

    def on_resize(self, width: int, height: int):
        self.largura = width
        self.altura = height
