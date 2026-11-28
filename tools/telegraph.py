"""Превращает пост дня в статью Telegraph (Instant View)."""
import json, re, urllib.request, urllib.parse

API = "https://api.telegra.ph/"
RAW = "https://raw.githubusercontent.com/affoleh-wq/itwebcore/main/"
BULLET = re.compile(r"^(\d+[\.\)]|\d️⃣|[-•—]|[☀-➿\U0001F300-\U0001FAFF])")

def _call(method, params):
    data = urllib.parse.urlencode(params).encode()
    res = json.load(urllib.request.urlopen(urllib.request.Request(API + method, data=data)))
    if not res.get("ok"):
        raise SystemExit(f"Telegraph ответил ошибкой: {res}")
    return res["result"]

def to_nodes(text, images, channel_url):
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text.strip()) if b.strip()]
    nodes = [{"tag": "figure", "children": [{"tag": "img", "attrs": {"src": RAW + img}}]} for img in images]
    for n, b in enumerate(blocks):
        lines = [l.strip() for l in b.split("\n") if l.strip()]
        if n == 0:
            nodes.append({"tag": "p", "children": [{"tag": "strong", "children": [" ".join(lines)]}]})
            continue
        bullets = [l for l in lines if BULLET.match(l)]
        if len(lines) > 1 and len(bullets) >= len(lines) - 1:
            head = [l for l in lines if not BULLET.match(l)]
            if head:
                nodes.append({"tag": "p", "children": head})
            nodes.append({"tag": "ul", "children": [{"tag": "li", "children": [l]} for l in bullets]})
        elif n == len(blocks) - 1:
            nodes.append({"tag": "blockquote", "children": [" ".join(lines)]})
        else:
            children = []
            for j, l in enumerate(lines):
                if j:
                    children.append({"tag": "br"})
                children.append(l)
            nodes.append({"tag": "p", "children": children})
    links = [{"tag": "a", "attrs": {"href": "https://instagram.com/itswebcore"}, "children": ["Instagram @itswebcore"]}]
    if channel_url:
        links = [{"tag": "a", "attrs": {"href": channel_url}, "children": ["WebCore в Telegram"]}, " · "] + links
    nodes.append({"tag": "p", "children": links})
    return nodes

def publish(title, text, images, channel_url=""):
    author_url = channel_url or "https://instagram.com/itswebcore"
    acc = _call("createAccount", {"short_name": "WebCore", "author_name": "WebCore", "author_url": author_url})
    page = _call("createPage", {
        "access_token": acc["access_token"], "title": title[:256],
        "author_name": "WebCore", "author_url": author_url,
        "content": json.dumps(to_nodes(text, images, channel_url), ensure_ascii=False),
    })
    return page["url"]

def lead(text):
    first = re.split(r"\n\s*\n", text.strip())[0]
    return " ".join(l.strip() for l in first.split("\n"))
