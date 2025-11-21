"""
Ecos do Passado - versão organizada (único arquivo, pronta para dividir)

O arquivo foi reestruturado para:
- Separar constantes, utilitários, UI (Botao), Views (TelaMenu, TelaJogo, TelaDialogos) e main.
- Corrigir usos incorretos do Arcade (start_render -> self.clear em Views).
- Garantir consistência nas chamadas draw_* de acordo com a API (draw_lrbt_rectangle_filled).
- Tornar o código mais legível e fácil de dividir posteriormente.
"""

import os
import arcade
from typing import Tuple, List, Optional

# ----------------------------
# Configurações / Constantes
# ----------------------------
LARGURA = 1280
ALTURA = 720
TITULO = "Ecos do Passado - Protótipo"

BASE_DIR = os.path.dirname(__file__)
DEFAULT_BG_PATH = os.path.join(BASE_DIR, "asets", "imagens", "fundo_menu.jpg")
if not os.path.exists(DEFAULT_BG_PATH):
    alt = os.path.join(BASE_DIR, "fundo_menu.jpg")
    DEFAULT_BG_PATH = alt if os.path.exists(alt) else None

CLICK_SOUND_PATH = os.path.join(BASE_DIR, "asets", "imagens", "click.wav")

# Colors
COR_TEXTO = (140, 140, 140, 255)
COR_BOTAO = (50, 50, 50, 255)
COR_HOVER = (100, 110, 150, 255)
COR_SOMBRA = (20, 20, 20, 180)
COR_FUNDO_JOGO = (60, 50, 40, 255)

# ----------------------------
# Utilitários
# ----------------------------
def safe_load_texture(path: Optional[str]) -> Optional[arcade.Texture]:
    """Tenta carregar uma textura, retorna None se falhar ou caminho for None."""
    if not path:
        return None
    try:
        return arcade.load_texture(path)
    except Exception:
        return None

def fit_font_size_measure(text: str, max_width: int, font_name: str, start_size: int = 36, min_size: int = 10) -> int:
    """
    Ajusta um tamanho de fonte para que o texto caiba em `max_width`.
    Usa arcade.get_text_image_dimensions quando disponível; caso contrário, usa uma estimativa.
    """
    size = start_size
    has_measure = hasattr(arcade, "get_text_image_dimensions")
    while size >= min_size:
        try:
            if has_measure:
                w, _ = arcade.get_text_image_dimensions(text, size, font_name)
            else:
                w = len(text) * (size * 0.5)
        except Exception:
            w = len(text) * (size * 0.5)
        if w <= max_width - 16:
            return size
        size -= 1
    return min_size

# ----------------------------
# UI: Botão
# ----------------------------
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

# ----------------------------
# Views (telas)
# ----------------------------
class TelaBase(arcade.View):
    """Uma View base com utilitários úteis compartilhados."""
    def __init__(self, largura: int = LARGURA, altura: int = ALTURA, font_name: Optional[str] = None, bg_path: Optional[str] = DEFAULT_BG_PATH):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.font_name = font_name or os.path.join(BASE_DIR, "Montserrat-Bold.ttf")
        if not os.path.exists(self.font_name):
            # fallback para fonte padrão do sistema
            self.font_name = "Arial"
        self.bg_path = bg_path
        self.bg_texture = None

    def on_show(self) -> None:
        """Carrega background se existir e define cor de fundo default."""
        arcade.set_background_color((0, 0, 0))
        self.bg_texture = safe_load_texture(self.bg_path)

class TelaMenu(TelaBase):
    def __init__(self, largura: int = LARGURA, altura: int = ALTURA, font_name: Optional[str] = None, bg_path: Optional[str] = DEFAULT_BG_PATH):
        super().__init__(largura, altura, font_name, bg_path)
        self.mouse_pos = (0, 0)

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

    def on_show(self) -> None:
        super().on_show()
        # carrega som opcional
        try:
            self.click_sound = arcade.load_sound(CLICK_SOUND_PATH) if os.path.exists(CLICK_SOUND_PATH) else None
        except Exception:
            self.click_sound = None

    def on_draw(self) -> None:
        # Em Views devemos usar self.clear() em vez de arcade.start_render()
        self.clear()

        # Desenha background
        if self.bg_texture:
            arcade.draw_lrwh_rectangle_textured(0, 0, self.largura, self.altura, self.bg_texture)
        else:
            # note a API: draw_lrbt_rectangle_filled(left, right, bottom, top, color)
            arcade.draw_lrbt_rectangle_filled(0, self.largura, 0, self.altura, (20, 20, 20))

        # Título
        arcade.draw_text("Ecos do Passado", self.largura // 2, self.altura - 120,
                         COR_TEXTO, font_size=72, anchor_x="center", anchor_y="center", font_name=self.font_name)

        # Botões
        for botao in self.botoes:
            botao.draw(self.mouse_pos, self.font_name)

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

