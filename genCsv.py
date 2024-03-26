import json

def genTripleCsv(inputPath='./triple.json'):
    with open(inputPath, encoding='gbk') as f:
        dic=json.load(f)
    
    inhirit=[]
    behave=[]
    env=[]

    for key in dic.keys():
        for i in dic[key]['父本']+dic[key]['母本']:
            inhirit.append(key+','+'源于,'+i)
        for i in dic[key]['表型']:
            behave.append(key+','+'表现,'+i)
        for i in dic[key]['环境']:
            env.append(key+','+'推广于,'+i)
    
    with open('geneT.csv','w') as f:
        for i in inhirit:
            f.write(i+'\n')

    with open('biaoxingT.csv','w') as f:
        for i in behave:
            f.write(i+'\n') 

    with open('envT.csv','w') as f:
        for i in env:
            f.write(i+'\n')
    

def genId(inputPath='./triple.json'):
    with open(inputPath, encoding='gbk') as f:
        dic=json.load(f)

    pingzhong=[]
    envs=[]
    biaoxing=[]
    pingzhong=list(set((list(dic.keys()))))
    for key in dic.keys():
        pingzhong+=(dic[key]['父本']+dic[key]['母本'])
        biaoxing+=dic[key]['表型']
        envs+=dic[key]['环境']
    
    pingzhong=list(set(pingzhong))
    biaoxing=list(set(biaoxing))
    envs=list(set(envs))
    ent=pingzhong+biaoxing+envs
    with open('ent.csv','w') as f:
        for i,j in enumerate(ent):
            f.write(str(i)+','+j+'\n')


if __name__=='__main__':
    # genTripleCsv()
    genId()