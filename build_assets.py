#!/usr/bin/env python3
"""
build_assets.py — Regera assets/ a partir do material entregue em `_originais/`.

`_originais/` (fora do git) guarda o material como veio da incorporadora:
imagens/ (renders 1080 px), plantas/ (PNG com transparência), design/ (logo +
bg em SVG animado). O de-para render -> nome final fica em `assets-map.tsv`
(TAB entre as colunas).

  assets/<destino>.webp              imagem do lightbox  (lado maior <= 2600 px, q80)
  assets/miniaturas/<destino>.webp   miniatura da grade  (lado maior <=  900 px, q72)

Plantas: os PNGs já vêm com transparência. O desenho é assentado sobre BRANCO
(o card de planta é branco), recortado na própria caixa (ignorando pontos
soltos) e com margem branca em volta. Plantas: lightbox <= 3000 px q86, grade
<= 1400 px q78. Nenhuma imagem é ampliada além do tamanho entregue.

Uso:
    python build_assets.py            # gera só o que falta
    python build_assets.py --force    # regera tudo
    python build_assets.py --brand    # regera logo + fundo (SVG) em assets/brand/

Requisito: Pillow (pip install pillow), com suporte a WebP.
"""
import argparse
import re
import sys
import unicodedata
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
SRC = ROOT / '_originais'
OUT = ROOT / 'assets'

FULL_W, FULL_Q = 2600, 80
THUMB_W, THUMB_Q = 900, 72
PLAN_FULL_W, PLAN_FULL_Q = 3000, 86
PLAN_THUMB_W, PLAN_THUMB_Q = 1400, 78

# viewBox do logo encostado no desenho (o quadro original é 600 x 600 com muita sobra);
# medido no quadro final da animação: x, y, largura, altura
LOGO_VIEWBOX = (23, 64, 554, 473)


def nfc(s):
    return unicodedata.normalize('NFC', s)


def find(rel):
    """Acha o arquivo em _originais/ tolerando acentos NFC/NFD (macOS x Windows)."""
    p = SRC
    for part in Path(rel).parts:
        hit = next((c for c in p.iterdir() if nfc(c.name) == nfc(part)), None)
        if hit is None:
            return None
        p = hit
    return p


def fresh(src, dst, force):
    return not force and dst.exists() and dst.stat().st_mtime > src.stat().st_mtime


def save_webp(im, path, max_side, quality):
    path.parent.mkdir(parents=True, exist_ok=True)
    im = im.copy()
    im.thumbnail((max_side, max_side), Image.LANCZOS)  # só reduz
    im.save(path, 'WEBP', quality=quality, method=6)


def clean_plan(path):
    """PNG transparente -> RGB sobre branco, recortado no desenho + margem."""
    im = Image.open(path).convert('RGBA')
    alpha = im.getchannel('A')
    # Pontos soltos (poeira do export) não podem esticar a caixa: mede em 1/8 da
    # resolução, onde um ponto vira quase transparente.
    k = 8
    small = alpha.point(lambda v: 255 if v > 40 else 0).resize(
        (max(1, im.width // k), max(1, im.height // k)), Image.BOX)
    box = small.point(lambda v: 255 if v > 60 else 0).getbbox()
    x0, y0, x1, y1 = (box[0] * k, box[1] * k, min(im.width, box[2] * k), min(im.height, box[3] * k))
    white = Image.new('RGBA', im.size, (255, 255, 255, 255))
    white.alpha_composite(im)
    drawing = white.convert('RGB').crop((x0, y0, x1, y1))
    pad = int(max(drawing.size) * 0.035)
    canvas = Image.new('RGB', (drawing.width + 2 * pad, drawing.height + 2 * pad), 'white')
    canvas.paste(drawing, (pad, pad))
    return canvas


def build_images(force):
    done = skip = 0
    for line in (ROOT / 'assets-map.tsv').read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        rel, dst = line.split('\t')
        src = find(rel)
        if src is None:
            print(f'  falta: {rel}', file=sys.stderr)
            continue
        full = OUT / f'{dst}.webp'
        thumb = OUT / 'miniaturas' / f'{dst}.webp'
        if fresh(src, full, force) and fresh(src, thumb, force):
            skip += 1
            continue
        if dst.startswith('plantas/'):
            im = clean_plan(src)
            save_webp(im, full, PLAN_FULL_W, PLAN_FULL_Q)
            save_webp(im, thumb, PLAN_THUMB_W, PLAN_THUMB_Q)
        else:
            im = Image.open(src).convert('RGB')
            save_webp(im, full, FULL_W, FULL_Q)
            save_webp(im, thumb, THUMB_W, THUMB_Q)
        done += 1
        print(f'  {dst}')
    print(f'Imagens: {done} geradas, {skip} já atualizadas.')


# ── MARCA ──────────────────────────────────────────────────────────
# Os SVGs do design vêm com as animações em `infinite`: o logo se reescreveria
# a cada 8 s e o monograma do fundo piscaria a cada 2 s. Aqui viram `1 both` —
# tocam UMA vez e congelam no quadro final. No logo o estado-base (sem
# animação) fica desmontado: por isso o reduced-motion NÃO desliga a animação,
# só a reduz a ~0 ms (pula direto para o quadro final).
def build_brand():
    once = re.compile(r'(\d+(?:\.\d+)?s linear) infinite')
    reduced = ('@media (prefers-reduced-motion: reduce) { * { animation-duration: 0.001ms !important; '
               'animation-delay: 0s !important; } }')
    (OUT / 'brand').mkdir(parents=True, exist_ok=True)

    logo = once.sub(r'\1 1 both', (SRC / 'design' / 'logo-torres.svg').read_text(encoding='utf-8'))
    if LOGO_VIEWBOX:
        x, y, w, h = LOGO_VIEWBOX
        logo = logo.replace('width="600" height="600" viewBox="0 0 600 600"',
                            f'width="{w}" height="{h}" viewBox="{x} {y} {w} {h}"')
    logo = logo.replace('</style>', reduced + '\n</style>')
    (OUT / 'brand' / 'logo.svg').write_text(logo, encoding='utf-8', newline='\n')

    bg = once.sub(r'\1 1 both', (SRC / 'design' / 'bg-torres.svg').read_text(encoding='utf-8'))
    bg = bg.replace('</style>', reduced + '\n</style>')
    (OUT / 'brand' / 'bg.svg').write_text(bg, encoding='utf-8', newline='\n')
    print('Marca regerada (assets/brand/logo.svg, bg.svg).')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--brand', action='store_true')
    a = ap.parse_args()
    if not SRC.is_dir():
        sys.exit(f"ERRO: pasta '{SRC.name}' não encontrada (material original).")
    build_images(a.force)
    if a.brand:
        build_brand()
