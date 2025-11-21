# views/dialogos.py
import os
import arcade
from typing import List, Optional
from core.utils import safe_load_texture
from core.settings import (
    DEFAULT_BG_PATH, 
    CLICK_SOUND_PATH,
    DIALOG_BOX_HEIGHT,
    DIALOG_MARGIN_LEFT,
    DIALOG_MARGIN_RIGHT,
    DIALOG_MARGIN_BOTTOM,
    DIALOG_MARGIN_TOP
)


class TelaDialogos(arcade.View):
    def __init__(
        self,
        largura: int = 1280,
        altura: int = 720,
        font_name: Optional[str] = None,
        bg_path: Optional[str] = DEFAULT_BG_PATH,
    ):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.font_name = font_name or "Arial"
        self.bg_path = bg_path
        self.bg_texture = safe_load_texture(self.bg_path)

        self.spritelist: arcade.SpriteList = arcade.SpriteList()
        self.item1: Optional[arcade.Sprite] = None
        self.ordem_itens: List[arcade.Sprite] = []
        self.ordem_index: int = 0
        self.dialogo_texto: List[str] = []
        # garante que o atributo exista antes de on_show
        self.dialogo_text_objs: List[arcade.Text] = []
        self._carregar_textos_exemplo()
        self.click = None

    def _carregar_textos_exemplo(self) -> None:
        blocos = [
            ["Ache o filhote."],
            [
                "Enquanto explorava cautelosamente o terreno, o filhote percebeu algo se mexendo perto de um rio lamacento que cortava o lixão."
            ],
            [
                "Era uma barata, deslizando lentamente entre os detritos e refletindo à luz cinzenta do dia. O gato, curioso e faminto, aproximou-se devagar..."
            ],
            [
                "Entre o despejo do esgoto e restos de pneus, um peixe morto jazia à beira da água. Coberto de lama e moscas, era para o filhote uma refeição preciosa."
            ],
        ]
        self.dialogo_texto = [" ".join(linhas).strip() for linhas in blocos]
        print(f"DEBUG: Carregados {len(self.dialogo_texto)} blocos de diálogo em _carregar_textos_exemplo()")

    def _criar_text_objs(self) -> None:
        """(Re)cria os objetos arcade.Text a partir de self.dialogo_texto,
        usando a largura atual da janela para a quebra de linha."""
        # Valida que há diálogos para criar
        if not self.dialogo_texto:
            print("AVISO: dialogo_texto está vazio em _criar_text_objs()")
            self.dialogo_text_objs = []
            return
            
        try:
            # Calcula largura disponível respeitando as margens configuradas
            window_width = self.window.width if self.window else self.largura
            largura_disponivel = max(100, window_width - DIALOG_MARGIN_LEFT - DIALOG_MARGIN_RIGHT)
            
            # Posição inicial (x,y) dentro da caixa de diálogo usando as margens configuradas
            x = DIALOG_MARGIN_LEFT
            y = DIALOG_MARGIN_BOTTOM
            
            self.dialogo_text_objs = [
                arcade.Text(
                    txt,
                    x,
                    y,
                    arcade.color.WHITE,
                    font_size=18,
                    width=largura_disponivel,
                    anchor_x="left",
                    anchor_y="bottom",
                    font_name=self.font_name,
                )
                for txt in self.dialogo_texto
            ]
            print(f"DEBUG: Criados {len(self.dialogo_text_objs)} objetos de texto de diálogo")
        except Exception as e:
            print(f"ERRO ao criar objetos de texto: {e}")
            import traceback
            traceback.print_exc()
            self.dialogo_text_objs = []

    def on_show(self) -> None:
        arcade.set_background_color((10, 10, 10))
        self.spritelist = arcade.SpriteList()

        # Valida que os diálogos foram carregados
        if not self.dialogo_texto:
            print("AVISO: dialogo_texto está vazio em on_show(). Carregando textos de exemplo...")
            self._carregar_textos_exemplo()

        # background como sprite (se existir)
        if self.bg_texture:
            try:
                fundo = arcade.Sprite(
                    self.bg_path,
                    scale=max(self.window.width / 1280, self.window.height / 720),
                    center_x=self.window.width // 2,
                    center_y=self.window.height // 2,
                )
                self.spritelist.append(fundo)
            except Exception:
                # se falhar ao criar o sprite de background, apenas ignoramos
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

        # (re)cria os Text objects para os diálogos agora que temos acesso à janela
        self._criar_text_objs()
        
        # Valida que os text objects foram criados
        if not self.dialogo_text_objs:
            print("ERRO: dialogo_text_objs ainda está vazio após _criar_text_objs()")

    def on_draw(self) -> None:
        self.clear()
        self.spritelist.draw()

        # Desenha a caixa de diálogo usando a altura configurada
        # left, right, bottom, top
        arcade.draw_lrbt_rectangle_filled(0, self.window.width, 0, DIALOG_BOX_HEIGHT, (0, 0, 0, 200))

        # Garantir que os text objects existam (caso on_draw seja chamado antes de on_show)
        if not self.dialogo_text_objs and self.dialogo_texto:
            print("AVISO: on_draw chamado antes de on_show. Criando text objects...")
            self._criar_text_objs()

        # desenha o bloco atual via Text objeto pré-criado
        if self.dialogo_text_objs:
            txt_obj = self.dialogo_text_objs[self.ordem_index]
            # atualiza largura caso a janela tenha mudado, respeitando as margens
            txt_obj.width = max(100, self.window.width - DIALOG_MARGIN_LEFT - DIALOG_MARGIN_RIGHT)
            # a posição x/y foi definida na criação; redesenha
            txt_obj.draw()
        else:
            # fallback mínimo (não deveria ocorrer se on_show rodou corretamente)
            arcade.draw_text(
                "Sem diálogos carregados.",
                DIALOG_MARGIN_LEFT,
                DIALOG_MARGIN_BOTTOM,
                arcade.color.WHITE,
                font_size=18,
                width=max(100, self.window.width - DIALOG_MARGIN_LEFT - DIALOG_MARGIN_RIGHT),
                anchor_x="left",
                anchor_y="bottom",
                font_name=self.font_name,
            )

        if self.ordem_index < len(self.dialogo_texto) - 1:
            arcade.draw_text(
                "Clique ou pressione [Enter] para continuar.",
                self.window.width - 20,
                8,
                arcade.color.LIGHT_GRAY,
                font_size=12,
                anchor_x="right",
            )
        else:
            arcade.draw_text(
                "Fim do trecho. [Enter] ou clique para voltar ao menu",
                self.window.width - 20,
                8,
                arcade.color.LIGHT_GRAY,
                font_size=12,
                anchor_x="right",
            )

    def _advance_block(self) -> None:
        if self.ordem_index < len(self.dialogo_texto) - 1:
            self.ordem_index += 1
        else:
            if hasattr(self.window, "menu_view") and self.window.menu_view:
                self.window.show_view(self.window.menu_view)

    def on_mouse_press(self, x: int, y: int, button, modifiers) -> None:
        if self.click and self.item1 and self.item1.collides_with_point((x, y)):
            arcade.play_sound(self.click)
        self._advance_block()

    def on_key_press(self, symbol, modifiers) -> None:
        if symbol in (arcade.key.SPACE, arcade.key.ENTER, arcade.key.RETURN):
            self._advance_block()
        elif symbol == arcade.key.ESCAPE:
            if hasattr(self.window, "menu_view") and self.window.menu_view:
                self.window.show_view(self.window.menu_view)

    def on_resize(self, width: int, height: int) -> None:
        # atualiza e recria objetos de texto para respeitar a nova largura
        self.largura = width
        self.altura = height
        if self.dialogo_texto:
            self._criar_text_objs()