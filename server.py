from flask import Flask, render_template, request
import xgboost as xgb
import joblib
import os

import trafilatura
import chardet
from sentence_transformers import SentenceTransformer
from googletrans import Translator
import numpy as np
import pickle


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

def ST(sentences, transformer):
    if transformer == "Roberta":
        model = SentenceTransformer('aditeyabaral/sentencetransformer-xlm-roberta-base')
    elif transformer == "Bert":
        model = SentenceTransformer('sentence-transformers/bert-base-nli-mean-tokens')
    #electrayı da ekle
    embedding = model.encode(sentences)
    #print("finished")
    return embedding

def translate(sentence):
    translator = Translator()
    result = translator.translate(sentence, dest = "en").text
    return result

def produce_vector(file, transformer):
    translated_content = ""
    html_content = get_html_content(file)
    #print(html_content)
    if html_content != "" and html_content != None:#buraları teslimden önce silersin decode sorunlarına karşı bi önlem
        if transformer == "Electra" or transformer == "Bert":
            print(file, "translating...")
            try:
                translated_content = translate(html_content)
                print(translated_content)
            except:
                print("done.")
            print(file, "transforming...")
            result = ST(translated_content, transformer)
            print("done.")
        else:
            print("done.\ntransforming...")
            result = ST(html_content, transformer)
    return result






app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])

def predict():
    prediction_result = "Phishing" # or it will be "Legitimate"
    if 'htmlFile' not in request.files:
        return "No file part"
    
    file = request.files['htmlFile']

    if file.filename == '':
        return "No selected file"

  
    file_path = 'test/' + file.filename
    file.save(file_path)

    # START of the business logic here
    # Perform prediction using the file_path with your XGBoost model
    # Replace the following line with your actual prediction logic
    
    #model = joblib.load('model\\xgb_model.pkl')
    with open('model\\xgb_model.pkl', 'rb') as xgb_file:
        xgb_model = pickle.load(xgb_file)
    with open('model\\catboost_model.pkl', 'rb') as catboost_file:
        catboost_model = pickle.load(catboost_file)

    def predict_phishing_legitimate(input_vector):
     
        input_vector = np.array(input_vector).reshape(1, -1)

       
        
        xgb_prediction = xgb_model.predict(input_vector)
        catboost_prediction = catboost_model.predict(input_vector)

      
        return xgb_prediction[0], catboost_prediction[0]
    
    sample_vector = produce_vector(file_path, "Bert")#you must change it if you used another st in training session ex.roberta
    xgb_result, catboost_result = predict_phishing_legitimate(sample_vector)

    if xgb_result == 1:#you can use catboost_result too, choose whose accuracy is higher
        prediction_result = "Phishing"
    else:
        prediction_result = "Legitimate"
    # END of the business logic here
   

    return f"{file_path} is {prediction_result}"

if __name__ == '__main__':
    app.run(debug=True, port=5050)