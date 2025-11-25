# views/dialogos.py — compatível 100% com Arcade 2.6.17

import json
import arcade
import traceback
from pathlib import Path
from typing import List, Dict
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

        self.bg_sprite = None
        self.char_sprite = None

        self.personagem_atual = ""
        self.texto_atual = ""

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
        try:
            with open(DIALOGOS_DIR / arquivo_json, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            traceback.print_exc()
            return []

    def _criar_sprite_bg(self, path: Path):
        try:
            sprite = arcade.Sprite(str(path), scale=1.0)
            sprite.center_x = self.largura // 2
            sprite.center_y = self.altura // 2

            sx = self.largura / sprite.texture.width
            sy = self.altura / sprite.texture.height
            sprite.scale = min(sx, sy)

            return sprite
        except:
            traceback.print_exc()
            return None

    def _criar_sprite_char(self, path: Path):
        try:
            sprite = arcade.Sprite(str(path), scale=1.0)

            # novo cálculo: garante que nunca sai da tela
            base_width = self.largura * 0.30
            scale = base_width / sprite.texture.width
            sprite.scale = scale

            sprite.center_x = int(self.largura * 0.82)
            sprite.center_y = int(self.box_top + sprite.height * 0.45)

            return sprite
        except:
            traceback.print_exc()
            return None

    def _aplicar_fala(self, fala_obj: Dict):
        try:
            self.personagem_atual = fala_obj.get("personagem", "")
            self.texto_atual = fala_obj.get("fala", "")

            self.name_text.text = self.personagem_atual
            self.dialog_text.text = self.texto_atual

            # Fundo
            bg = fala_obj.get("bg")
            if bg:
                p = ASSETS_BG_DIR / bg
                self.bg_sprite = self._criar_sprite_bg(p) if p.exists() else None

            # Sprite do personagem
            sp = fala_obj.get("sprite")
            if sp:
                p = ASSETS_SPRITES_DIR / sp
                self.char_sprite = self._criar_sprite_char(p) if p.exists() else None
            else:
                self.char_sprite = None

        except:
            traceback.print_exc()

    def _draw_dialog_box(self):
        l, r = self.box_left, self.box_left + self.box_width
        b, t = self.box_bottom, self.box_top

        for y in range(int(b), int(t), 4):
            arcade.draw_line(l, y, r, y, (0, 0, 0, 180), 4)

        arcade.draw_line(l, b, r, b, arcade.color.WHITE, 2)
        arcade.draw_line(l, t, r, t, arcade.color.WHITE, 2)
        arcade.draw_line(l, b, l, t, arcade.color.WHITE, 2)
        arcade.draw_line(r, b, r, t, arcade.color.WHITE, 2)

    def on_draw(self):
        self.clear()

        if self.bg_sprite:
            self.bg_sprite.draw()

        if self.char_sprite:
            self.char_sprite.draw()

        self._draw_dialog_box()

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
