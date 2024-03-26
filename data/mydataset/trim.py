import json
import random
def getFMdataset(path='./traindata.json'):
    with open(path,encoding='gbk') as f:
        data=json.load(f)
    newdatas=[]
    for i in data:
        if not i['父本']==[]:
            newdatas.append(i)
        else:
            if random.random()<0.4:
                newdatas.append(i)
    
    with open('fmData.json','w',encoding='gbk') as f:
        json.dump(newdatas,f,ensure_ascii=False)


if __name__=='__main__':
    getFMdataset()