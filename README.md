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

## Автопостинг в Telegram

Каждый день в 10:17 по Кишинёву GitHub публикует в канал пост на сегодня: текст из `telegram.md` и картинку (для карусели — альбомом). Если в тексте остались [квадратные скобки], пост не уходит — сначала заполни их.

Настройка один раз:

1. В Telegram открой @BotFather → `/newbot` → придумай имя и username бота → получи токен.
2. Открой свой канал → Управление каналом → Администраторы → Добавить администратора → найди бота → оставь право «Публикация сообщений».
3. В GitHub: этот репозиторий → Settings → Secrets and variables → Actions → New repository secret:
   - `TELEGRAM_BOT_TOKEN` — токен от BotFather;
   - `TELEGRAM_CHAT_ID` — `@имя_канала` (для приватного канала — числовой id вида `-100…`).
4. Проверка: вкладка Actions → «Пост дня в Telegram» → Run workflow → укажи дату поста, у которого заполнены все скобки.

Токен никому не пересылай и не пиши в чат — только в Secrets.
