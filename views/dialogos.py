# views/dialogos.py — versão universal para qualquer Arcade antigo
import json
import arcade
import traceback
from pathlib import Path
from typing import List, Dict, Optional
from core.utils import safe_load_texture

DIALOGOS_DIR = Path("dialogos")
ASSETS_BG_DIR = Path("assets") / "bg"
ASSETS_SPRITES_DIR = Path("assets") / "sprites"


class TelaDialogos(arcade.View):
    def __init__(
        self,
        largura: int = 800,
        altura: int = 600,
        arquivo_json: str = "cena_exemplo.json",
        font_name: str = "Arial"
    ):
        super().__init__()
        self.largura = largura
        self.altura = altura
        self.font_name = font_name

        self.roteiro: List[Dict] = self._carregar_roteiro(arquivo_json)
        self.index = 0

        self.bg_texture = None
        self.sprite_texture = None

        self.texto_atual = ""
        self.personagem_atual = ""

        # Caixa
        self.box_margin = 24
        self.box_height = int(self.altura * 0.28)
        self.box_width = self.largura - 2 * self.box_margin
        self.box_padding = 16
        self.name_area_height = 32

        self.box_left = self.box_margin
        self.box_bottom = self.box_margin
        self.box_top = self.box_bottom + self.box_height

        self.name_text = arcade.Text(
            "",
            self.box_left + self.box_padding,
            self.box_top - self.box_padding,
            arcade.color.WHITE,
            18,
            anchor_y="top",
            font_name=self.font_name
        )

        self.dialog_text = arcade.Text(
            "",
            self.box_left + self.box_padding,
            self.box_top - self.box_padding - self.name_area_height,
            arcade.color.WHITE,
            16,
            width=self.box_width - 2 * self.box_padding,
            align="left",
            multiline=True,
            anchor_y="top",
            font_name=self.font_name
        )

        if self.roteiro:
            self._aplicar_fala(self.roteiro[0])

    def _carregar_roteiro(self, arquivo_json: str):
        caminho = DIALOGOS_DIR / arquivo_json
        if not caminho.exists():
            print("[Dialogos] JSON não encontrado:", caminho)
            return []
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            traceback.print_exc()
            return []

    def _aplicar_fala(self, fala_obj: Dict):
        try:
            self.personagem_atual = fala_obj.get("personagem", "")
            self.texto_atual = fala_obj.get("fala", "")

            self.name_text.text = self.personagem_atual
            self.dialog_text.text = self.texto_atual

            # BG
            bg = fala_obj.get("bg")
            if bg:
                path = ASSETS_BG_DIR / bg
                if path.exists():
                    self.bg_texture = safe_load_texture(str(path))
                else:
                    print("[Dialogos] BG não encontrado:", path)
                    self.bg_texture = None
            else:
                self.bg_texture = None

            # SPRITE
            sp = fala_obj.get("sprite")
            if sp:
                path = ASSETS_SPRITES_DIR / sp
                if path.exists():
                    self.sprite_texture = safe_load_texture(str(path))
                else:
                    print("[Dialogos] Sprite não encontrado:", path)
                    self.sprite_texture = None
            else:
                self.sprite_texture = None

        except Exception:
            traceback.print_exc()

    # ------------------------------------------------------------------
    # FUNÇÃO DE DESENHO DO FUNDO — usando apenas draw_line
    # ------------------------------------------------------------------
    def _draw_bg(self):
        if self.bg_texture:
            try:
                # Desenhar textura manualmente (super antigo e simples)
                texture = self.bg_texture
                w = texture.width
                h = texture.height
                scale_x = self.largura / w
                scale_y = self.altura / h
                sx = min(scale_x, scale_y)

                arcade.draw_scaled_texture_rectangle(
                    self.largura // 2,
                    self.altura // 2,
                    texture,
                    sx
                )
                return
            except:
                pass

        # fallback: fundo preto
        for y in range(0, self.altura, 4):
            arcade.draw_line(0, y, self.largura, y, arcade.color.BLACK, 4)

    # ------------------------------------------------------------------
    # DESENHA A CAIXA DO DIÁLOGO — usando apenas draw_line
    # ------------------------------------------------------------------
    def _draw_dialog_box(self):
        left = self.box_left
        right = self.box_left + self.box_width
        top = self.box_top
        bottom = self.box_bottom

        # preenchimento semi-transparente
        for y in range(int(bottom), int(top), 4):
            arcade.draw_line(left, y, right, y, (0, 0, 0, 180), 4)

        # contorno
        arcade.draw_line(left, bottom, right, bottom, arcade.color.WHITE, 2)
        arcade.draw_line(left, top, right, top, arcade.color.WHITE, 2)
        arcade.draw_line(left, bottom, left, top, arcade.color.WHITE, 2)
        arcade.draw_line(right, bottom, right, top, arcade.color.WHITE, 2)

    # ------------------------------------------------------------------
    # DESENHA SPRITE — usando scaled_texture_rectangle (super antigo)
    # ------------------------------------------------------------------
    def _draw_sprite(self):
        if not self.sprite_texture:
            return

        try:
            tex = self.sprite_texture
            w = tex.width
            h = tex.height
            scale = min(1.0, (self.largura * 0.45) / w)
            draw_h = int(h * scale)
            y = int(self.box_top + draw_h * 0.35)

            arcade.draw_scaled_texture_rectangle(
                self.largura // 2,
                y,
                tex,
                scale
            )
        except Exception:
            traceback.print_exc()

    # ------------------------------------------------------------------
    def on_draw(self):
        self.clear()

        self._draw_bg()
        self._draw_dialog_box()
        self._draw_sprite()

        if self.personagem_atual:
            self.name_text.draw()

        self.dialog_text.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        self.index += 1
        if self.index < len(self.roteiro):
            self._aplicar_fala(self.roteiro[self.index])
        else:
            if hasattr(self.window, "menu_view"):
                self.window.show_view(self.window.menu_view)
