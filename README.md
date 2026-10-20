# Galeria — Itá Nobre (Tenda)

Galeria de imagens/plantas (+ player de vídeo) para injeção via script no 3DVista, hospedada no AWS S3.
Criada a partir do template da galeria José Torres Sobrinho (Saraiva de Rezende).

**Empreendimento:** Itá Nobre
**Incorporadora:** Tenda
**Tema:** fundo sólido taupe `#C3AEA1`, texto marrom escuro `#2E2019`, estado ativo marrom `#5A3A2B`.
O lightbox e os rótulos sobre foto continuam escuros, com texto creme.

---

## URLs de produção

| Arquivo | URL |
|---------|-----|
| Galeria | `https://skylineip.s3.sa-east-1.amazonaws.com/Tour+Virtual/TENDA/ferramentas/galeria/ita+nobre/index.html` |
| Vídeo   | `https://skylineip.s3.sa-east-1.amazonaws.com/Tour+Virtual/TENDA/ferramentas/galeria/ita+nobre/video-gallery.html` |
| Script  | `https://skylineip.s3.sa-east-1.amazonaws.com/Tour+Virtual/TENDA/ferramentas/galeria/ita+nobre/inject.js` |

**S3 path:** `s3://skylineip/Tour Virtual/TENDA/ferramentas/galeria/ita nobre/`

---

## Estrutura de arquivos

```
ita nobre/
├── index.html            ← galeria de imagens + plantas (?mode=imagens | plantas)
├── video-gallery.html    ← player do vídeo
├── inject.js             ← loader leve para injeção no 3DVista
├── deploy.ps1            ← deploy para o S3 (Windows)
├── build_assets.py       ← regera assets/ a partir de _originais/ (Pillow)
├── assets-map.tsv        ← arquivo entregue → nome final (fonte do build)
├── _originais/           ← material entregue, FORA do git e do deploy
│   ├── imagens/ (fachada, lazer, apartamento)  plantas/
└── assets/
    ├── brand/            ← logo.svg (traço escuro; a animação toca uma vez)
    ├── areas-comuns/     ← 10 imagens, uma sub-categoria por ambiente
    ├── apartamento/      ← decorado: sala/cozinha/varanda (4) + quartos/banheiro (4)
    ├── plantas/          ← 2 plantas tipo + bolotário, fundo branco
    ├── miniaturas/       ← espelha as pastas acima (grade)
    └── video/            ← vídeo 1080p (gitignored; ainda não entregue)
```

> Pastas e arquivos publicados: **minúsculos, sem espaços e sem acentos** (o S3 é
> case-sensitive). Os nomes de exibição, com acentuação, ficam em `GALLERY_CONFIG`
> no `index.html`.

---

## Categorias

| Categoria | Sub-categorias |
|-----------|----------------|
| Áreas Comuns | Todas · Salão de Festas · Churrasqueira · Piscina · Campo · Espaço Infantil · Pet Place · Saúde e Fitness |
| Apartamento Decorado | Sala e Cozinha · Quartos e Banheiro |
| Plantas | Tipologias (Planta Tipo / Com Varanda Estendida) · Bolotário |

---

## Assets — do material entregue ao WebP

| Uso | Tamanho | Qualidade |
|-----|---------|-----------|
| Lightbox | lado maior ≤ 2600 px (plantas ≤ 3000 px) | q80 (plantas q86) |
| Grade (`miniaturas/`) | lado maior ≤ 900 px (plantas ≤ 1400 px) | q72 (plantas q78) |

Os renders chegaram em 1080 px de altura (lazer em 1920 × 1080): o build **só reduz**, nunca amplia.
Plantas: PNG/TIF com transparência; o build assenta o desenho sobre branco e recorta na própria caixa.

```powershell
python build_assets.py            # só o que falta
python build_assets.py --force    # tudo
```

Para acrescentar imagens: jogue o arquivo em `_originais/`, adicione a linha no TSV,
rode o script e registre o item em `GALLERY_CONFIG.items`.

**Tipografia:** Montserrat (Google Fonts).

---

## Pendências

- **Vídeo:** não foi entregue. O `video-gallery.html` aponta para
  `assets/video/video-ita-nobre.mp4`; o botão de vídeo no 3DVista só deve ser
  ligado depois de subir o arquivo (`./deploy.ps1 -WithVideo`). Ao chegar, medir o
  crop e ajustar o `aspect-ratio` em `video-gallery.html`.
- **Legendas:** os subtítulos descrevem o que se vê em cada render; conferir com o book.
- **Pasta `assets/Plantas`:** no Windows ficou com "P" maiúsculo (arquivo travado pelo
  Explorer). O `deploy.ps1` já sobe para `assets/plantas/` em minúsculo; renomeie a
  pasta quando possível.

---

## Deploy AWS S3

```powershell
./deploy.ps1               # sync (sem o vídeo) + cache-control no HTML/JS
./deploy.ps1 -QuickHtml    # só HTML/JS
./deploy.ps1 -WithVideo    # inclui o vídeo — 1ª vez / ao trocá-lo
```

HTML/JS recebem `no-cache,no-store,must-revalidate`.

---

## Integração 3DVista

Loader no JavaScript global do projeto e chamadas nos botões — trechos prontos em
`3dvista-snippets.md`:

```js
GaleriaImagens(1);      // abre galeria de imagens    · GaleriaImagens(0) fecha
GaleriaPlantas(1);      // abre galeria de plantas    · GaleriaPlantas(0) fecha
AbrirGaleriaVideos(1);  // abre o vídeo               · AbrirGaleriaVideos(0) fecha
```
