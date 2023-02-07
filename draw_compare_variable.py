import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import multiprocessing as mp
from decimal import Decimal, ROUND_HALF_UP
from scipy.stats import mannwhitneyu

def takelast(elem):
    return elem[-1]
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False

def effect_size(a,b):
    if a==[] or b==[]:
        return 0
    else:        
        U1, p = mannwhitneyu(a, b, alternative='two-sided')
        nx, ny = len(a), len(b)
        U2 = nx*ny - U1
        U = min(U1, U2)
        N = nx + ny
        z = abs((U - nx*ny/2 + 0.5) / np.sqrt(nx*ny * (N + 1)/ 12))
        return str(Decimal(float(z/np.sqrt(N))).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP))

def get_lime_list(n):
    lilst=[[],[]]
    for i in range(limedf.shape[0]):
        for m in limedf["lime_lst"].iloc[i]:
            ftstr=m[0]
            ftstr=ftstr.split( )
            for fts in ftstr:
                if fts=='>' or fts=='<' or fts=='<=' or is_number(fts):
                    continue
                else:
                    limeftname=fts
            if namelist[n]==limeftname:
                if m[1]>0:
                    lilst[1].append(i)
                if m[1]<0:
                    lilst[0].append(i)
                break
    return [lilst,n]

m=3
t=2
k=1
if __name__=="__main__":
    df=pd.read_pickle("./data/X_test_m"+str(m)+"_t"+str(t)+"_k"+str(k)+".pkl")
    y_test=pd.read_pickle("./data/y_test_m"+str(m)+"_t"+str(t)+"_k"+str(k)+".pkl")
    df.reset_index(drop=True,inplace=True)
    y_test.reset_index(drop=True,inplace=True)
    df['oneyear']=y_test
    namelist=['contributorcmt','commiterstd','corealliss','coreoveryearnum']
    limedf=pd.read_pickle("./data/limeres_m"+str(m)+"_t"+str(t)+"_k"+str(k)+".pkl")


    namelistind=[[i] for i in range(len(namelist))]
    with mp.Pool(mp.cpu_count() // 2) as pool:
        res=pool.starmap(get_lime_list, namelistind)
        res.sort(key=takelast)
        lime_list=[i[0] for i in res]
    ind=0
    ftlist=['contributorcmt','commiterstd','corealliss','coreoveryearnum']
    ftlists=['#cmt_p','cmt_dev_std','#issue_all_c','#pro_oneyear_c']


    for i in range(len(namelist)):
        if namelist[i]!=ftlist[ind]:
            continue
        signlist=df[namelist[i]].values.tolist()
        typelist=df['type'].values.tolist()

        signlist=np.array(signlist)
        typelist=np.array(typelist)
        neglist=list(signlist[lime_list[i][0]])
        poslist=list(signlist[lime_list[i][1]])
        typeneglist=list(typelist[lime_list[i][0]])
        typeposlist=list(typelist[lime_list[i][1]])
        a0,a1,a2,a3=[],[],[],[]
        for d in range(len(typeneglist)):
            if typeneglist[d]==0:
                a0.append(neglist[d])
            else:
                a1.append(neglist[d])
        for d in range(len(typeposlist)):
            if typeposlist[d]==0:
                a2.append(poslist[d])
            else:
                a3.append(poslist[d])
        pos=0
        alist=[[a0,a2],[a1,a3]]
        plt.figure(ind,figsize=(8, 4))
        position=[]
        effects=[]
        for t in [0,1]:
            list0=alist[t][0]
            list1=alist[t][1]
            effects.append(effect_size(list0,list1))
            bplot=plt.boxplot([list0,list1],widths=0.8,
            positions=[pos,pos+1], showmeans=True,showfliers=False,patch_artist=True,meanprops = {'markerfacecolor':'black','markeredgecolor':'black', 'markersize':10})
            position.append(pos+0.5)
            pos+=3
            [[item.set_color('k') for item in bplot['medians']]]
            colors = ['red','green']
            for patch, color in zip(bplot['boxes'], colors):
                patch.set_facecolor(color)
        plt.tick_params(bottom=False,top=False,left=False,right=False,labelsize=15)
        plt.xlim((-1, 3*2-1))
        plt.ylabel(ftlists[ind],{'size':25})
        plt.xticks(position,["organization\n(effect size: "+str(effects[0])+")","individual\n(effect size: "+str(effects[1])+")"])
        plt.xticks(fontsize=25)
        plt.yticks(fontsize=25)
        plt.legend(handles=[bplot["boxes"][0],bplot["boxes"][1]],labels=["Negative Group","Positive Group"],fontsize=20,loc="upper left")
        ax = plt.gca()
        bwith = 2
        ax.spines['bottom'].set_linewidth(bwith)
        ax.spines['left'].set_linewidth(bwith)
        ax.spines['top'].set_linewidth(bwith)
        ax.spines['right'].set_linewidth(bwith)
        plt.grid(alpha=0.6)
        plt.tight_layout()
        plt.savefig('comvartype'+str(ind)+'.png')
        ind+=1