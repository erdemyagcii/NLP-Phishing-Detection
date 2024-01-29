import trafilatura
import torch
import os
import chardet
import numpy as np
import argparse


from googletrans import Translator
from sentence_transformers import SentenceTransformer


path1 = "PhishIntention\\Legitimate"
path2 = "PhishIntention\\Phishing"

legitimates = list()
phishings = list()


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def get_html_content(file_path):
    result = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            result = trafilatura.extract(html_content)
            result = str(result)
    except:#patlarsa exceptin içindeki with opena da try except at
        print("encoding type detecting...")
        try:
            enc = detect_encoding(file_path)
        except:
            pass
        try:
            with open(file_path, 'r', encoding=enc) as file:
                html_content = file.read()
                result = trafilatura.extract(html_content)
                result = str(result)
        except:
            result = ""
    return result

def translate(sentence):
    translator = Translator()
    result = translator.translate(sentence, dest = "en").text
    return result

def ST(sentences, transformer):
    if transformer == "xlm-roberta":
        model = SentenceTransformer('aditeyabaral/sentencetransformer-xlm-roberta-base', device='cuda')
    elif transformer == "sbert":
        model = SentenceTransformer('sentence-transformers/bert-base-nli-mean-tokens', device='cuda')
    #electrayı da ekle
    embeddings = model.encode(sentences)
    #print("finished")
    return embeddings


def generate_embeedings(folder_path, transformer, type):
    global legitimates
    global phishings
    done = 0
    fail = 0
    files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    i = 0
    for file in files:
        file_path = os.path.join(folder_path, file)
  
        html_content = get_html_content(file_path)
        if html_content != "" and html_content != None:#buraları teslimden önce silersin decode sorunlarına karşı bi önlem
            if transformer == "electra" or transformer == "sbert":
                print(file, "translating...")
                try:
                    translated_content = translate(html_content)
                except:
                    print("Moving to the next data due to translation problem of current data...")
                    continue
                print("done.")
                print(file, "transforming...")
                try:
                    result = ST(translated_content, transformer)
                except:
                    print("Invalid Sentence Transformer!")
                    exit()
                if type == "legitimate":
                    legitimates.append(result)
                else:
                    phishings.append(result)
                print("done.")
                done += 1
            else:
                print("done.\ntransforming...")
                try:
                    result = ST(html_content, transformer)
                except:
                    print("Invalid Sentence Transformer!")
                    exit()
                if type == "legitimate":
                    legitimates.append(result)
                else:
                    phishings.append(result)
                print("done.")
                done += 1
        else:
            fail += 1
        print("turn: ", i)
        i += 1
        print(type, " succesful: ", done, "failed: ", fail)






    try:
        os.makedirs('embeddings')
    except FileExistsError:
        pass
    if type == "legitimate":
        fname = '_'.join(transformer) + '_legitimate_vectors.npy'
        pth = os.path.join('embeddings', fname)
        np.save(pth, legitimates)#bu pathe nlpi modelini de ekle
    else:            
        fname = '_'.join(transformer) + '_phishing_vectors.npy'
        pth = os.path.join('embeddings', fname)
        np.save(pth, phishings)#bu pathe nlpi modelini de ekle

    
        
        

parser = argparse.ArgumentParser()
parser.add_argument('-transformer', type=str)

args = parser.parse_args()
# -transformer argümanı girilmişse ve bir değer verilmişse nlp_model değişkenine ata
if args.transformer:
    nlp_model = args.transformer
else:
    #default
    nlp_model = "sbert"

generate_embeedings(path1, nlp_model,  "legitimate" )
generate_embeedings(path2, nlp_model, "phishing")



















  

