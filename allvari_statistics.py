from statistics import mean, median
import numpy as np
import pandas as pd
import multiprocessing as mp
from decimal import Decimal, ROUND_HALF_UP
import scipy.stats as stats
from scipy.stats import mannwhitneyu


meaning=['The average number of commits','The average number of commits','The average number of pull requests','The average number of pull requests','The average number of reported issues','The average number of reported issues','The average number of reported issues','The average number of issue comments','The average number of issue comments','The average number of issue comments',
'The average number of pull request comments','The average number of pull request comments','The average number of pull request comments','The average number of commit comments','The average number of commit comments','The average number of commit comments','The average number of issue events','The average number of issue events','The average number of issue events','The average number of followed developers','The average number of followed developers',
'The average number of followed developers','The average number of starred projects','The average number of starred projects','The average number of starred projects','The number of days with commit activity','The median number of commits per day','The number of commits in the first half of observation period','The number of commits in the second half of observation period','The standard deviation of commits per day','The standard deviation of commits per code contributor','The average number of commits on all GitHub','The average number of commits on all GitHub','The average number of commits on all GitHub',
'The average number of pull requests on all GitHub','The average number of pull requests on all GitHub','The average number of pull requests on all GitHub','The average number of reported issues on all GitHub','The average number of reported issues on all GitHub','The average number of reported issues on all GitHub','The average number of owned projects','The average number of owned projects','The average number of owned projects','The average number of one-year sustained owned projects',
'The average number of owned one-year sustained projects','The average number of owned one-year sustained projects','The average number of owned two-year sustained projects','The average number of owned two-year sustained projects','The average number of owned two-year sustained projects','The average number of followers','The average number of followers','The average number of followers','The number of open issues three months after project creation','The ratio of open issues three months after project creation',
'The number of ``good first issues\'\' three months after project creation','The type of project owner account (0: organization, 1: user)','The number of stars three months after project creation','The number of forks three months after project creation','The number of project members three months after project creation','The ratio of core developers showing their affiliated companies/institutions','The ratio of peripheral developers showing their affiliated companies/institutions','The ratio of non-code contributors showing their affiliated companies/institutions','The average number of GitHub organizations core developers belong to','The average number of GitHub organizations peripheral developers belong to','The average number of GitHub organizations non-code contributors belong to',
'The number of README.md lines','The number of CONTRIBUTING.md lines',]

namelist=['corecmtmean','contributorcmt','corepr','contributorpr','coreiss','contributoriss','interesteriss','coreisscommenter','contributorisscommenter','interesterisscommenter','coreprcommenter','contributorprcommenter','interesterprcommenter','corecmtcommenter','contributorcmtcommenter','interestercmtcommenter','coreissevter', 'contributorissevter','interesterissevter',
'corefolling','contributorfolling', 'interesterfolling','corestarpronum', 'contributorstarpronum',  'interesterstarpronum','actday','eachdmedian','frontcmt', 'endcmt','eachdstd','commiterstd',
'coreallcmt','contributorallcmt','interesterallcmt','coreallpr','contributorallpr','interesterallpr','corealliss','contributoralliss','interesteralliss','corepronum','contributorpronum','interesterpronum','coreoveryearnum','contributoroveryearnum','coreover2yearnum','interesteroveryearnum','contributorover2yearnum','interesterover2yearnum','corefoll','contributorfoll','interesterfoll','openiss','openissratio',  'gfinum',
'type','numwat','fork', 'nummem', 'corehascomp','contributorhascomp', 'interesterhascomp','coreorgnum', 'contributororgnum', 'interesterorgnum',
'readme','contributing',
]

featurelist=[
'\#cmt\_c','\#cmt\_p','\#pr\_c','\#pr\_p','\#issue\_c','\#issue\_p','\#issue\_n','\#iss\_comment\_c','\#iss\_comment\_p','\#iss\_comment\_n','\#pr\_comment\_c','\#pr\_comment\_p','\#pr\_comment\_n','\#cmt\_comment\_c','\#cmt\_comment\_p','\#cmt\_comment\_n','\#iss\_event\_c','\#iss\_event\_p','\#iss\_event\_n','\#following\_c','\#following\_p','\#following\_n','\#star\_pro\_c','\#star\_pro\_p','\#star\_pro\_n',
'\#cmt\_actday','\#cmt\_median','\#cmt\_front','\#cmt\_end','cmt\_day\_std', 'cmt\_dev\_std','\#cmt\_all\_c','\#cmt\_all\_p','\#cmt\_all\_n','\#pr\_all\_c','\#pr\_all\_p','\#pr\_all\_n','\#issue\_all\_c','\#issue\_all\_p','\#issue\_all\_n','\#pro\_c','\#pro\_p','\#pro\_n','\#pro\_oneyear\_c','\#pro\_oneyear\_p','\#pro\_oneyear\_n','\#pro\_twoyear\_c','\#pro\_twoyear\_p','\#pro\_twoyear\_n','\#follower\_c','\#follower\_p','\#follower\_n','\#iss\_open','iss\_open\_ratio','\#GFI',
'type','\#star','\#fork','\#member','show\_comp\_c','show\_comp\_p','show\_comp\_n','\#org\_c','\#org\_p','\#org\_n',
'\#line\_readme','\#line\_contributing'
]

