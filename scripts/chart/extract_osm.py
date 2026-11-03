import sys,struct,zlib,json,math,collections,time
path,out=sys.argv[1],sys.argv[2]
def varint(b,i):
    r=0;s=0
    while True:
        c=b[i];i+=1;r|=(c&127)<<s
        if c<128:return r,i
        s+=7
def fields(b):
    i=0;n=len(b)
    while i<n:
        k,i=varint(b,i);f=k>>3;w=k&7
        if w==0:v,i=varint(b,i)
        elif w==2:
            l,i=varint(b,i);v=b[i:i+l];i+=l
        elif w==1:v=b[i:i+8];i+=8
        elif w==5:v=b[i:i+4];i+=4
        else:raise ValueError(w)
        yield f,w,v
def packed(b):
    r=[];i=0;n=len(b)
    while i<n:
        v,i=varint(b,i);r.append(v)
    return r
zz=lambda v:(v>>1)^-(v&1)
def delta(b):
    r=[];c=0
    for v in packed(b):
        c+=zz(v);r.append(c)
    return r
nodes={};ways=[];rels=[];pts=[]
t=time.time()
with open(path,'rb') as fh:
    while True:
        h=fh.read(4)
        if len(h)<4:break
        hl=struct.unpack('>I',h)[0];hd=fh.read(hl);typ=None;ds=0
        for f,w,v in fields(hd):
            if f==1:typ=v.decode()
            if f==3:ds=v
        blob=fh.read(ds);data=None
        for f,w,v in fields(blob):
            if f==1:data=v
            if f==3:data=zlib.decompress(v)
        if typ!='OSMData':continue
        st=[];gran=100;la0=lo0=0;groups=[]
        for f,w,v in fields(data):
            if f==1:st=[x[2] for x in fields(v)]
            elif f==2:groups.append(v)
            elif f==17:gran=v
            elif f==19:la0=v
            elif f==20:lo0=v
        S=[s.decode('utf8','ignore') for s in st]
        for g in groups:
            for f,w,v in fields(g):
                if f==2:
                    ids=lat=lon=kv=None
                    for ff,ww,vv in fields(v):
                        if ff==1:ids=delta(vv)
                        elif ff==8:lat=delta(vv)
                        elif ff==9:lon=delta(vv)
                        elif ff==10:kv=packed(vv)
                    j=0
                    for k in range(len(ids)):
                        la=(la0+lat[k]*gran)*1e-9;lo=(lo0+lon[k]*gran)*1e-9;nodes[ids[k]]=(lo,la)
                        if kv:
                            tg={}
                            while j<len(kv) and kv[j]!=0:
                                tg[S[kv[j]]]=S[kv[j+1]];j+=2
                            j+=1
                            if 'place' in tg:pts.append((lo,la,tg))
                elif f==3:
                    wid=0;ks=[];vs=[];refs=[]
                    for ff,ww,vv in fields(v):
                        if ff==1:wid=vv
                        elif ff==2:ks=packed(vv)
                        elif ff==3:vs=packed(vv)
                        elif ff==8:refs=delta(vv)
                    tg={S[a]:S[b] for a,b in zip(ks,vs)}
                    if tg.get('natural') in('coastline','reef','shoal') or 'place' in tg or 'building' in tg or tg.get('landuse')=='residential' or tg.get('natural')=='water':
                        ways.append((wid,tg,refs))
                elif f==4:
                    rid=0;ks=[];vs=[];ro=[];mi=[];ty=[]
                    for ff,ww,vv in fields(v):
                        if ff==1:rid=vv
                        elif ff==2:ks=packed(vv)
                        elif ff==3:vs=packed(vv)
                        elif ff==8:ro=packed(vv)
                        elif ff==9:mi=delta(vv)
                        elif ff==10:ty=packed(vv)
                    tg={S[a]:S[b] for a,b in zip(ks,vs)}
                    if tg.get('natural') in('reef','shoal','coastline') or 'place' in tg:
                        rels.append((rid,tg,[(S[r],m,t2) for r,m,t2 in zip(ro,mi,ty)]))
