import re, glob, os, asyncio
from playwright.async_api import async_playwright
import pathlib; ROOT=pathlib.Path(__file__).resolve().parents[1]; F=os.environ.get('FONTS_DIR', str(ROOT/'tools/node_modules/@fontsource'))
faces=''
for fam,d,ws in [('Exo 2','exo-2',[700,800]),('Inter','inter',[400,500,600,700])]:
    for w in ws:
        for sub,rng in [('cyrillic','U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116'),('latin','U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD')]:
            faces+=f"@font-face{{font-family:'{fam}';font-weight:{w};src:url(file://{F}/{d}/files/{d}-{sub}-{w}-normal.woff2) format('woff2');unicode-range:{rng}}}\n"
LOGO=str(ROOT/'brand/logo/svg')
REPL={'/_blob/e5e7d33c5ebe10cded658a893d9afceb':f'file://{LOGO}/webcore-mark.svg','/_blob/fc8b2a5683e872bedf5d93a027575744':f'file://{LOGO}/webcore-lockup.svg'}
async def main(pairs):
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--allow-file-access-from-files'])
        pg=await b.new_page(viewport={'width':1080,'height':1350})
        for src,out in pairs:
            s=open(src).read()
            inner=s[s.index('<x-dc>')+6:s.index('</x-dc>')]
            inner=re.sub(r'<helmet>.*?</helmet>','',inner,flags=re.S)
            for k,v in REPL.items(): inner=inner.replace(k,v)
            html=f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{faces} body{{margin:0}}</style></head><body>{inner}</body></html>'
            tmp=str(ROOT/'tools/.tmp.html'); open(tmp,'w').write(html)
            await pg.goto('file://'+tmp); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            os.makedirs(os.path.dirname(out),exist_ok=True)
            await pg.screenshot(path=out,clip={'x':0,'y':0,'width':1080,'height':1350})
        await b.close()
import sys, json
asyncio.run(main(json.loads(sys.argv[1])))
