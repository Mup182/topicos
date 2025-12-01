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

        #musica
        self.musica_ativa = True
        self.musica_player = None
        self.musica_obj = None

        # menuprincipal
        cx = self.largura // 2
        start_y = self.altura // 2 + 110
        step = 110
        largura_btn = 380
        altura_btn = 80

        self.cx = cx
        self.largura_btn = largura_btn
        self.altura_btn = altura_btn
        self.start_y = start_y
        self.step = step

        self.botoes: List[Botao] = [
            Botao("Novo Jogo", cx, start_y, largura_btn, altura_btn, acao="novo"),
            Botao("Carregar", cx, start_y - step, largura_btn, altura_btn, acao="carregar"),
            Botao("Configurações", cx, start_y - 2 * step, largura_btn, altura_btn, acao="config"),
        ]

        # mini-tela de config
        self.modo_config = False
        self.botao_musica = self.__criar_botao_musica("Desativar Música")
        self.botao_voltar = Botao(
            "Voltar",
            cx,
            self.altura//2 - 140,
            300, 80,
            acao="voltar_config"
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

    # helper para criar o botão de música
    def __criar_botao_musica(self, texto: str) -> Botao:
        return Botao(
            texto,
            self.cx,
            self.altura//2,
            420, 90,
            acao="toggle_musica"
        )

    #audio
    def _carregar_musica(self):
        caminho = "views/sounds/musica.wav"
        print("Carregando música:", caminho)

        try:
            self.musica_obj = arcade.load_sound(caminho)
        except Exception as e:
            print("ERRO ao carregar música:", e)
            self.musica_obj = None

    def _tocar_musica(self):
        if not self.musica_obj:
            return
        if not self.musica_ativa:
            return
        if self.musica_player:
            return

        try:
            self.musica_player = self.musica_obj.play(volume=0.4, loop=True)
        except TypeError:
            try:
                self.musica_player = self.musica_obj.play()
            except Exception as e:
                print("Erro ao tocar música (fallback):", e)
        except Exception as e:
            print("Erro ao tocar música:", e)

    def _parar_musica(self):
        if self.musica_player:
            try:
                if hasattr(self.musica_player, "pause"):
                    self.musica_player.pause()
                elif hasattr(self.musica_player, "stop"):
                    self.musica_player.stop()
            except Exception:
                pass
        self.musica_player = None

    def on_show(self):
        arcade.set_background_color((0, 0, 0))
        self._carregar_musica()
        self._tocar_musica()

    # ---------------------------- FUNDO ----------------------------
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

        for y in range(0, self.altura, 4):
            arcade.draw_line(0, y, self.largura, y, (20, 20, 20), 4)

    # ---------------------------- DESENHAR ----------------------------
    def _draw_button_rect(self, botao):
        left = botao.cx - botao.width/2
        right = botao.cx + botao.width/2
        bottom = botao.cy - botao.height/2
        top = botao.cy + botao.height/2

        color = (80, 80, 80) if botao.hover else (40, 40, 40)

        y = int(bottom)
        while y < int(top):
            arcade.draw_line(left, y, right, y, color, 4)
            y += 4

        arcade.draw_line(left, bottom, right, bottom, arcade.color.WHITE, 2)
        arcade.draw_line(left, top, right, top, arcade.color.WHITE, 2)
        arcade.draw_line(left, bottom, left, top, arcade.color.WHITE, 2)
        arcade.draw_line(right, bottom, right, top, arcade.color.WHITE, 2)

    def on_draw(self):
        self.clear()
        self._draw_bg()

        # ---------------- TÍTULO COM SOMBRA ----------------
        arcade.draw_text(
            "Ecos do Passado",
            self.largura // 2 + 4,
            self.altura - 120 - 4,
            (0, 0, 0, 220),
            72,
            anchor_x="center",
            anchor_y="center",
            font_name=self.font_name
        )

        arcade.draw_text(
            "Ecos do Passado",
            self.largura // 2,
            self.altura - 120,
            (120, 120, 120),
            72,
            anchor_x="center",
            anchor_y="center",
            font_name=self.font_name
        )
        # ---------------------------------------------------

        if not self.modo_config:
            for botao in self.botoes:
                self._draw_button_rect(botao)
                botao.draw(self.mouse_pos, self.font_name)
        else:
            self._draw_button_rect(self.botao_musica)
            self.botao_musica.draw(self.mouse_pos, self.font_name)

            self._draw_button_rect(self.botao_voltar)
            self.botao_voltar.draw(self.mouse_pos, self.font_name)

        self.footer_text.draw()

    # ---------------------------- INPUT ----------------------------
    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pos = (x, y)

        if not self.modo_config:
            for b in self.botoes:
                b.update_hover(self.mouse_pos)
        else:
            self.botao_musica.update_hover(self.mouse_pos)
            self.botao_voltar.update_hover(self.mouse_pos)

    def on_mouse_press(self, x, y, button, modifiers):

        # ------------- CONFIG -------------
        if self.modo_config:
            if self.botao_musica.contains(x, y):

                if self.musica_ativa:
                    self.musica_ativa = False
                    self._parar_musica()
                    self.botao_musica = self.__criar_botao_musica("Ativar Música")
                else:
                    self.musica_ativa = True
                    self.botao_musica = self.__criar_botao_musica("Desativar Música")
                    self._tocar_musica()

            elif self.botao_voltar.contains(x, y):
                self.modo_config = False

            return

        # ------------- MENU PRINCIPAL -------------
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
                    self.modo_config = True

                    if self.musica_ativa:
                        self.botao_musica = self.__criar_botao_musica("Desativar Música")
                    else:
                        self.botao_musica = self.__criar_botao_musica("Ativar Música")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()
