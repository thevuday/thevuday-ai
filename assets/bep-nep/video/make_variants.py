from PIL import Image, ImageFilter, ImageDraw
import numpy as np; from scipy import ndimage as nd
src=Image.open('bep-nep-logo-transparent.png').getchannel('A')
W=2400; H=round(src.height*W/src.width); A=np.asarray(src.resize((W,H),Image.LANCZOS)).astype(float)/255
P=60; A=np.pad(A,P); H,W=A.shape
PUR=(61,33,58); CREAM=(250,240,212); WHITE=(255,255,255)
def stroke(a,r):
    d=nd.distance_transform_edt(a<0.5); return np.clip((r+0.7-d),0,1)
def layer(alpha,col):
    im=Image.new('RGBA',(W,H),col+(0,)); im.putalpha(Image.fromarray((np.clip(alpha,0,1)*255).astype('uint8'))); return im
def shadow(alpha,blur,op,dy):
    s=Image.fromarray((alpha*255*op).astype('uint8')).filter(ImageFilter.GaussianBlur(blur))
    s=np.roll(np.asarray(s).astype(float)/255,dy,axis=0); return layer(s,(20,8,18))
def comp(*ls):
    out=Image.new('RGBA',(W,H),(0,0,0,0))
    for l in ls: out=Image.alpha_composite(out,l)
    return out
st=stroke(A,13)
# 1: cream fill, purple outline, shadow
v1=comp(shadow(st,18,.65,10),layer(st,PUR),layer(A,CREAM))
# 2: white fill, purple outline + thin cream outer ring, shadow
st2=stroke(A,20)
v2=comp(shadow(stroke(A,26),22,.7,12),layer(stroke(A,26),CREAM),layer(st2,PUR),layer(A,WHITE))
# 3: purple logo with strong cream glow (original color kept)
glow=Image.fromarray((stroke(A,16)*255).astype('uint8')).filter(ImageFilter.GaussianBlur(10))
g=np.clip(np.asarray(glow).astype(float)/255*1.6,0,1)
v3=comp(shadow(stroke(A,16),24,.5,10),layer(g,CREAM),layer(stroke(A,10),CREAM),layer(A,PUR))
for n,v in [('1-kem-vien-tim',v1),('2-trang-vien-doi',v2),('3-tim-vien-kem',v3)]:
    bb=v.getbbox(); v.crop(bb).save(f'bep-nep-video-{n}.png')
# preview on screenshot
bg=Image.open('/root/.claude/uploads/dca3ee88-efea-5771-8d24-154f92019262/b768bc2c-image.png').convert('RGBA').crop((272,338,934,1514))
tiles=[]
for n in ['1-kem-vien-tim','2-trang-vien-doi','3-tim-vien-kem']:
    t=bg.copy(); lg=Image.open(f'bep-nep-video-{n}.png'); w=600; lg=lg.resize((w,round(lg.height*w/lg.width)),Image.LANCZOS)
    t.alpha_composite(lg,((t.width-w)//2,330)); tiles.append(t)
pv=Image.new('RGBA',(bg.width*3+40,bg.height),(30,30,30,255))
for i,t in enumerate(tiles): pv.paste(t,(i*(bg.width+20),0))
pv.convert('RGB').save('preview-video.png')
