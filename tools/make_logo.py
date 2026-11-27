def mark(silver_a, silver_b, uid):
    return f'''<defs>
<linearGradient id="{uid}-l" x1="0" y1="368" x2="0" y2="655" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#0081fc"/><stop offset="1" stop-color="#1550e0"/></linearGradient>
<linearGradient id="{uid}-m" x1="464" y1="368" x2="742" y2="655" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#0087fb"/><stop offset="1" stop-color="#12e0fd"/></linearGradient>
<linearGradient id="{uid}-s" x1="0" y1="368" x2="0" y2="655" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{silver_a}"/><stop offset="1" stop-color="{silver_b}"/></linearGradient>
</defs>
<g id="mark">
<linearGradient id="{uid}-k" x1="0" y1="505" x2="0" y2="655" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#0139a1"/><stop offset="1" stop-color="#1a5fe6"/></linearGradient>
<polygon points="545,505 657,505 567,655 470,655" fill="url(#{uid}-k)"/>
<polygon points="295,368 407,368 570,655 466,655" fill="url(#{uid}-l)"/>
<polygon points="464,368 576,368 742,655 631,655" fill="url(#{uid}-m)"/>
<polygon points="735,368 847,368 737,551 682,458" fill="url(#{uid}-s)"/>
<polygon points="839,454 910,454 790,655 748,655 733,631" fill="url(#{uid}-s)"/>
<rect x="933" y="256" width="24" height="24" fill="#09baff"/>
<rect x="915" y="294" width="18" height="18" fill="#03409f"/>
<rect x="867" y="309" width="39" height="39" fill="#0ac8fe"/>
<rect x="926" y="344" width="31" height="30" fill="#0ac7fe"/>
<rect x="867" y="368" width="48" height="47" fill="#0bc9fd"/>
</g>'''

def word(web_color, core_color="#0085fe"):
    S=14
    def W(x):  # filled parallelograms
        y0,y1=743,823
        pts=[(0.5,15.5,34.5,49.5),(64.5,79.5,34.5,49.5),(64.5,79.5,94.5,109.5),(128.5,143.5,94.5,109.5)]
        out=[]
        for a,b,c,d in pts:
            out.append(f'<polygon points="{x+a},{y0} {x+b},{y0} {x+d},{y1} {x+c},{y1}"/>')
        return ''.join(out)
    def E(x):
        y=743
        return (f'<rect x="{x}" y="{y}" width="15" height="80"/><rect x="{x}" y="{y}" width="76" height="{S}"/>'
                f'<rect x="{x}" y="{y+34}" width="75" height="{S}"/><rect x="{x}" y="{y+66}" width="76" height="{S}"/>')
    def stroke(d): return f'<path d="{d}" fill="none" stroke-width="{S}"/>'
    def B(x):
        y=743; h=S/2
        return stroke(f'M{x+h} {y} V{y+80} M{x} {y+h} H{x+64} A11 11 0 0 1 {x+75} {y+18} V{y+32} A11 11 0 0 1 {x+64} {y+43} H{x+h} M{x+h} {y+43} H{x+67} A11 11 0 0 1 {x+78} {y+54} V{y+62} A11 11 0 0 1 {x+67} {y+80-h} H{x}')
    def C(x):
        y=743; h=S/2
        return stroke(f'M{x+84} {y+h} H{x+20} A13 13 0 0 0 {x+h} {y+20} V{y+60} A13 13 0 0 0 {x+20} {y+80-h} H{x+84}')
    def O(x):
        y=743; h=S/2
        return stroke(f'M{x+20} {y+h} H{x+70} A13 13 0 0 1 {x+83} {y+20} V{y+60} A13 13 0 0 1 {x+70} {y+80-h} H{x+20} A13 13 0 0 1 {x+h} {y+60} V{y+20} A13 13 0 0 1 {x+20} {y+h} Z')
    def R(x):
        y=743; h=S/2
        return (stroke(f'M{x+h} {y+80} V{y} M{x} {y+h} H{x+64} A11 11 0 0 1 {x+75} {y+18} V{y+32} A11 11 0 0 1 {x+64} {y+43} H{x+h}')
                + f'<polygon points="{x+40},{y+50} {x+57},{y+50} {x+85},{y+80} {x+66},{y+80}"/>')
    web=f'<g fill="{web_color}" stroke="{web_color}">{W(210)}{E(384)}{B(493)}</g>'
    core=f'<g fill="{core_color}" stroke="{core_color}">{C(614)}{O(731)}{R(857)}{E(975)}</g>'
    return f'<g id="wordmark">{web}{core}</g>'

def svg(vb, body, bg=None, title="WebCore"):
    x,y,w,h=vb
    bgr=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" width="{w}" height="{h}" role="img" aria-label="{title}"><title>{title}</title>{bgr}{body}</svg>\n'

import os
os.makedirs('out',exist_ok=True)
DARK_SIL=("#f5f5f5","#cfcfcf"); LIGHT_SIL=("#9aa3b2","#6b7586")
MARK_VB=(275,236,702,439)
LOCK_VB=(190,236,880,606)
WORD_VB=(190,723,880,120)
files={
 'webcore-mark.svg': svg(MARK_VB, mark(*DARK_SIL,'d')),
 'webcore-mark-light.svg': svg(MARK_VB, mark(*LIGHT_SIL,'l')),
 'webcore-lockup.svg': svg(LOCK_VB, mark(*DARK_SIL,'d')+word('#ffffff')),
 'webcore-lockup-light.svg': svg(LOCK_VB, mark(*LIGHT_SIL,'l')+word('#050608')),
 'webcore-lockup-on-black.svg': svg(LOCK_VB, mark(*DARK_SIL,'d')+word('#ffffff'), bg='#050608'),
 'webcore-wordmark.svg': svg(WORD_VB, word('#ffffff')),
 'webcore-wordmark-light.svg': svg(WORD_VB, word('#050608')),
 'webcore-avatar.svg': svg((0,0,1080,1080), '<rect width="1080" height="1080" fill="#050608"/><g transform="translate(540 556) scale(1.22) translate(-626 -455)">'+mark(*DARK_SIL,'a')+'</g>'),
}
for n,c in files.items(): open('out/'+n,'w').write(c)
print(list(files))
