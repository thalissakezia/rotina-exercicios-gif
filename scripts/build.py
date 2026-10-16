#!/usr/bin/env python3
"""GIFs de movimentos em etapas, baseados em 3 poses ilustradas de fonte aberta.

NÃO gerar quadros intermediários com IA ou alterar a biomecânica. As artes são
de Bryl Lim / Everkinetic (CC BY-SA 4.0), veja docs/REFERENCIAS.md.
"""
import argparse
import io
import json
import math
import urllib.request
from pathlib import Path
import cairosvg
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"output"
DAYS=("segunda","terca","quarta","quinta","sexta","sabado","domingo")
CATALOG=json.loads((ROOT/"data/exercicios.json").read_text(encoding="utf-8"))
INDEX={x["id"]:x for x in CATALOG["exercicios"]}
REV=CATALOG["fonte"]["revision"]
PINK="#e42c75"
NAVY="#142456"
ORANGE="#f16b3c"
COLORS=("#ffeaf2","#e4f5ff","#ebfaeb","#fff3d7","#f1e9ff","#e9f6f5")
ANIM=(0,1,2,1,0)
CACHE={}
ERRORS=set()

def font(n,bold=False):
    family="DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/"+family,n)

def wrapped(draw,txt,x,y,limit,f,color=NAVY,lines=2,spacing=1.25):
    parts=txt.split()
    rows=[]; current=""
    for word in parts:
        trial=(current+" "+word).strip()
        if current and draw.textlength(trial,font=f)>limit:
            rows.append(current);current=word
        else:current=trial
    if current:rows.append(current)
    for row in rows[:lines]:
        draw.text((x,y),row,font=f,fill=color)
        y+=int(f.size*spacing)
    return y

def get_poses(ex):
    if ex["status"]!="referenciado":return []
    slug=ex["slug"]
    if slug in CACHE:return CACHE[slug]
    result=[]
    for i in (1,2,3):
        url=("https://raw.githubusercontent.com/bryllim/workout-guide/"
             +REV+"/packages/workout-guide/assets/"+slug+"/frame-"+str(i)+".svg")
        try:
            with urllib.request.urlopen(url,timeout=35) as f: data=f.read()
            data=data.replace(b'fill="#fff"',b'fill="#304470"')  # melhorar contraste nos cartões claros
            png=cairosvg.svg2png(bytestring=data,output_width=335,output_height=335)
            result.append(Image.open(io.BytesIO(png)).convert("RGBA"))
        except Exception as exc:
            ERRORS.add(slug+": "+str(exc))
            CACHE[slug]=[]
            return []
    CACHE[slug]=result
    return result

def diagram(draw,x,y,group):
    """Mini corpo esquemático com regiões gerais (não é atlas anatômico)."""
    s=" ".join(group).lower()
    grey="#b9bdc4"
    c=x+44
    draw.ellipse((c-12,y,c+12,y+23),fill=grey)
    draw.rounded_rectangle((c-22,y+24,c+22,y+98),radius=12,fill=grey)
    for side in (-1,1):
        draw.line((c+side*19,y+40,c+side*34,y+108),fill=grey,width=12)
        draw.line((c+side*12,y+93,c+side*17,y+170),fill=grey,width=15)
    if any(k in s for k in ("glúte","quadr")):
        draw.ellipse((c-23,y+76,c+23,y+110),fill=ORANGE)
    if any(k in s for k in ("cox","adutor","abdutor","posterior","perna")):
        for side in (-1,1):
            q=c+side*13
            draw.ellipse((q-10,y+101,q+10,y+139),fill=ORANGE)
    if any(k in s for k in ("core","abdôm","lombar")):
        draw.rounded_rectangle((c-16,y+60,c+16,y+87),radius=8,fill=ORANGE)
    if any(k in s for k in ("ombro","braço","tríceps","peitoral","costas","postura")):
        draw.ellipse((c-33,y+35,c+33,y+57),fill=ORANGE)
    draw.text((x-1,y+178),"músculos",font=font(14),fill=NAVY)

