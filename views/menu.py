# views/menu.py — versão DEFINITIVA para Arcade 3.3.3 (sem nenhum draw_rectangle)
import arcade
from typing import Tuple, Optional, List

from core.settings import DEFAULT_BG_PATH, LARGURA, ALTURA, COR_TEXTO
from core.utils import safe_load_texture
from ui.botao import Botao
from views.dialogos import TelaDialogos


class TelaMenu(arcade.View):
    def __init__(
        self,
        largura: int = LARGURA,
        altura: int = ALTURA,
        font_name: Optional[str] = None,
        bg_path: Optional[str] = DEFAULT_BG_PATH
    ):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.bg_path = bg_path
        self.bg_texture = safe_load_texture(self.bg_path)

        self.font_name = font_name or "Arial"
        self.mouse_pos: Tuple[int, int] = (0, 0)

        cx = self.largura // 2
        start_y = self.altura // 2 + 110
        step = 110
        largura_btn = 380
        altura_btn = 80

        self.botoes: List[Botao] = [
            Botao("Novo Jogo", cx, start_y, largura_btn, altura_btn, acao="novo"),
            Botao("Carregar", cx, start_y - step, largura_btn, altura_btn, acao="carregar"),
            Botao("Configurações", cx, start_y - 2 * step, largura_btn, altura_btn, acao="config")
        ]

        # Textos
        self.title_text = arcade.Text(
            "Ecos do Passado",
            self.largura // 2,
            self.altura - 120,
            color=COR_TEXTO,
            font_size=72,
            anchor_x="center",
            anchor_y="center",
            font_name=self.font_name
        )

        self.footer_text = arcade.Text(
            "Use o mouse para navegar",
            20,
            20,
            color=arcade.color.LIGHT_GRAY,
            font_size=14,
            anchor_x="left",
            anchor_y="bottom",
            font_name=self.font_name
        )

    def on_show(self):
        arcade.set_background_color((0, 0, 0))

    # -------------------------------------------------------------------
    # DESENHAR FUNDO — compatível com Arcade 3.3.3
    # -------------------------------------------------------------------
    def _draw_bg(self):
        if self.bg_texture:
            try:
                arcade.draw_lrwh_rectangle_textured(
                    0, 0,
                    self.largura,
                    self.altura,
                    self.bg_texture
                )
                return
            except:
                pass

        # fallback: preenchimento com draw_line
        for y in range(0, self.altura, 4):
            arcade.draw_line(0, y, self.largura, y, (20, 20, 20), 4)

    # -------------------------------------------------------------------
    # DESENHAR BOTÃO — usando APENAS draw_line
    # -------------------------------------------------------------------
    def _draw_button_rect(self, botao):
        left = botao.cx - botao.width/2
        right = botao.cx + botao.width/2
        bottom = botao.cy - botao.height/2
        top = botao.cy + botao.height/2

        color = (80, 80, 80) if botao.hover else (40, 40, 40)

        # preenchimento com linhas
        y = int(bottom)
        while y < int(top):
            arcade.draw_line(left, y, right, y, color, 4)
            y += 4

        # contorno branco
        arcade.draw_line(left, bottom, right, bottom, arcade.color.WHITE, 2)
        arcade.draw_line(left, top, right, top, arcade.color.WHITE, 2)
        arcade.draw_line(left, bottom, left, top, arcade.color.WHITE, 2)
        arcade.draw_line(right, bottom, right, top, arcade.color.WHITE, 2)

    def on_draw(self):
        self.clear()

        self._draw_bg()

        self.title_text.draw()

        # desenhar botões
        for botao in self.botoes:
            self._draw_button_rect(botao)
            botao.draw(self.mouse_pos, self.font_name)

        self.footer_text.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos = (x, y)
        for b in self.botoes:
            b.update_hover(self.mouse_pos)

    def on_mouse_press(self, x, y, button, modifiers):
        for botao in self.botoes:
            if botao.contains(x, y):

                if botao.acao == "novo":
                    cena = TelaDialogos(
                        largura=self.largura,
                        altura=self.altura,
                        arquivo_json="cena_exemplo.json",
                        font_name=self.font_name
                    )
                    self.window.menu_view = self
                    self.window.show_view(cena)

                elif botao.acao == "carregar":
                    print("Função carregar ainda não implementada.")

                elif botao.acao == "config":
                    print("Configurações ainda não implementadas.")
