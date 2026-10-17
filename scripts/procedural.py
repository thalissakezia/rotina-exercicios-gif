"""Demonstrações geométricas originais: adução deitada, prancha e alongamento.

São ilustrações DIDÁTICAS em etapas, baseadas em instruções da ACE,
Harvard Health e CUH/NHS. Não copia arte/fotografia dessas fontes e não
constitui avaliação clínica, análise de amplitude ou validação de segurança.
"""
from PIL import Image, ImageDraw
from math import sin, pi, cos, hypot, sqrt

INK="#304470"
LEGGING="#34446b"
PINK="#ef6d9b"
SHOE="#f794a9"
SKIN="#e4a27f"

def stroke(d, a, b, color, width=14, outline=3):
    a,b=tuple(round(x) for x in a),tuple(round(x) for x in b)
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

def eased(frame, count=12):
    return (1 - cos(2*pi*(frame%count)/count))/2

def rotate(point,pivot,angle):
    x,y=point[0]-pivot[0],point[1]-pivot[1]
    return (pivot[0]+x*cos(angle)-y*sin(angle),
            pivot[1]+x*sin(angle)+y*cos(angle))

def inner_landmarks(t):
    hip=(156,246)
    angle=-0.16*t
    return hip,rotate((223,258),hip,angle),rotate((306,270),hip,angle),rotate((320,271),hip,angle)

def seated_landmarks(t):
    hip=(131,249)
    knee=rotate((206,207),hip,-0.13*t)
    foot=(knee[0]+34,knee[1]+57)
    toe=(foot[0]+17,foot[1]+7)
    return hip,knee,foot,toe

def arm_elbow(shoulder,wrist,upper=43,forearm=43):
    dx,dy=wrist[0]-shoulder[0],wrist[1]-shoulder[1]
    dist=hypot(dx,dy)
    if dist>=upper+forearm:
        raise ValueError("Punho fora do alcance do braço")
    a=(upper**2-forearm**2+dist**2)/(2*dist)
    h=sqrt(max(0.0,upper**2-a**2))
    return (shoulder[0]+a*dx/dist-h*dy/dist,
            shoulder[1]+a*dy/dist+h*dx/dist)

def inner_thigh(t):
    # PERNA DE BAIXO se move; perna superior DOBRADA fica apoiada.
    im=setup()
    d=ImageDraw.Draw(im)
    mat(d,281)
    hip,knee,ankle,toe=inner_landmarks(t)
    lift=24*t
    # Perna inferior sempre estendida, antevista em tom claro.
    stroke(d,hip,knee,"#52628d",15)
    stroke(d,knee,ankle,"#52628d",14)
    stroke(d,ankle,toe,SHOE,10)
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
    arrow(d,305,217-18*t)
    d.text((167,294),"Sobe a perna DE BAIXO",fill=INK)
    return im

def kneeling_plank(t):
    im=setup()
    d=ImageDraw.Draw(im)
    mat(d,255)
    # Linha corporal constante da cabeça aos JOELHOS, sem movimento de rep.
    shoulder=PLANK_POINTS["shoulder"]
    hip=PLANK_POINTS["hip"]
    knee=PLANK_POINTS["knee"]
    stroke(d,hip,knee,LEGGING,24)
    stroke(d,shoulder,hip,PINK,28)
    # Joelho apoia diretamente no tapete. Canela/pé permanecem atrás.
    stroke(d,knee,(316,217),LEGGING,14)
    stroke(d,(316,217),(330,220),SHOE,9)
    # cotovelo sob ombro; antebraço apoiado no tapete
    stroke(d,shoulder,(124,241),SKIN,14)
    stroke(d,(124,241),(180,244),SKIN,12)
    stroke(d,(107,159),(72,146),SKIN,13)
    head(d,(67,138),16)
    # O movimento visível é APENAS um discreto indicador de respiração.
    xx=round(175+61*t)
    d.ellipse((xx-5,118,xx+5,128),fill="#3a9cc1")
    d.text((144,98),"Respire",fill=INK)
    d.text((147,291),"JOELHO APOIADO: isometria",fill=INK)
    return im

def seated_glute(t):
    im=setup()
    d=ImageDraw.Draw(im)
    mat(d,280)
    delta=11*t
    hip,cross_knee,foot,toe=seated_landmarks(t)
    # Uma perna estendida; a outra cruzada por cima, joelho abraçado.
    stroke(d,(142,257),(221,268),LEGGING,18)
    stroke(d,(221,268),(301,270),LEGGING,16)
    stroke(d,(301,270),(320,274),SHOE,11)
    stroke(d,hip,cross_knee,"#3d527b",19)
    stroke(d,cross_knee,foot,LEGGING,15)
    stroke(d,foot,toe,SHOE,10)
    # Tronco ereto fixo, sem torsão agressiva
    stroke(d,hip,(134,166),PINK,29)
    head(d,(133,132),18)
    target=(cross_knee[0]-7,cross_knee[1]+3)
    for shoulder in ((144,173),(117,174)):
        elbow=arm_elbow(shoulder,target)
        stroke(d,shoulder,elbow,SKIN,11)
        stroke(d,elbow,target,SKIN,10)
    d.text((153,292),"Joelho ao peito, sem forçar",fill=INK)
    return im

# Pontos explicitados permitem testes sem interpretação por IA.
PLANK_POINTS={"shoulder":(124,154),"hip":(218,205),"knee":(296,246),"mat_top":255}
INNER_LOWER_ANKLES=[(306,264),(306,253),(306,240)]
SEATED_TORSO={"hip":(131,249),"shoulder":(134,166)}

BUILDERS={"interna":inner_thigh,"prancha-joelhos":kneeling_plank,"gluteo-sentado":seated_glute}

def build(exercise_id, frame_count=12):
    """Fases suaves em loop, sem gerar imagem por IA."""
    if exercise_id not in BUILDERS:
        raise KeyError(exercise_id)
    if frame_count<8: raise ValueError("Mínimo de 8 quadros")
    return [BUILDERS[exercise_id](eased(i,frame_count)) for i in range(frame_count)]
