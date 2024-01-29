# NLP-Phishing-Detection
Detecting phishing websites using NLP models

If you are not interested in ai training part(Who just wants to use this tool):
First of all you should import the necessary libs as most cureent versions in the server.py:

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

After that you can run this server by:
$ python server.py
And you should paste the url that given by server to your browser then you must paste your html file to test folder.
Now you are ready to detect this html is phishing or not.

If you are interested in ai training part:

Summary:
Firstly, I implemented this project on a system with NVIDIA GEFORCE 940m-2gb 
GPU, running Windows and a 64-bit architecture. Next, I handled the Data Preparation 
phase, cleaning up files other than those named html.txt and renaming these html.txt files 
to new names (e.g., 1.txt, 2.txt). I organized them into two new folders (Legitimate and 
Phishing folders). Subsequently, I completed the installation of requirements such as 
cuda, pytorch, sentence transformers, etc.
Afterwards, I processed these html.txt files through Trafilatura to extract their text 
content. If necessary (e.g., for BERT), I translated the content into English using the 
Google Translate API. Then, I fed this text into the relevant NLP-Sentence Transformer 
models (BERT and XML-RoBERTa) to generate embeddings. I separated these vectors 
into innocent and malicious categories, storing them in separate NPY files.
Next, I used these embedding NPY files as input for Cat and XGBoost classifiers, 
resulting in two models. With these models, I could now make predictions. I created a 
server using these models, established communication with a client, and turned the 
project into a usable product.

Omissions and violations:
1) I did not use Electra.
2) I could not use Roberta because the generation time was approximately 120 hours due to 
the hardware's limitations. Therefore, I only used BERT(30-35 hour).
3) I stored the embeddings in two files, not a single file. Additionally, the file format is 
NPY, not PKL. When running the prepare_embedding.py file, use the structure specified 
in the image.
4) I couldn't finish the part where the selected file is automatically moved to the test folder. 
Therefore, the selected HTML file needs to be manually placed in the test folder.

Conclusion:
1) I fixed the xgboost algorithm in the code because it has a higher accuracy, but if you 
want, you can switch to cat with a few lines of code changes.
2) Please try not to manipulate the file and folder structure I provided. Don't forget to 
manually create a test folder and place the HTML file in it. Also, do not delete any files 
from the model folder because both models need to be in their proper locations for the 
respective script to function.
