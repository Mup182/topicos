# jogo_unificado_topicos.py
# Protótipo unificado — usa "asets/imagens" dentro da pasta do projeto (topicos)
import arcade
import os
from typing import Tuple

# Janela
LARGURA = 1280
ALTURA = 720
TITULO = "Ecos do Passado - Protótipo"

# Cores
COR_TEXTO = (240, 240, 240, 255)
COR_BOTAO = (50, 50, 50, 255)
COR_HOVER = (200, 180, 150, 255)
COR_SOMBRA = (20, 20, 20, 180)
COR_FUNDO_JOGO = (60, 50, 40, 255)

BASE_DIR = os.path.dirname(__file__)

# Ajustado para sua estrutura: topicos/asets/imagens/...
DEFAULT_BG_PATH = os.path.join(BASE_DIR, "asets", "imagens", "fundo_menu.jpg")
if not os.path.exists(DEFAULT_BG_PATH):
    # fallback para raiz (caso queira deixar o arquivo direto na pasta)
    DEFAULT_BG_PATH = os.path.join(BASE_DIR, "fundo_menu.jpg")
    if not os.path.exists(DEFAULT_BG_PATH):
        DEFAULT_BG_PATH = None

CLICK_SOUND_PATH = os.path.join(BASE_DIR, "asets", "imagens", "click.wav")
# ---------------- utilidades ----------------
def fit_font_size_measure(text: str, max_width: int, font_name: str, start_size: int = 36, min_size: int = 10):
    size = start_size
    has_measure = hasattr(arcade, "get_text_image_dimensions")
    while size >= min_size:
        try:
            if has_measure:
                w, h = arcade.get_text_image_dimensions(text, size, font_name)
            else:
                w = len(text) * (size * 0.5)
        except Exception:
            w = len(text) * (size * 0.5)
        if w <= max_width - 16:
            return size
        size -= 1
    return min_size

# ---------------- Botão (menu) ----------------
class Botao:
    def __init__(self, texto: str, center_x: int, center_y: int, largura: int, altura: int, acao: str = None):
        self.texto = texto
        self.center_x = center_x
        self.center_y = center_y
        self.base_largura = largura
        self.base_altura = altura
        self.acao = acao
        self.hover = False
        self.hover_scale = 1.0

    def update_hover(self, mouse_pos: Tuple[int, int]):
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
        self.hover_scale += (target - self.hover_scale) * 0.25

    def draw(self, mouse_pos: Tuple[int, int], font_name: str):
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
        arcade.draw_lrtb_rectangle_filled(left, right, top, bottom, cor)

        font_size = fit_font_size_measure(self.texto, largura, font_name, start_size=36, min_size=12)

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

# ---------------- View: TelaMenu ----------------
class TelaMenu(arcade.View):
    def __init__(self, largura=LARGURA, altura=ALTURA, bg_path: str = DEFAULT_BG_PATH):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.mouse_pos = (0, 0)
        self.bg_path = bg_path
        self.bg_texture = None

        self.font_name = os.path.join(BASE_DIR, "Montserrat-Bold.ttf")
        if not os.path.exists(self.font_name):
            self.font_name = "Arial"

        cx = self.largura // 2
        start_y = self.altura // 2 + 110
        step = 110
        largura_btn = 380
        altura_btn = 80
        self.botoes = [
            Botao("Novo Jogo", cx, start_y, largura_btn, altura_btn, acao="novo"),
            Botao("Carregar", cx, start_y - step, largura_btn, altura_btn, acao="carregar"),
            Botao("Configurações", cx, start_y - 2 * step, largura_btn, altura_btn, acao="config"),
        ]

    def on_show(self):
        arcade.set_background_color((0, 0, 0))
        if self.bg_path and os.path.exists(self.bg_path):
            try:
                self.bg_texture = arcade.load_texture(self.bg_path)
            except Exception as e:
                print("Erro ao carregar background:", e)
                self.bg_texture = None
        else:
            self.bg_texture = None

    def on_draw(self):
        arcade.start_render()
        if self.bg_texture:
            arcade.draw_lrwh_rectangle_textured(0, 0, self.largura, self.altura, self.bg_texture)
        else:
            arcade.draw_lrtb_rectangle_filled(0, self.largura, self.altura, 0, (20, 20, 20))

        arcade.draw_text("Ecos do Passado", self.largura // 2, self.altura - 120,
                         COR_TEXTO, font_size=72, anchor_x="center", anchor_y="center", font_name=self.font_name)

        for botao in self.botoes:
            botao.draw(self.mouse_pos, self.font_name)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.mouse_pos = (x, y)
        for b in self.botoes:
            b.update_hover(self.mouse_pos)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        for botao in self.botoes:
            if botao.contains(x, y):
                if botao.acao == "novo":
                    jogo = TelaJogo(self.largura, self.altura, font_name=self.font_name, bg_path=self.bg_path)
                    jogo.window = self.window
                    self.window.menu_view = self
                    self.window.show_view(jogo)
                elif botao.acao == "carregar":
                    print("Função de carregar ainda em desenvolvimento!")
                elif botao.acao == "config":
                    print("Abrir configurações (a implementar).")