new_featurelist=[
'\#cmt\_c','\#pr\_c','\#issue\_c','\#iss\_comment\_c','\#cmt\_comment\_c','\#iss\_event\_c','\#following\_c','\#star\_pro\_c',
'\#cmt\_p','\#pr\_p','\#issue\_p','\#iss\_comment\_p','\#cmt\_comment\_p','\#iss\_event\_p','\#following\_p','\#star\_pro\_p',
'\#issue\_n','\#iss\_comment\_n','\#cmt\_comment\_n','\#iss\_event\_n','\#following\_n','\#star\_pro\_n',
'\#cmt\_actday','\#cmt\_median','\#cmt\_front','\#cmt\_end','cmt\_day\_std', 'cmt\_dev\_std',
'\#cmt\_all\_c','\#pr\_all\_c','\#issue\_all\_c','\#pro\_c','\#pro\_oneyear\_c','\#pro\_twoyear\_c','\#follower\_c',
'\#cmt\_all\_p','\#pr\_all\_p','\#issue\_all\_p','\#pro\_p','\#pro\_oneyear\_p','\#pro\_twoyear\_p','\#follower\_p',
'\#cmt\_all\_n','\#pr\_all\_n','\#issue\_all\_n','\#pro\_n','\#pro\_oneyear\_n','\#pro\_twoyear\_n','\#follower\_n',
'\#iss\_open','iss\_open\_ratio','\#GFI','\#line\_readme','\#line\_contributing',
'show\_comp\_c','\#org\_c',
'show\_comp\_p','\#org\_p',
'show\_comp\_n','\#org\_n',
'type','\#star','\#fork','\#member'
]

def effect_size(a,b):
    U1, p = mannwhitneyu(a, b, alternative='two-sided')
    nx, ny = len(a), len(b)
    U2 = nx*ny - U1
    U = min(U1, U2)
    N = nx + ny
    z = abs((U - nx*ny/2 + 0.5) / np.sqrt(nx*ny * (N + 1)/ 12))
    return Decimal(float(z/np.sqrt(N))).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)

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

def takelast(elem):
    return elem[-1]

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
                if m[1]<=0:
                    lilst[0].append(i)
                break
    return [lilst,n]

m=3
t=2
k=1
df=pd.read_pickle("./data/X_test_m"+str(m)+"_t"+str(t)+"_k"+str(k)+".pkl")
y_test=pd.read_pickle("./data/y_test_m"+str(m)+"_t"+str(t)+"_k"+str(k)+".pkl")
df.reset_index(drop=True,inplace=True)
y_test.reset_index(drop=True,inplace=True)
df['oneyear']=y_test
df0=df[df['oneyear']==0]
df1=df[df['oneyear']==1]
limedf=pd.read_pickle("./data/limeres_m"+str(m)+"_t"+str(t)+"_k"+str(k)+".pkl")
namelistind=[[i] for i in range(len(namelist))]
with mp.Pool(20) as pool:
    res=pool.starmap(get_lime_list, namelistind)
    res.sort(key=takelast)
    lime_list=[i[0] for i in res]

