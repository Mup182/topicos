# views/dialogos.py — compatível com Arcade 2.6.x
import json
import arcade
import traceback
from pathlib import Path
from typing import List, Dict, Optional

DIALOGOS_DIR = Path("dialogos")
ASSETS_BG_DIR = Path("assets") / "bg"
ASSETS_SPRITES_DIR = Path("assets") / "sprites"


class TelaDialogos(arcade.View):
    def __init__(
        self,
        largura: int = 800,
        altura: int = 600,
        arquivo_json: str = "cena_exemplo.json",
        font_name: str = "Arial",
    ):
        super().__init__()
        # valores iniciais (serão atualizados em on_show/on_draw)
        self.largura = largura
        self.altura = altura
        self.font_name = font_name

        # roteiro
        self.roteiro: List[Dict] = self._carregar_roteiro(arquivo_json)
        self.index = 0

        # sprites (Sprite ou None)
        self.bg_sprite: Optional[arcade.Sprite] = None
        self.char_sprite: Optional[arcade.Sprite] = None

        # conteúdo atual
        self.personagem_atual = ""
        self.texto_atual = ""

        # layout da caixa de diálogo (valores base — largura da área de texto será ajustada se houver sprite)
        self.box_margin = 24
        self.box_height = int(self.altura * 0.28)
        self.box_padding = 16
        self.name_area_height = 32

        # serão calculados em on_show / on_draw
        self.box_left = self.box_margin
        self.box_bottom = self.box_margin
        self.box_top = self.box_bottom + self.box_height
        self.box_width = max(100, self.largura - 2 * self.box_margin)

        # objetos arcade.Text (definidos com largura provisória; atualizaremos dinamicamente)
        self.name_text = arcade.Text(
            "",
            self.box_left + self.box_padding,
            0,  # y definido dinamicamente
            arcade.color.WHITE,
            18,
            anchor_y="top",
            font_name=self.font_name,
        )

        self.dialog_text = arcade.Text(
            "",
            self.box_left + self.box_padding,
            0,  # y definido dinamicamente
            arcade.color.WHITE,
            16,
            width=self.box_width - 2 * self.box_padding,
            align="left",
            multiline=True,
            anchor_y="top",
            font_name=self.font_name,
        )

        # aplica a primeira fala (se houver)
        if self.roteiro:
            try:
                self._aplicar_fala(self.roteiro[0])
            except Exception:
                traceback.print_exc()

    # ------------------------------
    def on_show(self):
        # atualiza valores com a janela real quando a view é mostrada
        try:
            self.largura = int(self.window.width)
            self.altura = int(self.window.height)
        except Exception:
            # fallback para valores já existentes
            pass

        # recalcula box e textos
        self._recalc_layout()

        # reescalona background e personagem (caso já tenham sido carregados)
        if self.bg_sprite:
            self._rescale_bg()
        if self.char_sprite:
            self._rescale_char()

    def on_resize(self, width, height):
        # manter tudo em sincronia se a janela for redimensionada
        self.largura = int(width)
        self.altura = int(height)
        self._recalc_layout()
        if self.bg_sprite:
            self._rescale_bg()
        if self.char_sprite:
            self._rescale_char()

    # ------------------------------
    def _carregar_roteiro(self, arquivo_json: str) -> List[Dict]:
        caminho = DIALOGOS_DIR / arquivo_json
        if not caminho.exists():
            print(f"[TelaDialogos] JSON não encontrado: {caminho}")
            return []
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                print("[TelaDialogos] Formato inválido: JSON deve ser uma lista de falas.")
                return []
            return data
        except Exception:
            traceback.print_exc()
            return []

    # ------------------------------
    def _criar_sprite_bg(self, path: Path) -> Optional[arcade.Sprite]:
        try:
            sprite = arcade.Sprite(str(path), scale=1.0)
            sprite.center_x = self.largura // 2
            sprite.center_y = self.altura // 2
            # escala em _rescale_bg
            self.bg_sprite = sprite
            self._rescale_bg()
            return sprite
        except Exception:
            traceback.print_exc()
            return None

    def _rescale_bg(self):
        # garante que o background cubra a tela mantendo aspecto
        try:
            tex = self.bg_sprite.texture
            if not tex:
                return
            sx = self.largura / tex.width
            sy = self.altura / tex.height
            # usamos max para cobrir toda a tela (preencher) — irá cortar ao manter proporção
            scale = max(sx, sy)
            self.bg_sprite.scale = scale
            self.bg_sprite.center_x = self.largura // 2
            self.bg_sprite.center_y = self.altura // 2
        except Exception:
            traceback.print_exc()

    # ------------------------------
    def _criar_sprite_char(self, path: Path) -> Optional[arcade.Sprite]:
        try:
            sprite = arcade.Sprite(str(path), scale=1.0)
            self.char_sprite = sprite
            self._rescale_char()
            return sprite
        except Exception:
            traceback.print_exc()
            return None

    def _rescale_char(self):
        try:
           if not self.char_sprite or not self.char_sprite.texture:
              return

           tex = self.char_sprite.texture

        # sprite ocupa cerca de 22% da largura da tela
           target_w = int(self.largura * 0.22)
           scale = target_w / tex.width
           self.char_sprite.scale = scale

        # posição: EXACTAMENTE ao lado direito da caixa de diálogo
           margin = 20

           self.char_sprite.center_x = self.box_left + self.box_width + margin + (self.char_sprite.width // 2)
           self.char_sprite.center_y = self.box_bottom + (self.box_height // 2)

        except Exception:
            traceback.print_exc()

    # ------------------------------
    def _aplicar_fala(self, fala_obj: Dict):
        try:
            self.personagem_atual = fala_obj.get("personagem", "") or ""
            self.texto_atual = fala_obj.get("fala", "") or ""

            # atualiza textos
            self.name_text.text = self.personagem_atual
            self.dialog_text.text = self.texto_atual

            # BACKGROUND (carrega sprite e escala)
            bg_name = fala_obj.get("bg")
            if bg_name:
                bg_path = ASSETS_BG_DIR / bg_name
                if bg_path.exists():
                    self.bg_sprite = self._criar_sprite_bg(bg_path)
                else:
                    print(f"[TelaDialogos] BG não encontrado: {bg_path}")
                    self.bg_sprite = None
            else:
                self.bg_sprite = None

            # SPRITE DO PERSONAGEM (carrega e posiciona)
            sprite_name = fala_obj.get("sprite")
            if sprite_name:
                sp_path = ASSETS_SPRITES_DIR / sprite_name
                if sp_path.exists():
                    self.char_sprite = self._criar_sprite_char(sp_path)
                else:
                    print(f"[TelaDialogos] Sprite não encontrado: {sp_path}")
                    self.char_sprite = None
            else:
                self.char_sprite = None

            # recalcula layout (usa o sprite atual para ajustar largura do texto)
            self._recalc_layout()
        except Exception:
            traceback.print_exc()

    # ------------------------------
    def _recalc_layout(self):
        try:
          self.box_bottom = self.box_margin
          self.box_top = self.box_bottom + int(self.altura * 0.28)

        # reserva espaço à direita somente se houver sprite
          reserved_right = 0
          if self.char_sprite:
            tex = self.char_sprite.texture
            if tex:
                reserved_right = int(self.largura * 0.25)  # mais seguro, garante espaço

        # caixa reduzida para caber sprite ao lado
          self.box_width = max(200, self.largura - 2 * self.box_margin - reserved_right)

        # texto acompanha nova largura
          self.dialog_text.width = self.box_width - 2 * self.box_padding

        # reposiciona textos
          self.name_text.x = self.box_left + self.box_padding
          self.name_text.y = self.box_top - self.box_padding

          self.dialog_text.x = self.name_text.x
          self.dialog_text.y = self.name_text.y - self.name_area_height

        except Exception:
         traceback.print_exc()


    # ------------------------------
    def _draw_dialog_box(self):
        l = self.box_left
        r = self.box_left + self.box_width
        b = self.box_bottom
        t = self.box_top

        # preenchimento semi-transparente (linhas horizontais)
        for y in range(int(b), int(t), 4):
            arcade.draw_line(l, y, r, y, (0, 0, 0, 180), 4)

        # contorno
        arcade.draw_line(l, b, r, b, arcade.color.WHITE, 2)
        arcade.draw_line(l, t, r, t, arcade.color.WHITE, 2)
        arcade.draw_line(l, b, l, t, arcade.color.WHITE, 2)
        arcade.draw_line(r, b, r, t, arcade.color.WHITE, 2)

    # ------------------------------
    def on_draw(self):
        # atualiza tamanho (útil em fullscreen / after show)
        try:
            self.largura = int(self.window.width)
            self.altura = int(self.window.height)
        except Exception:
            pass

        # recalcula layout e reescalona sprites antes de desenhar
        self._recalc_layout()
        if self.bg_sprite:
            self._rescale_bg()
        if self.char_sprite:
            self._rescale_char()

        self.clear()

        # desenha background (preenchendo a tela)
        if self.bg_sprite:
            try:
                self.bg_sprite.draw()
            except Exception:
                # fallback defensivo: se Sprite.draw falhar, desenhar textura manualmente
                try:
                    tex = self.bg_sprite.texture
                    arcade.draw_texture_rect(tex, 0, 0, self.largura, self.altura, 0)  # alguns ambientes têm essa função
                except Exception:
                    # último recurso: preencher com retângulo/linhas
                    for y in range(0, self.altura, 4):
                        arcade.draw_line(0, y, self.largura, y, arcade.color.BLACK, 4)

        # desenha sprite do personagem (à direita)
        if self.char_sprite:
            try:
                self.char_sprite.draw()
            except Exception:
                # fallback: tentar desenhar a textura diretamente (se disponível)
                try:
                    tex = self.char_sprite.texture
                    cx = int(self.char_sprite.center_x)
                    cy = int(self.char_sprite.center_y)
                    w = int(self.char_sprite.width)
                    h = int(self.char_sprite.height)
                    arcade.draw_texture_rect(tex, cx - w // 2, cy - h // 2, w, h, 0)
                except Exception:
                    pass

        # desenha caixa + textos
        self._draw_dialog_box()

        if self.personagem_atual:
            try:
                self.name_text.draw()
            except Exception:
                pass

        try:
            self.dialog_text.draw()
        except Exception:
            pass

    # ------------------------------
    def on_mouse_press(self, x, y, button, modifiers):
        self.index += 1
        if self.index < len(self.roteiro):
            try:
                self._aplicar_fala(self.roteiro[self.index])
            except Exception:
                traceback.print_exc()
        else:
            if hasattr(self.window, "menu_view"):
                self.window.show_view(self.window.menu_view)

    # volta ao menu com ESC
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            if hasattr(self.window, "menu_view"):
                self.window.show_view(self.window.menu_view)
