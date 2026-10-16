"""Demonstrações geométricas originais: adução deitada, prancha e alongamento.

São ilustrações DIDÁTICAS em etapas, baseadas em instruções da ACE,
Harvard Health e CUH/NHS. Não copia arte/fotografia dessas fontes e não
constitui avaliação clínica, análise de amplitude ou validação de segurança.
"""
from PIL import Image, ImageDraw
from math import sin, pi

INK="#304470"
LEGGING="#34446b"
PINK="#ef6d9b"
SHOE="#f794a9"
SKIN="#e4a27f"

def stroke(d, a, b, color, width=14, outline=3):
    d.line((a[0],a[1],b[0],b[1]),fill=INK,width=width+2*outline,joint="curve")
    d.ellipse((a[0]-(width+2*outline)/2,a[1]-(width+2*outline)/2,a[0]+(width+2*outline)/2,a[1]+(width+2*outline)/2),fill=INK)
    d.ellipse((b[0]-(width+2*outline)/2,b[1]-(width+2*outline)/2,b[0]+(width+2*outline)/2,b[1]+(width+2*outline)/2),fill=INK)
    d.line((a[0],a[1],b[0],b[1]),fill=color,width=width,joint="curve")
    for x,y in (a,b):
        r=width/2
        d.ellipse((x-r,y-r,x+r,y+r),fill=color)

def head(d,center,r=18):
    x,y=center
    d.ellipse((x-r-2,y-r-2,x+r+2,y+r+2),fill=INK)
    d.ellipse((x-r,y-r,x+r,y+r),fill=SKIN)
    d.ellipse((x-r,y-r-5,x+r,y-1),fill="#453544")
    d.ellipse((x+r-5,y-5,x+r-2,y-2),fill=INK)

def mat(d,y=274):
    d.rounded_rectangle((14,y,329,y+20),radius=9,fill="#b6a7e6")
    d.line((32,y+8,309,y+8),fill="#d9d0f2",width=3)

def arrow(d,x,y):
    c="#ea357e"
    d.line([(x,y+22),(x,y)],fill=c,width=5)
    d.polygon([(x-7,y+7),(x,y-3),(x+7,y+7)],fill=c)

def setup():
    return Image.new("RGBA",(335,335),(0,0,0,0))

def inner_thigh(step):
    # PERNA DE BAIXO se move; perna superior DOBRADA fica apoiada.
    im=setup()
    d=ImageDraw.Draw(im)
    mat(d,281)
    lift=(0,11,24)[step]
    hip=(156,246)
    # Perna inferior sempre estendida, antevista em tom claro.
    knee=(223,258-lift//2)
    ankle=(306,264-lift)
    stroke(d,hip,knee,"#52628d",15)
    stroke(d,knee,ankle,"#52628d",14)
    stroke(d,ankle,(320,265-lift),SHOE,10)
    # Perna superior dobrada atravessa a frente, joelho à frente.
    stroke(d,(152,241),(203,218),LEGGING,17)
    stroke(d,(203,218),(216,270),LEGGING,14)
    stroke(d,(216,270),(235,271),SHOE,10)
    # Tronco e braço de sustentação ficam estáveis
    stroke(d,(151,241),(102,211),PINK,28)
    stroke(d,(104,213),(81,258),SKIN,13)
    stroke(d,(81,258),(56,259),SKIN,12)
    head(d,(79,195),19)
    d.ellipse((53,190,60,199),fill="#493448")
    arrow(d,305,220-lift)
    d.text((172,308),"Sobe a perna DE BAIXO",fill=INK)
    return im

def kneeling_plank(step):
    im=setup()
    d=ImageDraw.Draw(im)
    mat(d,255)
    # Linha corporal constante da cabeça aos JOELHOS, sem movimento de rep.
    shoulder=(124,154)
    hip=(222,190)
    knee=(302,222)
    stroke(d,hip,knee,LEGGING,24)
    stroke(d,shoulder,hip,PINK,28)
    stroke(d,knee,(326,244),LEGGING,14)
    stroke(d,(326,244),(331,245),SHOE,9)
    # cotovelo sob ombro; antebraço apoiado no tapete
    stroke(d,shoulder,(124,241),SKIN,14)
    stroke(d,(124,241),(180,244),SKIN,12)
    stroke(d,(107,159),(72,146),SKIN,13)
    head(d,(67,138),16)
    # O movimento visível é APENAS um discreto indicador de respiração.
    xx=(175,222,236)[step]
    d.ellipse((xx-5,118,xx+5,128),fill="#3a9cc1")
    d.text((144,98),"Respire",fill=INK)
    d.text((147,305),"ISOMETRIA: corpo imóvel",fill=INK)
    return im

def seated_glute(step):
    im=setup()
    d=ImageDraw.Draw(im)
    mat(d,280)
    delta=(0,5,11)[step]
    hip=(131,249)
    # Uma perna estendida; a outra cruzada por cima, joelho abraçado.
    stroke(d,(142,257),(221,268),LEGGING,18)
    stroke(d,(221,268),(301,270),LEGGING,16)
    stroke(d,(301,270),(320,274),SHOE,11)
    cross_knee=(206-delta,207-delta)
    stroke(d,hip,cross_knee,"#3d527b",19)
    stroke(d,cross_knee,(240-delta,264),LEGGING,15)
    stroke(d,(240-delta,264),(257-delta,271),SHOE,10)
    # Tronco ereto fixo, sem torsão agressiva
    stroke(d,hip,(134,166),PINK,29)
    head(d,(133,132),18)
    stroke(d,(144,173),(183-delta,202-delta),SKIN,13)
    stroke(d,(183-delta,202-delta),(198-delta,208-delta),SKIN,11)
    stroke(d,(117,174),(168-delta,211-delta),SKIN,12)
    stroke(d,(168-delta,211-delta),(197-delta,208-delta),SKIN,11)
    d.text((153,305),"Joelho ao peito, sem forçar",fill=INK)
    return im

BUILDERS={"interna":inner_thigh,"prancha-joelhos":kneeling_plank,"gluteo-sentado":seated_glute}

def build(exercise_id):
    """Três poses por exercício, origem 100% programática."""
    if exercise_id not in BUILDERS:
        raise KeyError(exercise_id)
    return [BUILDERS[exercise_id](i) for i in range(3)]
