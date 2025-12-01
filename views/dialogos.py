# views/dialogos.py — compatível com Arcade 2.6.x, com suporte a "escolha"
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
        self.largura = largura
        self.altura = altura
        self.font_name = font_name

        # roteiro mestre
        self.master_roteiro: List[Dict] = self._carregar_roteiro(arquivo_json)
        self.index = 0

        # sprites
        self.bg_sprite: Optional[arcade.Sprite] = None
        self.char_sprites: List[arcade.Sprite] = []  # ← corrigido

        # escolha
        self.waiting_choice = False
        self.current_choice = None
        self.choice_buttons = []

        # conteúdo atual
        self.personagem_atual = ""
        self.texto_atual = ""

        # layout
        self.box_margin = 24
        self.box_height = int(self.altura * 0.28)
        self.box_padding = 16
        self.name_area_height = 32

        self.box_left = self.box_margin
        self.box_bottom = self.box_margin
        self.box_top = self.box_bottom + self.box_height
        self.box_width = max(100, self.largura - 2 * self.box_margin)

        self.name_text = arcade.Text(
            "",
            self.box_left + self.box_padding,
            0,
            arcade.color.WHITE,
            18,
            anchor_y="top",
            font_name=self.font_name,
        )

        self.dialog_text = arcade.Text(
            "",
            self.box_left + self.box_padding,
            0,
            arcade.color.WHITE,
            16,
            width=self.box_width - 2 * self.box_padding,
            align="left",
            multiline=True,
            anchor_y="top",
            font_name=self.font_name,
        )

        # aplica 1ª fala
        if self.master_roteiro:
            try:
                self._aplicar_item(self.master_roteiro[0])
            except Exception:
                traceback.print_exc()

    # ----------------------------------------------------------------------
    def _carregar_roteiro(self, arquivo_json: str) -> List[Dict]:
        caminho = DIALOGOS_DIR / arquivo_json
        if not caminho.exists():
            print(f"[TelaDialogos] JSON não encontrado: {caminho}")
            return []
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                print("[TelaDialogos] JSON deve ser uma lista.")
                return []
            return data
        except Exception:
            traceback.print_exc()
            return []

    # ----------------------------------------------------------------------
    def _criar_sprite_bg(self, path: Path):
        try:
            sp = arcade.Sprite(str(path), scale=1.0)
            sp.center_x = self.largura // 2
            sp.center_y = self.altura // 2
            self.bg_sprite = sp
            self._rescale_bg()
        except:
            traceback.print_exc()

    def _rescale_bg(self):
        try:
            tex = self.bg_sprite.texture
            sx = self.largura / tex.width
            sy = self.altura / tex.height
            self.bg_sprite.scale = max(sx, sy)
        except:
            traceback.print_exc()

    # ----------------------------------------------------------------------
    def _criar_sprite_char(self, filename: str):
        """Cria sprite SEM posicionar ainda."""
        try:
            p = ASSETS_SPRITES_DIR / filename
            sp = arcade.Sprite(str(p), scale=1.0)
            sp.filename_lower = filename.lower()  # nova referência
            return sp
        except:
            traceback.print_exc()
            return None

    # ----------------------------------------------------------------------
    def _posicionar_char_sprites(self):
        """Posiciona todos os sprites simultaneamente."""
        try:
            right_margin = 20

            for sp in self.char_sprites:
                fname = sp.filename_lower

                # PEDRO (centro superior)
                if "pedro" in fname:
                    target_w = int(self.largura * 0.47)
                    scale = target_w / sp.texture.width
                    sp.scale = scale
                    sp.center_x = self.largura // 2
                    sp.center_y = int(self.box_top + sp.height * 0.10)
                    continue

                # MARCOS (direita)
                if "marcos" in fname:
                    target_w = int(self.largura * 0.22)
                    scale = target_w / sp.texture.width
                    sp.scale = scale
                    box_right = self.box_left + self.box_width
                    sp.center_x = box_right + right_margin + sp.width / 2
                    sp.center_y = self.box_bottom + self.box_height / 2
                    continue

                sp.center_x = self.largura - 150
                sp.center_y = self.altura // 2

        except:
            traceback.print_exc()

    # ----------------------------------------------------------------------
    def _aplicar_item(self, item: Dict):

        # escolha
        if item.get("tipo") == "escolha":
            self.waiting_choice = True
            self.current_choice = item
            self._prepare_choice_buttons(item)
            return

        # fala normal
        self.waiting_choice = False
        self.current_choice = None
        self.choice_buttons = []

        self.personagem_atual = item.get("personagem", "")
        self.texto_atual = item.get("fala", "")

        # background
        bg = item.get("bg")
        if bg:
            p = ASSETS_BG_DIR / bg
            if p.exists():
                self._criar_sprite_bg(p)
            else:
                self.bg_sprite = None
        else:
            self.bg_sprite = None

        # sprites
        self.char_sprites = []
        spr = item.get("sprite")

        if isinstance(spr, list):
            for s in spr:
                if not s:
                    continue
                sp = self._criar_sprite_char(s)
                if sp:
                    self.char_sprites.append(sp)

        elif isinstance(spr, str):
            sp = self._criar_sprite_char(spr)
            if sp:
                self.char_sprites.append(sp)

        self._recalc_layout()
        self._posicionar_char_sprites()

        self.name_text.text = self.personagem_atual
        self.dialog_text.text = self.texto_atual

    # ----------------------------------------------------------------------
    def _prepare_choice_buttons(self, item: Dict):
        opcs = item.get("opcoes", [])
        self.choice_buttons = []
        btn_w = int(self.largura * 0.28)
        btn_h = 48
        gap = 24
        total_w = len(opcs) * btn_w + (len(opcs) - 1) * gap
        start_x = (self.largura - total_w) // 2
        y = int(self.altura * 0.45)

        for i, o in enumerate(opcs):
            x1 = start_x + i * (btn_w + gap)
            x2 = x1 + btn_w
            y2 = y + btn_h
            self.choice_buttons.append((x1, y, x2, y2, o["texto"], o["key"]))

    # ----------------------------------------------------------------------
    def _recalc_layout(self):
        self.box_bottom = self.box_margin
        self.box_top = self.box_bottom + int(self.altura * 0.28)

        reserved_right = 0
        for sp in self.char_sprites:
            if "marcos" in sp.filename_lower:
                reserved_right = int(self.largura * 0.25)

        self.box_width = max(200, self.largura - 2 * self.box_margin - reserved_right)
        self.dialog_text.width = self.box_width - 2 * self.box_padding
        self.name_text.x = self.box_left + self.box_padding
        self.name_text.y = self.box_top - self.box_padding
        self.dialog_text.x = self.name_text.x
        self.dialog_text.y = self.name_text.y - self.name_area_height

    # ----------------------------------------------------------------------
    def _draw_dialog_box(self):
        l = self.box_left
        r = l + self.box_width
        b = self.box_bottom
        t = self.box_top

        for y in range(int(b), int(t), 4):
            arcade.draw_line(l, y, r, y, (0, 0, 0, 180), 4)

        arcade.draw_rectangle_outline(
            (l + r) / 2, (b + t) / 2,
            self.box_width, self.box_height,
            arcade.color.WHITE, 2
        )

    # ----------------------------------------------------------------------
    def on_draw(self):
        try:
            self.largura = int(self.window.width)
            self.altura = int(self.window.height)
        except:
            pass

        self._recalc_layout()
        if self.bg_sprite:
            self._rescale_bg()
        self._posicionar_char_sprites()

        self.clear()

        if self.bg_sprite:
            self.bg_sprite.draw()

        # desenha sprites
        for sp in self.char_sprites:
            sp.draw()

        # ================================
        #       CAIXAS DE ESCOLHA
        # ================================
        if self.waiting_choice and self.current_choice:
            for (x1, y1, x2, y2, label, key) in self.choice_buttons:

                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                w = x2 - x1
                h = y2 - y1

                # fundo escuro
                arcade.draw_rectangle_filled(cx, cy, w, h, (0, 0, 0, 200))

                # borda clara
                arcade.draw_rectangle_outline(cx, cy, w, h, arcade.color.WHITE, 3)

                # texto
                arcade.draw_text(
                    label,
                    cx, cy,
                    arcade.color.WHITE,
                    18,
                    anchor_x="center",
                    anchor_y="center",
                )
            return

        # caixa de diálogo
        self._draw_dialog_box()
        if self.personagem_atual:
            self.name_text.draw()
        self.dialog_text.draw()

    # ----------------------------------------------------------------------
    def on_mouse_press(self, x, y, button, modifiers):

        if self.waiting_choice and self.current_choice:
            for (x1, y1, x2, y2, label, key) in self.choice_buttons:
                if x1 <= x <= x2 and y1 <= y <= y2:
                    self._handle_choice_selection(key)
                    return
            return

        self.index += 1
        while self.index < len(self.master_roteiro) and self.master_roteiro[self.index].get("tipo") == "meta_skip":
            self.index += 1

        if self.index < len(self.master_roteiro):
            self._aplicar_item(self.master_roteiro[self.index])
        else:
            if hasattr(self.window, "menu_view"):
                self.window.show_view(self.window.menu_view)

    # ----------------------------------------------------------------------
    def _handle_choice_selection(self, key: str):
        for i, item in enumerate(self.master_roteiro):
            if item.get("caminho") == key:
                self.index = i
                self.waiting_choice = False
                self.current_choice = None
                self.choice_buttons = []
                self._aplicar_item(self.master_roteiro[i])
                return

        # fallback
        self.waiting_choice = False
        self.index += 1
        if self.index < len(self.master_roteiro):
            self._aplicar_item(self.master_roteiro[self.index])
        else:
            if hasattr(self.window, "menu_view"):
                self.window.show_view(self.window.menu_view)

    # ----------------------------------------------------------------------
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            if hasattr(self.window, "menu_view"):
                self.window.show_view(self.window.menu_view)
