"""Ставит аватар и описание Telegram-канала из brand/profiles.md через бота."""
import json, os, re, uuid, urllib.request, urllib.error
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]; CHAT = os.environ["TELEGRAM_CHAT_ID"]
API = f"https://api.telegram.org/bot{TOKEN}/"
def call(method, fields, files=None):
    b = uuid.uuid4().hex; body = b""
    for k, v in fields.items():
        body += f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    for k, p in (files or {}).items():
        body += f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"; filename=\"{os.path.basename(p)}\"\r\nContent-Type: image/png\r\n\r\n".encode() + open(p, "rb").read() + b"\r\n"
    body += f"--{b}--\r\n".encode()
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(API + method, data=body, headers={"Content-Type": f"multipart/form-data; boundary={b}"})))
    except urllib.error.HTTPError as e:
        r = json.load(e)
    print(method, "ok" if r.get("ok") else f"ошибка Telegram: {r.get('description')}")
    if not r.get("ok"): globals()["FAILED"] = True
md = open("brand/profiles.md", encoding="utf-8").read()
tg = md.split("## Telegram-канал", 1)[1]
blocks = re.findall(r"```\n(.*?)\n```", tg, re.S)
description = blocks[1].strip()
call("setChatPhoto", {"chat_id": CHAT}, {"photo": "brand/logo/png/webcore-avatar-1080.png"})
call("setChatDescription", {"chat_id": CHAT, "description": description})

if globals().get("FAILED"):
    raise SystemExit("Проверь, что бот — администратор канала с правом «Изменение профиля канала».")
