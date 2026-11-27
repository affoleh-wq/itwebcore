# Инструменты

## render.py — картинки постов

```
cd tools && npm i @fontsource/exo-2 @fontsource/inter && pip install playwright
python3 render.py '[["../templates/week-01/Main.dc.html", "../out/post.png"]]'
```

Рендерит шаблон в PNG 1080×1350 со шрифтами Exo 2 и Inter и логотипами из `brand/logo/svg`.

## make_logo.py — векторный логотип

`python3 make_logo.py` пересобирает все SVG в `out/`.
