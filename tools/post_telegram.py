"""Публикует пост дня из content/ в Telegram-канал через бота.

Берёт папку content/*/NN_ГГГГ-ММ-ДД_*/ на сегодняшнюю дату (Europe/Chisinau),
текст из telegram.md и картинки post.png или slide-*.png.
Если в тексте остались [квадратные скобки] — ничего не публикует и падает с ошибкой,
чтобы незаполненные заготовки не ушли в канал.
"""
import glob, json, os, re, sys, datetime, zoneinfo, urllib.request, urllib.error, uuid, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import telegraph

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT = os.environ["TELEGRAM_CHAT_ID"]
API = f"https://api.telegram.org/bot{TOKEN}/"

day = os.environ.get("POST_DATE") or datetime.datetime.now(zoneinfo.ZoneInfo("Europe/Chisinau")).date().isoformat()
dirs = sorted(glob.glob(f"content/*/[0-9][0-9]_{day}_*/"))
if not dirs:
    print(f"На {day} поста нет — пропускаю."); sys.exit(0)
d = dirs[0]
marker = f"content/.posted/{day}"
if os.path.exists(marker) and os.environ.get("DRY_RUN") != "true":
    print(f"Пост на {day} уже опубликован — пропускаю."); sys.exit(0)
text = open(os.path.join(d, "telegram.md"), encoding="utf-8").read().strip()
left = re.findall(r"\[[^\]]+\]", text)
if left:
    print(f"В {d}telegram.md остались незаполненные заготовки: {left}. Заполни их — пост не опубликован.")
    sys.exit(1)
images = sorted(glob.glob(os.path.join(d, "slide-*.png")), key=lambda p: int(re.search(r"(\d+)\.png$", p).group(1))) or glob.glob(os.path.join(d, "post.png"))

def call(method, fields, files=None):
    boundary = uuid.uuid4().hex
    body = b""
    for k, v in fields.items():
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    for k, path in (files or {}).items():
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"; filename=\"{os.path.basename(path)}\"\r\nContent-Type: image/png\r\n\r\n".encode()
        body += open(path, "rb").read() + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    req = urllib.request.Request(API + method, data=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        res = json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        res = json.load(e)
    if not res.get("ok"):
        raise SystemExit(f"Telegram ответил ошибкой: {res}")
    return res

title_file = os.path.join(d, "title.txt")
dry = os.environ.get("DRY_RUN") == "true"
if os.path.exists(title_file) and os.environ.get("ARTICLE_MODE", "on") != "off":
    title = open(title_file, encoding="utf-8").read().strip()
    channel_url = f"https://t.me/{CHAT[1:]}" if CHAT.startswith("@") else ""
    url = telegraph.publish(title, text, images, channel_url)
    print(f"Статья: {url}")
    if dry:
        print("Пробный запуск — в канал не отправлено."); sys.exit(0)
    msg = f"<b>{html.escape(title)}</b>\n\n{html.escape(telegraph.lead(text))}\n\n<a href=\"{url}\">Читать статью →</a>"
    call("sendMessage", {"chat_id": CHAT, "text": msg, "parse_mode": "HTML",
                         "link_preview_options": json.dumps({"url": url, "prefer_large_media": True, "show_above_text": True})})
elif dry:
    print("Пробный запуск — в канал не отправлено."); sys.exit(0)
elif len(images) == 1 and len(text) <= 1024:
    call("sendPhoto", {"chat_id": CHAT, "caption": text}, {"photo": images[0]})
elif len(images) == 1:
    call("sendPhoto", {"chat_id": CHAT}, {"photo": images[0]})
    call("sendMessage", {"chat_id": CHAT, "text": text})
elif images:
    media = [{"type": "photo", "media": f"attach://p{i}"} for i in range(len(images[:10]))]
    if len(text) <= 1024:
        media[0]["caption"] = text
    call("sendMediaGroup", {"chat_id": CHAT, "media": json.dumps(media, ensure_ascii=False)}, {f"p{i}": p for i, p in enumerate(images[:10])})
    if len(text) > 1024:
        call("sendMessage", {"chat_id": CHAT, "text": text})
else:
    call("sendMessage", {"chat_id": CHAT, "text": text})
os.makedirs("content/.posted", exist_ok=True)
open(marker, "w").write(d + "\n")
print(f"Опубликовано: {d}")
