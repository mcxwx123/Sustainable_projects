import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
import pandas as pd
import multiprocessing as mp
from statistics import median
from utils import data_utils

class XGB:
    def __init__(self, df,model_name,fold):
        self.df=df
        self.model_name=model_name
        self.fold=fold

    def run(self):
        global metric
        X_train, X_test, y_train, y_test = data_utils.load_train_test_data(self.df,self.model_name,self.fold)

        del X_train['project_id']
        del X_test['project_id']
        if self.model_name=="Logistic_regression":
            model = LogisticRegression(max_iter=10000)
        elif self.model_name=="Random_forest":
            model = RandomForestClassifier(n_estimators=10, criterion='gini')
        else:
            model = XGBClassifier(use_label_encoder=False,eval_metric=['logloss','auc','error'])    
        model.fit(X_train,y_train)
        y_score=model.predict_proba(X_test)[:,1]
        auc=data_utils.get_auc(y_test,y_score)
        metric = np.array(metric) + np.array([auc])

def checklife(a,b,c,rtn):
    add=0
    if a!=0:
        onecmt=a
        startt=b
        onecmt=[d for d in onecmt if (d-startt)/86400000<=365*m]
        if onecmt!=0 and c>365*m:
            eachmo=[]
            onecmt=[d for d in onecmt if (d-startt)/86400000<=365*m]
            for t in range(12*m):
                cmtnum=0
                for ind in range(len(onecmt)):
                    det=onecmt[ind]-startt
                    if det/86400000>=t*30.42 and det/86400000<t*30.42+30.42:
                        cmtnum+=1
                        if cmtnum==2*k:
                            break
                eachmo.append(cmtnum)
            if median(eachmo)>=k:
                add=1
    return [add,rtn]

def takelast(elem):
    return elem[-1]

def strictlife(df):
    cmtt=df["cmtt"].values
    lifeday=df["lifeday"].values
    startT=df["startT"].values
    checkdata=[[cmtt[i],startT[i],lifeday[i],i] for i in range(len(cmtt))]
    with mp.Pool(max(mp.cpu_count() // 2,1)) as pool:
        res = pool.starmap(checklife, checkdata)
        res.sort(key=takelast)
        res=[i[0] for i in res]
    return pd.DataFrame(res)   

if __name__ == '__main__':
    global metric
    
    model_names=["Complete_XGB","common","other","Logistic_regression","Random_forest","only_specific","only_patt","only_Interest","only_General","only_Popularity","only_chance","only_control"]
    #Table III
    for m in [1,3,5]:
        df = pd.read_pickle("./data/prodata_"+str(m)+".pkl")
        del df["oneyear"]
        model_name="Complete_XGB"
        for t in [1,2]:
            for k in [1,2,6]:
                datadf=df.copy(deep=True)
                datadf.insert(0,'oneyear',strictlife(datadf))
                metric=[0]
                for fold in range(10):
                    model = XGB(datadf,model_name,fold)
                    model.run()
                metric = [x/10 for x in metric]
                print("m="+str(m)+", t="+str(t)+", k="+str(k)+", auc="+str(metric[0]))
    
    #Table IV
    df = pd.read_pickle("./data/prodata_3.pkl")
    del df["oneyear"]
    printlist=[]
    datadf=df.copy(deep=True)
    t=2
    k=1
    datadf.insert(0,'oneyear',strictlife(datadf))
    for model_name in model_names:
        print(model_name)
        metric=[0]
        for fold in range(10):
            model = XGB(datadf,model_name,fold)
            model.run()
        metric = [x/10 for x in metric]
        print(metric)
        printlist.append(metric)
    for i in range(len(model_names)):
        print(model_names[i],printlist[i])