# ---------------- View: TelaJogo (capítulo) ----------------
class TelaJogo(arcade.View):
    def __init__(self, largura=LARGURA, altura=ALTURA, font_name: str = None, bg_path: str = DEFAULT_BG_PATH):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.fade_in = 255
        self.background_color = COR_FUNDO_JOGO
        self.font_name = font_name or os.path.join(BASE_DIR, "Montserrat-Bold.ttf")
        if not os.path.exists(self.font_name):
            self.font_name = "Arial"
        self.bg_path = bg_path
        self.bg_texture = None

    def on_show(self):
        arcade.set_background_color(self.background_color)
        if self.bg_path and os.path.exists(self.bg_path):
            try:
                self.bg_texture = arcade.load_texture(self.bg_path)
            except Exception:
                self.bg_texture = None

    def on_draw(self):
        arcade.start_render()
        if self.bg_texture:
            arcade.draw_lrwh_rectangle_textured(0, 0, self.largura, self.altura, self.bg_texture)
        else:
            arcade.draw_lrtb_rectangle_filled(0, self.largura, self.altura, 0, self.background_color)

        texto = ("Capítulo 1 - Brasília, 1964\n\n"
                 "O filhote acordou e saiu em busca de comida. (substitua por seu texto completo se quiser.)")
        arcade.draw_text(texto,
                         self.largura // 2, self.altura // 2,
                         (255, 230, 200), font_size=28,
                         anchor_x="center", anchor_y="center", width=self.largura - 120, align="center",
                         font_name=self.font_name)
        if self.fade_in > 0:
            arcade.draw_lrtb_rectangle_filled(0, self.largura, self.altura, 0, (0, 0, 0, int(self.fade_in)))

        arcade.draw_text("Clique ou pressione [Enter] para continuar...",
                         20, 20, arcade.color.LIGHT_GRAY, font_size=14)

    def on_update(self, delta_time: float):
        if self.fade_in > 0:
            self.fade_in -= 10
            if self.fade_in < 0:
                self.fade_in = 0

    def on_mouse_press(self, x, y, button, modifiers):
        dialogos = TelaDialogos(font_name=self.font_name, bg_path=self.bg_path)
        dialogos.window = self.window
        self.window.show_view(dialogos)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(self.window.menu_view)
        elif symbol in (arcade.key.ENTER, arcade.key.RETURN, arcade.key.SPACE):
            dialogos = TelaDialogos(font_name=self.font_name, bg_path=self.bg_path)
            dialogos.window = self.window
            self.window.show_view(dialogos)

