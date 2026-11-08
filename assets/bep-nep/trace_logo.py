from PIL import Image, ImageFilter;import numpy as np;from scipy import ndimage as nd
im=np.asarray(Image.open('/root/.claude/uploads/dca3ee88-efea-5771-8d24-154f92019262/ed9ba449-image.jpg').convert('RGB')).astype(int)
r,g,b=im[...,0],im[...,1],im[...,2];lum=(r+g+b)/3
L=nd.gaussian_filter(lum,1.6)
bgL=nd.grey_closing(nd.zoom(L,0.125,order=1),size=(25,25)); bgL=nd.gaussian_filter(bgL,4)
bgL=nd.zoom(bgL,(L.shape[0]/bgL.shape[0],L.shape[1]/bgL.shape[1]),order=1)
ratio=L/np.maximum(bgL,1)
m=(ratio<0.62)&(r-g>-12)
m=nd.binary_opening(m,iterations=1)
np.save('ratio.npy',ratio)
print('ink color',np.median(im[m&(lum<90)],axis=0),'bg',np.median(im[(lum>200)],axis=0))
lab,n=nd.label(m);S=nd.find_objects(lab)
out=np.zeros_like(m)
for i,sl in enumerate(S):
  k=i+1;a=(lab[sl]==k).sum();x0,x1,y0,y1=sl[1].start,sl[1].stop,sl[0].start,sl[0].stop
  if a<60 or y0<900 or y1>1600: continue
  if 690<x0<720 and y0>1100: continue   # clipped p of Bep
  if 900<x0<1010: continue      # seam
  if x1>935 and x0<1010: continue
  out|=(lab==k)
# copy p of Nep to Bep position
pk=[i+1 for i,sl in enumerate(S) if 1520<sl[1].start<1560 and sl[0].start>1140][0];print('pk',pk);p=(lab==pk); ys,xs=np.where(p); out[ys+1,xs-833]=True
out=nd.binary_fill_holes(out)^nd.binary_fill_holes(out)&~out  # keep
# fill only tiny holes (noise)
holes=nd.binary_fill_holes(out)&~out; hl,hn=nd.label(holes)
sz=nd.sum(holes,hl,range(1,hn+1))
for j,s in enumerate(sz):
  if s<150: out[hl==j+1]=True
from PIL import ImageDraw
M=Image.fromarray(out.astype('uint8')*255);D=ImageDraw.Draw(M)
lines=[([(557,1063),(595,1056)],8),
 ([(462,1146),(520,1133),(590,1118),(650,1108),(695,1102)],8),
 ([(515,1131),(531,1108)],6),([(540,1127),(547,1113)],6),
 ([(626,1107),(605,1080)],6),([(648,1104),(637,1092)],6)]
def nep(p):return (1280+(p[0]-468)*214/223, 1052+(p[1]-1045)*101/110)
for pts,w in lines:
  for T in (lambda p:p,):
    D.line([T(p) for p in pts],fill=0,width=w,joint='curve')
out=np.asarray(M)>0
out=out.copy()
Y,X=np.mgrid[1030:1166,1265:1516]
clr=(X<1500)|(Y>1060); out[Y[clr],X[clr]]=False
hat=out[1030:1170,450:702]; hy,hx=np.where(hat)
out[hy+1030+4,hx+450+808]=True
ys,xs=np.where(out);pad=60
out=out[ys.min()-pad:ys.max()+pad, xs.min()-pad:xs.max()+pad]
img=Image.fromarray((out*255).astype('uint8')).rotate(-0.5,resample=Image.BICUBIC,expand=False)
W,H=img.size;img=img.resize((W*3,H*3),Image.BICUBIC).filter(ImageFilter.GaussianBlur(8))
a=np.asarray(img).astype(float)
alpha=np.clip((a-128)*6+128,0,255).astype('uint8')  # crisp antialiased edge
A=Image.fromarray(alpha)
ink=(61,33,58);bg=(243,233,198)
t=Image.new('RGBA',A.size,ink+(0,));t.putalpha(A);t.save('bep-nep-logo-transparent.png')
c=Image.new('RGB',A.size,bg);c.paste(Image.new('RGB',A.size,ink),mask=A);c.save('bep-nep-logo-cream.png')
print(A.size)
