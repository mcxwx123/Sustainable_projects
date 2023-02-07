import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve
from sklearn.metrics import auc

def get_auc(eval_labels, scores):
    fpr, tpr, thresholds_keras = roc_curve(eval_labels,scores)
    auc_ = auc(fpr, tpr)
    return auc_

def unflod(df,s):
    df=df[s].values
    lst=[]
    for i in df:
        dic={}
        for j in range(len(i)):
            dic[j]=i[j]
        lst.append(dic)
    return pd.DataFrame(lst)

def getmean(l):
    return np.mean(l)

def getmedian(l):
    return np.median(l)

def getstd(l):
    return np.std(l)


def load_train_test_data(df,model_name,fold):
    c=list(df.columns)
    df.reset_index(drop=True,inplace=True)
    if 'eachdaycmt' in c:
        df.insert(0,'eachdmean',df["eachdaycmt"].apply(getmean))
        df.insert(0,'eachdmedian',df["eachdaycmt"].apply(getmedian))
        df.insert(0,'eachdstd',df["eachdaycmt"].apply(getstd))
        del df['eachdaycmt']
    T=pd.concat([df],axis=1)
    c=list(df.columns)
    T.columns=c
    T.reset_index(drop=True,inplace=True)
    corecap=unflod(T,"corecap")
    del T['corecap']
    c=list(T.columns)
    T=pd.concat([T,corecap],axis=1)
    c+=['corepronum','coreallcmt','corefoll','corealliss','coreallpr','coreactpronum','coreoveryearnum','coreover2yearnum']
    T.columns=c

    corewill=unflod(T,"corewill")
    del T['corewill']
    c=list(T.columns)
    T=pd.concat([T,corewill],axis=1)
    c+=['corecmtmean','corepr','coreiss','corefolling','corehascomp','corestarpronum','coreorgnum','coreisscommenter','coreissevter','coreprcommenter','corecmtcommenter']
    T.columns=c
   

    contributorcap=unflod(T,"contributorcap")
    interestercap=unflod(T,"interestercap")
    del T['contributorcap']
    del T['interestercap']
    c=list(T.columns)
    T=pd.concat([T,contributorcap],axis=1)
    T=pd.concat([T,interestercap],axis=1)
    c+=['contributorpronum','contributorallcmt','contributorfoll','contributoralliss','contributorallpr','contributoractpronum','contributoroveryearnum','contributorover2yearnum']
    c+=['interesterpronum','interesterallcmt','interesterfoll','interesteralliss','interesterallpr','interesteractpronum','interesteroveryearnum','interesterover2yearnum']
    T.columns=c

    contributorwill=unflod(T,"contributorwill")
    interesterwill=unflod(T,"interesterwill")
    del T['contributorwill']
    del T['interesterwill']
    c=list(T.columns)
    T=pd.concat([T,contributorwill],axis=1)
    T=pd.concat([T,interesterwill],axis=1)
    c+=['contributorcmt','contributorpr','contributoriss','contributorfolling','contributorhascomp','contributorstarpronum','contributororgnum','contributorisscommenter','contributorissevter','contributorprcommenter','contributorcmtcommenter']
    c+=['interesteriss','interesterfolling','interesterhascomp','interesterstarpronum','interesterorgnum','interesterisscommenter','interesterissevter','interesterprcommenter','interestercmtcommenter']
    T.columns=c


    if model_name in ["Logistic_regression","Random_forest","Complete_XGB"]:
        pro=T[['corecmtmean','corepr','coreiss','coreisscommenter','coreissevter','coreprcommenter','corecmtcommenter','contributorcmt','contributorpr','contributoriss','contributorisscommenter','contributorissevter','contributorprcommenter','contributorcmtcommenter',
        'interesteriss','interesterisscommenter','interesterissevter','interesterprcommenter','interestercmtcommenter','actday','eachdmedian','eachdstd','frontcmt', 'endcmt', 'commiterstd',
        'corefolling','corestarpronum','contributorfolling','contributorstarpronum','interesterfolling','interesterstarpronum','corepronum','coreallcmt','corealliss','coreallpr','coreoveryearnum','coreover2yearnum',
        'contributorpronum','contributorallcmt','contributoralliss','contributorallpr','contributoroveryearnum','contributorover2yearnum','interesterpronum','interesterallcmt','interesteralliss','interesterallpr','interesteroveryearnum','interesterover2yearnum',
        'corefoll','contributorfoll','interesterfoll','openiss', 'openissratio','gfinum','readme','hasreadme','contributing','hascontributing','codeofconduct','hasconduct','corecmt', 'leftcmt', 'ratiocmt','daycmtnum','cmtratio','eachdmean','merget','bugnum','enhancementnum','helpwantednum','labelnum','cmtpeople',
        'fork','type', 'numwat','nummem', 'corehascomp', 'coreorgnum', 'contributorhascomp', 'contributororgnum', 'interesterhascomp', 'interesterorgnum',"oneyear",'project_id'
        ]]

    elif model_name=="only_specific":
        pro=T[['corecmtmean','corepr','coreiss','coreisscommenter','coreissevter','coreprcommenter','corecmtcommenter','contributorcmt','contributorpr','contributoriss','contributorisscommenter','contributorissevter','contributorprcommenter','contributorcmtcommenter',
        'interesteriss','interesterisscommenter','interesterissevter','interesterprcommenter','interestercmtcommenter',"oneyear",'project_id'
        ]]
    elif model_name=="only_patt":
        pro=T[['actday','eachdmedian','eachdstd','corecmt', 'leftcmt', 'frontcmt', 'endcmt', 'ratiocmt','daycmtnum','cmtratio','eachdmean','merget','commiterstd',"oneyear",'project_id'
        ]]
    elif model_name=="only_Interest":
        pro=T[['corefolling','corestarpronum','contributorfolling','contributorstarpronum','interesterfolling','interesterstarpronum',"oneyear",'project_id'
        ]]
    elif model_name=="only_General":
        pro=T[['corepronum','coreallcmt','corealliss','coreallpr','coreoveryearnum','coreover2yearnum','contributorpronum','contributorallcmt','contributoralliss','contributorallpr','contributoroveryearnum','contributorover2yearnum','interesterpronum','interesterallcmt','interesteralliss','interesterallpr','interesteroveryearnum','interesterover2yearnum',"oneyear",'project_id'
        ]]
    elif model_name=="only_Popularity":
        pro=T[['corefoll','contributorfoll','interesterfoll',"oneyear",'project_id'
        ]]
    elif model_name=="only_control":
        pro=T[['fork','type', 'numwat','nummem', 'cmtpeople','corehascomp', 'coreorgnum', 'contributorhascomp', 'contributororgnum', 'interesterhascomp', 'interesterorgnum',"oneyear",'project_id'
        ]]
    elif model_name=="only_chance":
        pro=T[['openiss', 'openissratio','gfinum','readme','hasreadme','contributing','hascontributing','codeofconduct','hasconduct',"oneyear",'project_id'
        ]]
    elif model_name=="common":
        pro=T[['corecmtmean','coreiss','contributorcmt','contributoriss',
        'interesteriss','type','nummem',"oneyear",'project_id'
        ]]
    elif model_name=="other":
        pro=T[['corepr','coreisscommenter','coreissevter','coreprcommenter','corecmtcommenter','contributorpr','contributorisscommenter','contributorissevter','contributorprcommenter','contributorcmtcommenter',
        'interesterisscommenter','interesterissevter','interesterprcommenter','interestercmtcommenter','actday','eachdmedian','eachdstd','frontcmt', 'endcmt', 'commiterstd',
        'corefolling','corestarpronum','contributorfolling','contributorstarpronum','interesterfolling','interesterstarpronum','corepronum','coreallcmt','corealliss','coreallpr','coreoveryearnum','coreover2yearnum',
        'contributorpronum','contributorallcmt','contributoralliss','contributorallpr','contributoroveryearnum','contributorover2yearnum','interesterpronum','interesterallcmt','interesteralliss','interesterallpr','interesteroveryearnum','interesterover2yearnum',
        'corefoll','contributorfoll','interesterfoll','openiss', 'openissratio','gfinum','readme','hasreadme','contributing','hascontributing','codeofconduct','hasconduct','corecmt', 'leftcmt', 'ratiocmt','daycmtnum','cmtratio','eachdmean','merget','bugnum','enhancementnum','helpwantednum','labelnum','cmtpeople',
        'fork','numwat', 'corehascomp', 'coreorgnum', 'contributorhascomp', 'contributororgnum', 'interesterhascomp', 'interesterorgnum',"oneyear",'project_id'
        ]]

    p_train_split1=int((fold/10)*pro.shape[0])
    p_train_split2=int((fold/10+0.1)*pro.shape[0])
    train_data1=pro.iloc[:p_train_split1]
    train_data2=pro.iloc[p_train_split2:]
    train_data=pd.concat([train_data1,train_data2],axis=0)
    test_data=pro.iloc[p_train_split1:p_train_split2]
    p_train = train_data[train_data.oneyear == 1]
    n_train = train_data[train_data.oneyear == 0]
    train_data=pd.concat([p_train,n_train],ignore_index=True)
    y_train=train_data['oneyear']
    y_test=test_data['oneyear']

    del train_data['oneyear']
    del test_data['oneyear']
    X_train=train_data
    X_test=test_data

    return X_train, X_test, y_train, y_test