def card(ex,series,dose,pose,number):
    w,h=650,520
    im=Image.new("RGB",(w,h),"#fffefe")
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((4,4,w-4,h-4),radius=24,fill=COLORS[number%len(COLORS)],outline="#e9e3ea",width=2)
    d.ellipse((18,16,75,73),fill=("#da5a82","#4ca9d3","#58ae65","#efad32","#9772cd")[number%5])
    d.text((37,24),str(number+1),font=font(28,True),fill="white")
    wrapped(d,ex["nome"],88,18,545,font(28,True),lines=2)
    wrapped(d,"Músculos: "+ex["musculos"],25,103,608,font(18),lines=2)
    diagram(d,21,158,ex["musculos"].split(","))
    poses=get_poses(ex)
    if poses:
        art=poses[pose]
        im.paste(art,(225,122),art)
    else:
        d.rounded_rectangle((175,163,625,379),radius=15,fill="#fff7f7")
        wrapped(d,"REFERÊNCIA TÉCNICA PENDENTE",193,220,415,font(22,True),PINK,2)
        wrapped(d,"GIF suspenso para não ensinar movimento incorreto.",194,294,408,font(17),lines=2)
    d=ImageDraw.Draw(im)
    wrapped(d,ex["instrucoes"],27,422,596,font(17),lines=2)
    d.rounded_rectangle((20,474,630,512),radius=12,fill="#ffffff")
    d.text((33,483),str(series)+(" série" if series==1 else " séries")+"  |  "+dose,font=font(19,True),fill=NAVY)
    d.text((490,499),"CC BY-SA",font=font(9),fill="#64718a")
    return im

def store_gif(frames,path):
    path.parent.mkdir(parents=True,exist_ok=True)
    quant=[f.quantize(colors=112,method=Image.Quantize.MEDIANCUT) for f in frames]
    quant[0].save(path,save_all=True,append_images=quant[1:],duration=[310,270,380,270,310],loop=0,disposal=2,optimize=True)

def build_day(day):
    spec=json.loads((ROOT/"data/dias"/(day+".json")).read_text(encoding="utf-8"))
    rows=math.ceil(len(spec["exercicios"])/2)
    width=1320;height=160+rows*527+84
    result=[]
    for pose in ANIM:
        im=Image.new("RGB",(width,height),"#fff8fb")
        d=ImageDraw.Draw(im)
        d.text((25,15),"Rotina da manhã — "+day.capitalize(),font=font(43,True),fill=NAVY)
        d.text((28,80),spec["objetivo"]+"  •  Descanso: "+str(spec["descanso_segundos"])+" s",font=font(23),fill=PINK)
        for idx,item in enumerate(spec["exercicios"]):
            ex=INDEX[item["id"]]
            panel=card(ex,item["series"],item["dose"],pose,idx)
            im.paste(panel,(10+(idx%2)*655,137+(idx//2)*527))
        d=ImageDraw.Draw(im)
        d.text((25,height-65),"Artes: Bryl Lim / Everkinetic (CC BY-SA 4.0). Áreas musculares ilustrativas.",font=font(17),fill=NAVY)
        result.append(im)
    store_gif(result,OUT/"daily"/(day+".gif"))
    print("Dia gerado:",day,len(spec["exercicios"]),"exercícios")
    for idx,item in enumerate(spec["exercicios"]):
        ex=INDEX[item["id"]]
        if ex["status"]!="referenciado" or not get_poses(ex):continue
        path=OUT/"gifs"/(item["id"]+".gif")
        if path.exists():continue
        store_gif([card(ex,item["series"],item["dose"],pose,idx) for pose in ANIM],path)
    return spec

def generate_html(days):
    lines=['<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">',
           '<meta name="viewport" content="width=device-width, initial-scale=1">',
           '<title>Rotina de exercícios</title><style>',
           'body{font:16px system-ui;max-width:1050px;margin:auto;padding:20px;background:#fff8fb;color:#142456}',
           'section{padding:16px 0}img{max-width:100%;height:auto;border-radius:12px}',
           'nav{display:flex;gap:12px;flex-wrap:wrap}a{color:#a92865}',
           '</style></head><body><h1>Rotina semanal animada</h1>',
           '<p>Movimentos com três poses de referência; não substituem orientação profissional.</p>',
           '<nav>']
    for day in days:lines.append('<a href="#'+day+'">'+day.capitalize()+'</a>')
    lines.append('</nav>')
    for day in days:
        lines.append('<section id="'+day+'"><h2>'+day.capitalize()+'</h2>')
        lines.append('<img src="daily/'+day+'.gif" alt="Exercícios de '+day+'"></section>')
    lines.append('<p>Imagens: Bryl Lim / Everkinetic. CC BY-SA 4.0. Consulte README e docs/REFERENCIAS.md.</p></body></html>')
    (OUT/"semana.html").write_text("\n".join(lines),encoding="utf-8")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--all",action="store_true")
    ap.add_argument("--day",choices=DAYS)
    args=ap.parse_args()
    days=DAYS if args.all or not args.day else [args.day]
    for day in days:build_day(day)
    generate_html(days)
    if ERRORS:print("Referências indisponíveis:\n"+"\n".join(sorted(ERRORS)))
    print("Arquivos produzidos em",OUT)

if __name__=="__main__":main()