class TelaJogo(TelaBase):
    def __init__(self, largura: int = LARGURA, altura: int = ALTURA, font_name: Optional[str] = None, bg_path: Optional[str] = DEFAULT_BG_PATH):
        super().__init__(largura, altura, font_name, bg_path)
        self.fade_in = 255

    def on_show(self) -> None:
        super().on_show()
        arcade.set_background_color(self.background_color if hasattr(self, "background_color") else COR_FUNDO_JOGO)

    @property
    def background_color(self):
        return COR_FUNDO_JOGO

    def on_draw(self) -> None:
        self.clear()
        if self.bg_texture:
            arcade.draw_lrwh_rectangle_textured(0, 0, self.largura, self.altura, self.bg_texture)
        else:
            arcade.draw_lrbt_rectangle_filled(0, self.largura, 0, self.altura, self.background_color)

        texto = ("Capítulo 1 - Brasília, 1964\n\n"
                 "O filhote acordou e saiu em busca de comida. (substitua por seu texto completo se quiser.)")
        arcade.draw_text(texto,
                         self.largura // 2, self.altura // 2,
                         (255, 230, 200), font_size=28,
                         anchor_x="center", anchor_y="center", width=self.largura - 120, align="center",
                         font_name=self.font_name)

        # Fade-in overlay
        if self.fade_in > 0:
            arcade.draw_lrbt_rectangle_filled(0, self.largura, 0, self.fade_in_overlay_top(), (0, 0, 0, int(self.fade_in)))

        arcade.draw_text("Clique ou pressione [Enter] para continuar.",
                         20, 20, arcade.color.LIGHT_GRAY, font_size=14)

    def fade_in_overlay_top(self) -> int:
        """
        Calcula o 'top' para o overlay de fade.
        Mantive como função para facilitar ajustes futuros.
        """
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

class TelaDialogos(TelaBase):
    def __init__(self, largura: int = LARGURA, altura: int = ALTURA, font_name: Optional[str] = None, bg_path: Optional[str] = DEFAULT_BG_PATH):
        super().__init__(largura, altura, font_name, bg_path)
        self.spritelist: arcade.SpriteList = arcade.SpriteList()
        self.item1: Optional[arcade.Sprite] = None
        self.ordem_itens: List[arcade.Sprite] = []
        self.ordem_index: int = 0
        self.dialogo_texto: List[str] = []
        self._carregar_textos_exemplo()
        self.click = None

    def _carregar_textos_exemplo(self) -> None:
        blocos = [
            ["Ache o filhote."],
            ["Enquanto explorava cautelosamente o terreno, o filhote percebeu algo se mexendo perto de um rio lamacento que cortava o lixão."],
            ["Era uma barata, deslizando lentamente entre os detritos e refletindo à luz cinzenta do dia. O gato, curioso e faminto, aproximou-se devagar e cada passo seu afundava um pouco na lama."],
            ["Entre o despejo do esgoto e restos de pneus, um peixe morto jazia à beira da água. Coberto de lama e moscas, era para o filhote uma refeição preciosa."]
        ]
        self.dialogo_texto = [" ".join(linhas).strip() for linhas in blocos]

    def on_show(self) -> None:
        super().on_show()
        self.spritelist = arcade.SpriteList()

        # background como sprite (se existir)
        if self.bg_texture:
            try:
                fundo = arcade.Sprite(self.bg_path,
                                      scale=max(self.window.width / 1280, self.window.height / 720),
                                      center_x=self.window.width // 2,
                                      center_y=self.window.height // 2)
                self.spritelist.append(fundo)
            except Exception:
                pass

        # cria um item interativo (placeholder) - sprite sólido
        self.item1 = arcade.SpriteSolidColor(56, 56, arcade.color.BRONZE)
        self.item1.center_x = self.window.width // 2
        self.item1.center_y = 150
        self.spritelist.append(self.item1)

        self.ordem_itens = [self.item1]
        self.ordem_index = 0

        # som opcional
        try:
            self.click = arcade.load_sound(CLICK_SOUND_PATH) if os.path.exists(CLICK_SOUND_PATH) else None
        except Exception:
            self.click = None

    def on_draw(self) -> None:
        self.clear()
        self.spritelist.draw()

        # caixa de diálogo maior (top=180) - note API draw_lrbt_rectangle_filled(left, right, bottom, top, color)
        box_top = 180
        arcade.draw_lrbt_rectangle_filled(0, self.window.width, 0, box_top, (0, 0, 0, 200))

        bloco = self.dialogo_texto[self.ordem_index]
        arcade.draw_text(
            bloco,
            40, 28,  # margem interna
            arcade.color.WHITE,
            font_size=18,
            width=self.window.width - 80,
            anchor_x="left",
            font_name=self.font_name
        )

        if self.ordem_index < len(self.dialogo_texto) - 1:
            arcade.draw_text("Clique ou pressione [Enter] para continuar.",
                             self.window.width - 20, 8,
                             arcade.color.LIGHT_GRAY, font_size=12, anchor_x="right")
        else:
            arcade.draw_text("Fim do trecho. [Enter] ou clique para voltar ao menu",
                             self.window.width - 20, 8,
                             arcade.color.LIGHT_GRAY, font_size=12, anchor_x="right")

    def _advance_block(self) -> None:
        if self.ordem_index < len(self.dialogo_texto) - 1:
            self.ordem_index += 1
        else:
            if hasattr(self.window, "menu_view") and self.window.menu_view:
                self.window.show_view(self.window.menu_view)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> None:
        if self.click and self.item1 and self.item1.collides_with_point((x, y)):
            arcade.play_sound(self.click)
        self._advance_block()

    def on_key_press(self, symbol, modifiers) -> None:
        if symbol in (arcade.key.SPACE, arcade.key.ENTER, arcade.key.RETURN):
            self._advance_block()
        elif symbol == arcade.key.ESCAPE:
            if hasattr(self.window, "menu_view") and self.window.menu_view:
                self.window.show_view(self.window.menu_view)

# ----------------------------
# Main
# ----------------------------
def main():
    janela = arcade.Window(LARGURA, ALTURA, TITULO)
    menu = TelaMenu(LARGURA, ALTURA, bg_path=DEFAULT_BG_PATH)
    janela.menu_view = menu
    janela.show_view(menu)
    arcade.run()

if __name__ == "__main__":
    main()
