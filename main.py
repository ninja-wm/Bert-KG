# -*- coding: utf-8 -*-
# @Author : lishouxian
# @Email : gzlishouxian@gmail.com
# @File : main.py
# @Software: PyCharm
import json
from logging import info
from engines.utils.logger import get_logger
from configure import Configure
from engines.train import train
from engines.model import Model
from transformers import BertTokenizer, BertModel
from engines.predict import predict_one
import argparse
import os
import torch


def fold_check(configures):
    checkpoints_dir = 'checkpoints_dir'
    if not os.path.exists(configures.checkpoints_dir) or not hasattr(configures, checkpoints_dir):
        print('checkpoints fold not found, creating...')
        paths = configures.checkpoints_dir.split('/')

        if len(paths) == 2 and os.path.exists(paths[0]) and not os.path.exists(configures.checkpoints_dir):
            os.mkdir(configures.checkpoints_dir)
        else:
            try:
                os.mkdir('checkpoints')
            except:
                pass

    log_dir = 'log_dir'
    if not os.path.exists(configures.log_dir) or not hasattr(configures, log_dir):
        print('log fold not found, creating...')
        os.mkdir(configures.log_dir)



def genTriple(configs, tokenizer, model, device,path='./rawData.json',):
    infoDict=dict()
    with open(path,encoding='gbk')as f:
        rawData=json.load(f)
    for key in rawData.keys():
        seqList=rawData[key]
        for seq in seqList:
            if seq.split('：')[0]=='栽培技术要点':
                continue
            try:
                result=predict_one(configs, tokenizer, seq, model, device)
            except:
                continue
            if not key in infoDict.keys():
                infoDict[key]=dict()
                infoDict[key]['父本']=[]
                infoDict[key]['母本']=[]
                infoDict[key]['表型']=[]
                infoDict[key]['环境']=[]

            try:
                infoDict[key]['父本']+=(result['父本'])
            except:
                pass
            
            try:
                infoDict[key]['母本']+=(result['母本'])
            except:
                pass
            
            try:
                infoDict[key]['表型']+=(result['表型'])
            except:
                pass
            
            try:
                infoDict[key]['环境']+=(result['环境'])
            except:
                pass

            
    with open('./triple.json','w',encoding='gbk') as f:
        json.dump(infoDict,f,ensure_ascii=False)
    






if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Entity extractor by binary tagging')
    parser.add_argument('--config_file', default='system.config', help='Configuration File')
    args = parser.parse_args()
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    print(device)
    configs = Configure(config_file=args.config_file)
    fold_check(configs)
    logger = get_logger(configs.log_dir)
    configs.show_data_summary(logger)
    
    mode = configs.mode.lower()
    print('---------mode----------',mode)
    if mode == 'train':
        logger.info('mode: train')
        train(configs, device, logger,reload=False)
    elif mode == 'interactive_predict':
        logger.info('mode: predict_one')
        tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
        bert_model = BertModel.from_pretrained('bert-base-chinese').to(device)
        num_labels = len(configs.class_name)
        model = Model(hidden_size=768, num_labels=num_labels).to(device)
        model.load_state_dict(torch.load(os.path.join(configs.checkpoints_dir, 'best_model.pkl')))
        model.eval()
        while True:
            logger.info('please input a sentence (enter [exit] to exit.)')
            sentence = input()
            if sentence == 'exit':
                break
            result = predict_one(configs, tokenizer, sentence, model, device)
            print(result)

    elif mode=='gentriple':
        print('True')
        tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
        bert_model = BertModel.from_pretrained('bert-base-chinese').to(device)
        num_labels = len(configs.class_name)
        model = Model(hidden_size=768, num_labels=num_labels).to(device)
        model.load_state_dict(torch.load(os.path.join(configs.checkpoints_dir, 'best_model.pkl')))
        model.eval()
        genTriple(configs, tokenizer, model, device)
        print(mode)