for x in range(len(new_featurelist)):
    i=featurelist.index(new_featurelist[x])
    if featurelist[i]=='\#cmt\_c':
        print("\midrule")
        print('\\parbox[t]{-2mm}{\\multirow{31}{*}{\\rotatebox[origin=c]{90}{\\textbf{Willingness of Participants}}}}&\\parbox[t]{-2mm}{\\multirow{9}{*}{\\rotatebox[origin=c]{90}{Core}}}')
    if featurelist[i]=='\#cmt\_all\_c':
        print("\midrule")
        print('\\parbox[t]{-2mm}{\\multirow{21}{*}{\\rotatebox[origin=c]{90}{\\textbf{Capacity of Participants}}}}&\\parbox[t]{-2mm}{\\multirow{7}{*}{\\rotatebox[origin=c]{90}{Core}}}')
    if featurelist[i]=='\#iss\_open':
        print("\midrule")
        print('\\parbox[t]{-2mm}{\\multirow{5}{*}{\\rotatebox[origin=c]{90}{\\textbf{Oppo.}}}}')
    if featurelist[i]=='show\_comp\_c':
        print("\midrule")
        print('\\parbox[t]{-2mm}{\\multirow{10}{*}{\\rotatebox[origin=c]{90}{\\textbf{Control Variables}}}}&')

    if featurelist[i]=='\#cmt\_p':
        print('\\cline{3-7}&\\parbox[t]{-2mm}{\\multirow{9}{*}{\\rotatebox[origin=c]{90}{Peripheral}}}')
    if featurelist[i]=='\#issue\_n':
        print('\\cline{3-7}&\\parbox[t]{-2mm}{\\multirow{7}{*}{\\rotatebox[origin=c]{90}{Non-code}}}')
    if featurelist[i]=='\#cmt\_actday':
        print('\\cline{3-7}&')
    if featurelist[i]=='\#cmt\_all\_p':
        print('\\cline{3-7}&\\parbox[t]{-2mm}{\\multirow{7}{*}{\\rotatebox[origin=c]{90}{Peripheral}}}')
    if featurelist[i]=='\#cmt\_all\_n':
        print('\\cline{3-7}&\\parbox[t]{-2mm}{\\multirow{7}{*}{\\rotatebox[origin=c]{90}{Non-code}}}')
    if featurelist[i]=='show\_comp\_p':
        print('\\cline{3-7}&')
    if featurelist[i]=='show\_comp\_n':
        print('\\cline{3-7}&')
    if featurelist[i]=='type':
        print('\\cline{3-7}&')

    if featurelist[i] not in ['\#cmt\_c','\#cmt\_all\_c','show\_comp\_c','\#cmt\_p','\#issue\_n','\#cmt\_actday','\#cmt\_all\_p','\#cmt\_all\_n','show\_comp\_p','show\_comp\_n','type']:
        print('&')


    
    signlist=df[namelist[i]].values.tolist()
    signlist=np.array(signlist)
    neglist=list(signlist[lime_list[i][0]])
    poslist=list(signlist[lime_list[i][1]])

    if namelist[i] in ['coreallcmt','contributorallcmt','interesterallcmt']:
        decimalstr="0.0"
    else:
        decimalstr="0.00"

    if neglist==[] or poslist==[]:
        signarrow="\\NoEffect"
        print("&"+featurelist[i]+"&"+meaning[i]+"&"
            +str(Decimal(float(median(neglist))).quantize(Decimal(decimalstr), rounding=ROUND_HALF_UP))+"/"+str(Decimal(float(0.00)).quantize(Decimal(decimalstr), rounding=ROUND_HALF_UP))+"&"+str(Decimal(float(0.00)).quantize(Decimal(decimalstr), rounding=ROUND_HALF_UP))+"/"+str(Decimal(float(0.00)).quantize(Decimal(decimalstr), rounding=ROUND_HALF_UP))+"\hspace{1.09mm} "+"("+str(0.00)+")"+signarrow+"\\\\"
            )
    else:
        if median(neglist)>median(poslist) or mean(neglist)>mean(poslist):
            signarrow="\\DownArrow"
        elif median(neglist)==median(poslist) and mean(neglist)==mean(poslist):
            signarrow="\\NoEffect"
        else:
            signarrow="\\UpArrow"

        if effect_size(neglist,poslist)<0.1:
            signarrow="\\NoEffect"
        elif effect_size(neglist,poslist)>=0.1 and effect_size(neglist,poslist)<0.3:
            signarrow+="Medium"
        else:
            signarrow+="Large"

        if stats.mannwhitneyu(neglist,poslist,alternative='two-sided')[1]<0.00078:
            print("&"+featurelist[i]+"&"+meaning[i]+"&"
            +str(Decimal(float(median(neglist))).quantize(Decimal(decimalstr), rounding=ROUND_HALF_UP))+"/"+str(Decimal(float(mean(neglist))).quantize(Decimal(decimalstr), rounding=ROUND_HALF_UP))+"&"+str(Decimal(float(median(poslist))).quantize(Decimal(decimalstr), rounding=ROUND_HALF_UP))+"/"+str(Decimal(float(mean(poslist))).quantize(Decimal(decimalstr), rounding=ROUND_HALF_UP))+"$^*$"+"&"+str(effect_size(neglist,poslist))+signarrow+"\\\\"
            )
        else:
            print("&"+featurelist[i]+"&"+meaning[i]+"&"
            +str(Decimal(float(median(neglist))).quantize(Decimal(decimalstr), rounding=ROUND_HALF_UP))+"/"+str(Decimal(float(mean(neglist))).quantize(Decimal(decimalstr), rounding=ROUND_HALF_UP))+"&"+str(Decimal(float(median(poslist))).quantize(Decimal(decimalstr), rounding=ROUND_HALF_UP))+"/"+str(Decimal(float(mean(poslist))).quantize(Decimal(decimalstr), rounding=ROUND_HALF_UP))+"\hspace{1.09mm} "+"&"+str(effect_size(neglist,poslist))+signarrow+"\\\\"
            )