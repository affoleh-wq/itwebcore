# WebCore — контент

Всё для соцсетей WebCore (@itswebcore): брендбук, логотип и готовые посты для Telegram и Instagram — по одному в день.

## Как забирать пост на сегодня

1. Открой `content/` → папку недели → папку дня (например, `01_2026-11-28_sb_znakomstvo`).
2. `telegram.md` — скопируй текст в канал / группу Telegram, приложи `post.png` (или слайды альбомом).
3. `instagram.md` — подпись для Instagram, картинка та же (`post.png` или `slide-1…6.png` для карусели).
4. Заполни всё в [квадратных скобках] своими данными или удали эти фразы. Подсказки — в `notes.md`.

Новая неделя появляется в `content/` каждое воскресенье.

## Структура

```
brand/       брендбук (README.md), цвета и шрифты (tokens.json), логотипы svg + png
content/     посты по неделям и дням: telegram.md, instagram.md, картинки, notes.md
templates/   исходники картинок (HTML) — по ним рендерятся PNG
tools/       render.py — HTML → PNG 1080×1350; make_logo.py — генератор SVG логотипа
```

## Онлайн-версии

- Брендбук: https://claude.ai/artifact/QbpRvEtLxS9kAguBnJHeWp
- Тексты: https://claude.ai/artifact/FtPdGRc1ynD8hf2HnTNcro
- Картинки недели 1 (редактируемый канвас): https://claude.ai/artifact/3MYrVXMfvaf55EGuCUR4Nk