# ---------------- View: TelaDialogos ----------------
class TelaDialogos(arcade.View):
    def __init__(self, largura=LARGURA, altura=ALTURA, font_name: str = None, bg_path: str = DEFAULT_BG_PATH):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.font_name = font_name or os.path.join(BASE_DIR, "Montserrat-Bold.ttf")
        if not os.path.exists(self.font_name):
            self.font_name = "Arial"
        self.bg_path = bg_path

        # elementos inicializados no on_show
        self.spritelist = arcade.SpriteList()
        self.item1 = None
        self.ordem_itens = []
        self.ordem_index = 0
        self.dialogo_texto = []
        # carrega textos em blocos (cada bloco = uma string longa)
        self._carregar_textos_exemplo()

        # som de click opcional (procura em asets/imagens/click.wav)
        self.click = None
        if os.path.exists(CLICK_SOUND_PATH):
            try:
                self.click = arcade.load_sound(CLICK_SOUND_PATH)
            except Exception:
                self.click = None

    def _carregar_textos_exemplo(self):
        # Aqui você coloca blocos de texto mais longos.
        blocos = [
            ["Ache o filhote."],
            ["Enquanto explorava cautelosamente o terreno, o filhote percebeu algo se mexendo perto de um rio lamacento que cortava o lixão."],
            ["Era uma barata, deslizando lentamente entre os detritos e refletindo à luz cinzenta do dia. O gato, curioso e faminto, aproximou-se devagar e cada passo seu afundava um pouco na lama."],
            ["Entre o despejo do esgoto e restos de pneus, um peixe morto jazia à beira da água. Coberto de lama e moscas, era para o filhote uma refeição preciosa."]
        ]
        # transforma cada bloco (lista) em uma única string com espaços
        self.dialogo_texto = [" ".join(linhas).strip() for linhas in blocos]

    def on_show(self):
        arcade.set_background_color((10, 10, 10))
        self.spritelist = arcade.SpriteList()

        # background como sprite (se existir)
        if self.bg_path and os.path.exists(self.bg_path):
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

    def on_draw(self):
        self.clear()
        self.spritelist.draw()

        # caixa de diálogo maior (top=180)
        box_top = 180
        arcade.draw_lrtb_rectangle_filled(0, self.window.width, box_top, 0, (0, 0, 0, 200))

        # pega o bloco atual — é UMA STRING longa
        bloco = self.dialogo_texto[self.ordem_index]
        # desenha o texto dentro do box, com quebra automática width
        arcade.draw_text(
            bloco,
            40, 28,  # margem interna
            arcade.color.WHITE,
            font_size=18,
            width=self.window.width - 80,
            anchor_x="left",
            font_name=self.font_name
        )

        # dica de ação (se ainda houver blocos depois, mostra "Clique/Enter", se não, mostra "Voltar ao menu")
        if self.ordem_index < len(self.dialogo_texto) - 1:
            arcade.draw_text("Clique ou pressione [Enter] para continuar...",
                             self.window.width - 20, 8,
                             arcade.color.LIGHT_GRAY, font_size=12, anchor_x="right")
        else:
            arcade.draw_text("Fim do trecho. [Enter] ou clique para voltar ao menu",
                             self.window.width - 20, 8,
                             arcade.color.LIGHT_GRAY, font_size=12, anchor_x="right")

    def _advance_block(self):
        # avança para próximo bloco, ou finaliza (volta ao menu)
        if self.ordem_index < len(self.dialogo_texto) - 1:
            self.ordem_index += 1
        else:
            # fim dos diálogos: volta ao menu (mude se quiser avançar para outra cena)
            self.window.show_view(self.window.menu_view)

    def on_mouse_press(self, x, y, button, modifiers):
        # toca som se clicar no item (opcional)
        if self.click and self.item1 and self.item1.collides_with_point((x, y)):
            arcade.play_sound(self.click)
        # avançar um bloco por clique em qualquer lugar (comportamento prático)
        self._advance_block()

    def on_key_press(self, symbol, modifiers):
        if symbol in (arcade.key.SPACE, arcade.key.ENTER, arcade.key.RETURN):
            self._advance_block()
        elif symbol == arcade.key.ESCAPE:
            self.window.show_view(self.window.menu_view)

# ---------------- main ----------------
def main():
    janela = arcade.Window(LARGURA, ALTURA, TITULO)
    menu = TelaMenu(LARGURA, ALTURA, bg_path=DEFAULT_BG_PATH)
    janela.menu_view = menu
    janela.show_view(menu)
    arcade.run()

if __name__ == "__main__":
    main()