print('nodes',len(nodes),'ways kept',len(ways),'rels kept',len(rels),'place nodes',len(pts),'t',round(time.time()-t,1))
print('natural ways',collections.Counter(w[1].get('natural') for w in ways if 'natural' in w[1]))
print('place ways',collections.Counter(w[1].get('place') for w in ways if 'place' in w[1]))
print('place nodes',collections.Counter(p[2]['place'] for p in pts))
print('rels',collections.Counter((r[1].get('natural'),r[1].get('place')) for r in rels))
wm={w[0]:w for w in ways}
def coords(r):return [nodes[x] for x in r if x in nodes]
# join coastline ways into rings
coast=[w for w in ways if w[1].get('natural')=='coastline']
start=collections.defaultdict(list)
for w in coast:start[w[2][0]].append(w)
used=set();rings=[];openc=0
for w in coast:
    if w[0] in used:continue
    used.add(w[0]);chain=list(w[2])
    while chain[0]!=chain[-1]:
        nx=[c for c in start.get(chain[-1],[]) if c[0] not in used]
        if not nx:break
        used.add(nx[0][0]);chain+=nx[0][2][1:]
    if chain[0]==chain[-1]:rings.append(chain)
    else:openc+=1
print('coast ways',len(coast),'closed rings',len(rings),'open chains',openc)
def area(c):
    # signed km2, lon scaled by cos(lat)
    if len(c)<3:return 0,(0,0)
    la=sum(p[1] for p in c)/len(c);k=math.cos(math.radians(la));a=0;cx=cy=0
    for i in range(len(c)-1):
        x0,y0=c[i];x1,y1=c[i+1];cr=(x0*k*x1*0+0);cr=(x0*k)*y1-(x1*k)*y0;a+=cr;cx+=(x0+x1)*cr;cy+=(y0+y1)*cr
    a/=2
    if abs(a)<1e-14:return 0,(sum(p[0] for p in c)/len(c),la)
    return a*111.32*111.32,(cx/(6*a),cy/(6*a))
isl=[]
for r in rings:
    c=coords(r)
    if len(c)<4:continue
    a,ce=area(c);isl.append({'area':a,'lon':ce[0],'lat':ce[1],'ring':c})
pos=[i for i in isl if i['area']>0];neg=[i for i in isl if i['area']<=0]
print('rings land(+)',len(pos),'water/other(-)',len(neg),'area sum land km2',round(sum(i['area'] for i in pos),1))
sz=sorted(i['area'] for i in pos)
print('area quantiles km2',[round(sz[int(len(sz)*q)],4) for q in(0,.1,.25,.5,.75,.9,.99)] if sz else None,'max',sz[-1] if sz else None)
# reefs
reefs=[]
for w in ways:
    if w[1].get('natural') in('reef','shoal'):
        c=coords(w[2]);
        if len(c)>=2:reefs.append(c)
for r in rels:
    if r[1].get('natural') in('reef','shoal'):
        for role,m,t2 in r[2]:
            if t2==1 and m in wm:
                c=coords(wm[m][2]);
                if len(c)>=2:reefs.append(c)
print('reef lines',len(reefs),'points',sum(len(x) for x in reefs))
# buildings: centroid list
bld=[]
for w in ways:
    if 'building' in w[1]:
        c=coords(w[2])
        if c:bld.append((sum(p[0] for p in c)/len(c),sum(p[1] for p in c)/len(c)))
print('buildings',len(bld))
# names from place ways/rels/nodes
named=[]
for w in ways:
    if w[1].get('place') in('island','islet'):
        c=coords(w[2])
        if c:named.append((sum(p[0] for p in c)/len(c),sum(p[1] for p in c)/len(c),w[1].get('name:en') or w[1].get('name'),w[1].get('tourism'),w[0]))
for r in rels:
    if r[1].get('place') in('island','islet'):
        c=[]
        for role,m,t2 in r[2]:
            if t2==1 and m in wm and role in('outer',''):c+=coords(wm[m][2])
        if c:named.append((sum(p[0] for p in c)/len(c),sum(p[1] for p in c)/len(c),r[1].get('name:en') or r[1].get('name'),r[1].get('tourism'),r[0]))
for lo,la,tg in pts:
    if tg['place'] in('island','islet'):named.append((lo,la,tg.get('name:en') or tg.get('name'),tg.get('tourism'),0))
print('named island features',len(named),'with name',sum(1 for n in named if n[2]))
sett=[(lo,la,tg.get('name:en') or tg.get('name'),tg['place']) for lo,la,tg in pts if tg['place'] in('city','town','village','hamlet')]
print('settlement nodes',len(sett))
json.dump({'land':pos,'water':[{'area':i['area'],'lon':i['lon'],'lat':i['lat']} for i in neg],'reefs':reefs,'buildings':bld,'named':named,'settlements':sett},open(out,'w'))
