# Trechos para colar no 3DVista — José Torres Sobrinho

Copie daqui. Cada bloco é independente.

---

## 1. Loader — cole no **JavaScript global do projeto** (roda uma vez)

```js
(function(){
  var s = document.createElement('script');
  s.src = 'https://skylineip.s3.sa-east-1.amazonaws.com/Tour+Virtual/saraiva-rezende/torres/ferramentas/inject.js?v=' + Date.now();
  document.head.appendChild(s);
})();
```

---

## 2. Galerias — cole na **action** do hotspot/botão

Abrir a galeria de imagens:

```js
GaleriaImagens(1);
```

Fechar a galeria de imagens:

```js
GaleriaImagens(0);
```

Abrir a galeria de plantas:

```js
GaleriaPlantas(1);
```

Fechar a galeria de plantas:

```js
GaleriaPlantas(0);
```

Abrir o vídeo:

```js
AbrirGaleriaVideos(1);
```

Fechar o vídeo:

```js
AbrirGaleriaVideos(0);
```
