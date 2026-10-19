# Galeria — José Torres Sobrinho (Saraiva de Rezende)

Galeria de imagens/plantas (+ player de vídeo) para injeção via script no 3DVista, hospedada no AWS S3.

**Empreendimento:** Edifício José Torres Sobrinho
**Incorporadora:** Grupo Saraiva de Rezende
**Tema:** marrom + pêssego/creme (`#542E1E` / `#F7B581` · `#FFEAD9`, detalhe cobre `#CD8859`)

---

## URLs de produção

| Arquivo | URL |
|---------|-----|
| Galeria | `https://skylineip.s3.sa-east-1.amazonaws.com/Tour+Virtual/saraiva-rezende/torres/ferramentas/index.html` |
| Vídeo   | `https://skylineip.s3.sa-east-1.amazonaws.com/Tour+Virtual/saraiva-rezende/torres/ferramentas/video-gallery.html` |
| Script  | `https://skylineip.s3.sa-east-1.amazonaws.com/Tour+Virtual/saraiva-rezende/torres/ferramentas/inject.js` |

**S3 path:** `s3://skylineip/Tour Virtual/saraiva-rezende/torres/ferramentas/`

---

## Estrutura de arquivos

```
ferramentas/
├── index.html            ← galeria de imagens + plantas (?mode=imagens | plantas)
├── video-gallery.html    ← player do vídeo
├── inject.js             ← loader leve para injeção no 3DVista
├── deploy.ps1            ← deploy para o S3 (Windows)
├── build_assets.py       ← regera assets/ a partir de _originais/ (Pillow)
├── assets-map.tsv        ← arquivo entregue → nome final (fonte do build)
├── _originais/           ← material entregue, FORA do git e do deploy
│   ├── imagens/  plantas/  design/
└── assets/
    ├── brand/            ← logo.svg + bg.svg (do design, animação tocando uma vez)
    ├── fachada/          ← torre (03) + acesso (02)
    ├── areas-comuns/     ← 17 imagens, uma sub-categoria por ambiente
    ├── apartamento/      ← decorado: 12 (1 suíte + 1 quarto) + 18 (1 suíte + 2 quartos)
    ├── plantas/          ← 2 tipologias + pavimento tipo, fundo branco
    ├── miniaturas/       ← espelha fachada/, areas-comuns/, apartamento/ e plantas/ (grade)
    └── video/            ← vídeo 1080p (gitignored; ainda não entregue)
```

> Pastas e arquivos publicados: **minúsculos, sem espaços e sem acentos** (o S3 é
> case-sensitive). Os nomes de exibição, com acentuação, ficam em `GALLERY_CONFIG`
> no `index.html`.

---

## Categorias

| Categoria | Sub-categorias |
|-----------|----------------|
| Fachada | — (Fachada × 3 · Acesso × 2) |
| Áreas Comuns | Salão de Festas · Brinquedoteca · Coworking · Espaço Pet |
| Apartamento Decorado | 1 Suíte + 1 Quarto · 1 Suíte + 2 Quartos |
| Plantas | Tipologias (1 suíte + 1 quarto / 1 suíte + 2 quartos) · Pavimento Tipo |

---

## Assets — do material entregue ao WebP

| Uso | Tamanho | Qualidade |
|-----|---------|-----------|
| Lightbox | lado maior ≤ 2600 px (plantas ≤ 3000 px) | q80 (plantas q86) |
| Grade (`miniaturas/`) | lado maior ≤ 900 px (plantas ≤ 1400 px) | q72 (plantas q78) |

Os renders chegaram em 1080 px de altura: o build **só reduz**, nunca amplia.

**Plantas:** os PNGs já vêm com transparência; o build assenta o desenho sobre
branco e recorta na própria caixa (pontos soltos do export são ignorados).

**Fachada:** a pasta entregue tinha duas versões das 5 imagens (`Jose…` e
`José…`). Está em uso a versão com acento, que é a revisão (paisagismo e
iluminação ajustados); a antiga ficou em `_originais/imagens/fachada-versao-antiga/`.

**Marca:** os SVGs do design vêm com as animações em `infinite`; o build troca para
`1 both` (tocam uma vez e congelam no quadro final) e encosta o viewBox do logo no
desenho (`23 64 554 473`). No logo o estado-base (sem animação) fica desmontado,
então `prefers-reduced-motion` só encurta a animação para ~0 ms em vez de
desligá-la.

```powershell
python build_assets.py            # só o que falta
python build_assets.py --force    # tudo
python build_assets.py --brand    # logo + fundo
```

Para acrescentar imagens: jogue o arquivo em `_originais/`, adicione a linha no TSV,
rode o script e registre o item em `GALLERY_CONFIG.items`.

**Tipografia:** Montserrat (Google Fonts).

---

## Pendências

- **Vídeo:** não foi entregue. O `video-gallery.html` aponta para
  `assets/video/video-torres.mp4`; o botão de vídeo no 3DVista só deve ser
  ligado depois de subir o arquivo (`./deploy.ps1 -WithVideo`). Ao chegar, medir o
  crop (cropdetect) e ajustar o `aspect-ratio` em `video-gallery.html`.
- **Legendas do decorado:** os subtítulos das imagens de apartamento descrevem o que
  se vê (Sala e Cozinha / Dormitório / Banheiro); conferir com o book se for
  preciso nomear suíte x dormitório x banheiro social.
- **Sobras do template anterior** no repositório, fora do deploy:
  `fachada-interativa.html` (Aflora Marista). Pode ser apagado.

---

## Deploy AWS S3

```powershell
./deploy.ps1               # sync (sem o vídeo) + cache-control no HTML/JS
./deploy.ps1 -QuickHtml    # só HTML/JS
./deploy.ps1 -WithVideo    # inclui o vídeo — 1ª vez / ao trocá-lo
```

O sync sobe **apenas** o que a galeria consome (HTML/JS + `assets/brand`, `fachada`,
`areas-comuns`, `apartamento`, `plantas`, `miniaturas`, `video`). HTML/JS recebem
`no-cache,no-store,must-revalidate`.

---

## Integração 3DVista

Loader no JavaScript global do projeto e chamadas nos botões — trechos prontos em
`3dvista-snippets.md`:

```js
GaleriaImagens(1);      // abre galeria de imagens    · GaleriaImagens(0) fecha
GaleriaPlantas(1);      // abre galeria de plantas    · GaleriaPlantas(0) fecha
AbrirGaleriaVideos(1);  // abre o vídeo               · AbrirGaleriaVideos(0) fecha
```
