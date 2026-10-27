import sys, subprocess, numpy as np
def load(p):
    raw = subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32)/32768
def stats(p):
    x = load(p); sr=16000; hop=160; win=640
    n=(len(x)-win)//hop
    frames=np.lib.stride_tricks.as_strided(x,(n,win),(x.strides[0]*hop,x.strides[0]))
    rms=np.sqrt((frames**2).mean(1)); db=20*np.log10(rms+1e-9)
    thr=np.percentile(db,95)-30
    speech=db>thr
    f0=[]
    lo,hi=int(sr/300),int(sr/65)
    for i in np.where(speech)[0][::2]:
        f=frames[i]-frames[i].mean()
        ac=np.correlate(f,f,'full')[win-1:]
        if ac[0]<=0: continue
        seg=ac[lo:hi]; k=np.argmax(seg)+lo
        if ac[k]/ac[0]>0.45: f0.append(sr/k)
    f0=np.array(f0); st=12*np.log2(f0/np.median(f0))
    # Silben-Proxy: Energiespitzen im geglätteten Pegel
    env=np.convolve(rms,np.ones(5)/5,'same'); 
    peaks=((env[1:-1]>env[:-2])&(env[1:-1]>=env[2:])&(db[1:-1]>thr+6)).sum()
    dur=len(x)/sr; sp=speech.mean()
    print(f"{p.split('/')[-1][:28]:28s} dur {dur:5.1f}s  F0 med {np.median(f0):5.0f}Hz  F0-Streuung {np.std(st):4.2f} st  P10-P90 {np.percentile(st,90)-np.percentile(st,10):4.1f} st  Sprachanteil {sp*100:4.0f}%  Silben/s(Sprechzeit) {peaks/(dur*sp):4.1f}  Dyn {np.percentile(db[speech],90)-np.percentile(db[speech],10):4.1f}dB")
for p in sys.argv[1:]: stats(p)
