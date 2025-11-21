# views/menu.py
import os
import arcade
from typing import Tuple, Optional, List
from core.settings import DEFAULT_BG_PATH, LARGURA, ALTURA, COR_TEXTO
from core.utils import safe_load_texture
from ui.botao import Botao
from views.jogo import TelaJogo  # import local para facilitar navegação

class TelaMenu(arcade.View):
    def __init__(self, largura: int = LARGURA, altura: int = ALTURA, font_name: Optional[str] = None, bg_path: Optional[str] = DEFAULT_BG_PATH):
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
            Botao("Configurações", cx, start_y - 2 * step, largura_btn, altura_btn, acao="config"),
        ]

        # Inicializa os objetos Text aqui para evitar AttributeError
        self.title_text = arcade.Text(
            "Ecos do Passado",
            self.largura // 2, self.altura - 120,
            color=COR_TEXTO,
            font_size=72,
            anchor_x="center",
            anchor_y="center",
            font_name=self.font_name
        )
        self.footer_text = arcade.Text(
            "Use o mouse para navegar",
            20, 20,
            color=arcade.color.LIGHT_GRAY,
            font_size=14,
            anchor_x="left",
            anchor_y="bottom",
            font_name=self.font_name
        )

        # click_sound opcional: define como None por padrão (seguro)
        self.click_sound = None

    def on_show(self) -> None:
        arcade.set_background_color((0, 0, 0))
        # tenta carregar som opcional (não interrompe se falhar)
        try:
            sound_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "asets", "imagens", "click.wav")
            self.click_sound = arcade.load_sound(sound_path) if os.path.exists(sound_path) else None
        except Exception:
            self.click_sound = None

    def on_draw(self) -> None:
        self.clear()
        if self.bg_texture:
            arcade.draw_lrwh_rectangle_textured(0, 0, self.largura, self.altura, self.bg_texture)
        else:
            arcade.draw_lrbt_rectangle_filled(0, self.largura, 0, self.altura, (20, 20, 20))

        # Atualiza posição antes de desenhar (caso a janela tenha sido redimensionada)
        self.title_text.position = (self.largura // 2, self.altura - 120)
        self.title_text.draw()

        # botões
        for botao in self.botoes:
            botao.draw(self.mouse_pos, self.font_name)

        # footer
        self.footer_text.position = (20, 20)
        self.footer_text.draw()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        self.mouse_pos = (x, y)
        for b in self.botoes:
            b.update_hover(self.mouse_pos)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        for botao in self.botoes:
            if botao.contains(x, y):
                if botao.acao == "novo":
                    jogo = TelaJogo(self.largura, self.altura, font_name=self.font_name, bg_path=self.bg_path)
                    jogo.window = self.window
                    # guarda referência para voltar ao menu
                    self.window.menu_view = self
                    self.window.show_view(jogo)
                elif botao.acao == "carregar":
                    # placeholder
                    print("Função de carregar ainda em desenvolvimento!")
                elif botao.acao == "config":
                    print("Abrir configurações (a implementar).")
