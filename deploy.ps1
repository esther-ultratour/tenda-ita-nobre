<#
  deploy.ps1 — Deploy da galeria Jose Torres Sobrinho (Saraiva de Rezende) para o AWS S3.

  Uso:
    ./deploy.ps1             # sync completo + cache-control no HTML/JS
    ./deploy.ps1 -QuickHtml  # atualiza só index.html, video-gallery.html e inject.js (rápido)
    ./deploy.ps1 -WithVideo  # inclui o vídeo no sync (necessário na 1ª vez / ao trocá-lo)

  Pré-requisitos (uma única vez):
    1. AWS CLI instalado  -> https://aws.amazon.com/cli/
    2. Credenciais        -> aws configure   (regiao: sa-east-1)
#>

param(
  [switch]$QuickHtml,
  [switch]$WithVideo
)

$ErrorActionPreference = 'Stop'
$Bucket = 's3://skylineip/Tour Virtual/saraiva-rezende/torres/ferramentas'
$NoCache = 'no-cache,no-store,must-revalidate'

Set-Location -Path $PSScriptRoot

if (-not (Get-Command aws -ErrorAction SilentlyContinue)) {
  Write-Host 'ERRO: AWS CLI nao encontrado no PATH.' -ForegroundColor Red
  Write-Host 'Instale em https://aws.amazon.com/cli/ e rode "aws configure".' -ForegroundColor Yellow
  exit 1
}

function Copy-Html($file) {
  Write-Host "  -> $file" -ForegroundColor Cyan
  aws s3 cp $file "$Bucket/$file" --cache-control $NoCache
}

if ($QuickHtml) {
  Write-Host 'Atualizando apenas HTML/JS...' -ForegroundColor Green
  Copy-Html 'index.html'
  Copy-Html 'video-gallery.html'
  Copy-Html 'inject.js'
}
else {
  # O video fica de fora do sync por padrao (o --exclude tambem protege o
  # arquivo ja existente no S3 de ser removido pelo --delete).
  $videoExclude = @('--exclude', 'assets/video/*')
  if ($WithVideo) {
    Write-Host 'Sync completo (incluindo o video)...' -ForegroundColor Green
    $videoExclude = @()
  } else {
    Write-Host 'Sync completo para o S3 (sem o video)...' -ForegroundColor Green
  }

  # Sobe SO o que a galeria consome. Fica de fora: _originais/ (material
  # entregue), scripts/docs, e as sobras do template anterior (assets/thumbs/,
  # fachada-interativa.html), que nao pertencem a este empreendimento.
  aws s3 sync . "$Bucket/" `
    --exclude "*" `
    --include "index.html" --include "video-gallery.html" --include "inject.js" `
    --include "assets/brand/*" --include "assets/fachada/*" --include "assets/areas-comuns/*" --include "assets/apartamento/*" `
    --include "assets/plantas/*" --include "assets/miniaturas/*" --include "assets/video/*" `
    --exclude "*Thumbs.db" `
    @videoExclude `
    --delete

  # HTML/JS precisam de cache-control para o 3DVista nunca servir versao cacheada
  Write-Host 'Aplicando cache-control no HTML/JS...' -ForegroundColor Green
  Copy-Html 'index.html'
  Copy-Html 'video-gallery.html'
  Copy-Html 'inject.js'
}

Write-Host 'Deploy concluido.' -ForegroundColor Green
Write-Host "Base: https://skylineip.s3.sa-east-1.amazonaws.com/Tour+Virtual/saraiva-rezende/torres/ferramentas/" -ForegroundColor DarkGray
