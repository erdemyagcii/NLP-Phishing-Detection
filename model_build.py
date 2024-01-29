import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
import pickle
import argparse
import os

def load_embeddings(embedding_file):
    return np.load(embedding_file)

def train_and_evaluate_model(algorithm, X_train, y_train, X_test, y_test):
    if algorithm == 'xgb':
        model = XGBClassifier()
    elif algorithm == 'cat':
        model = CatBoostClassifier()
    else:
        raise ValueError("Invalid algorithm. Please choose 'xgb' or 'cat'.")

    model.fit(X_train, y_train)
    y_test_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_test_pred)
    precision = precision_score(y_test, y_test_pred)
    recall = recall_score(y_test, y_test_pred)
    f1 = f1_score(y_test, y_test_pred)

    return model, accuracy, precision, recall, f1

def save_model(model, file_path):
    with open(file_path, 'wb') as model_file:
        pickle.dump(model, model_file)

def main():
    parser = argparse.ArgumentParser(description="Train and evaluate an ML model.")
    parser.add_argument('-algorithm', choices=['xgb', 'cat'], help="ML algorithm selection ('xgb' or 'cat')", required=True)
    parser.add_argument('-phishingEmbeddings', help="Relative path to the phishing embedding file stored in the 'embeddings' folder", required=True)
    parser.add_argument('-legitimateEmbeddings', help="Relative path to the legitimate embedding file stored in the 'embeddings' folder", required=True)

    args = parser.parse_args()

    phishing_embeddings = load_embeddings(os.path.join('embeddings', args.phishingEmbeddings))
    legitimate_embeddings = load_embeddings(os.path.join('embeddings', args.legitimateEmbeddings))
    phishing_labels = np.ones(len(phishing_embeddings))
    legitimate_labels = np.zeros(len(legitimate_embeddings))
    x = np.concatenate([phishing_embeddings, legitimate_embeddings], axis=0)
    y = np.concatenate([phishing_labels, legitimate_labels])
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, shuffle=True)


    print("model building...")
    model, accuracy, precision, recall, f1 = train_and_evaluate_model(args.algorithm, X_train, y_train, X_test, y_test)

    print(f"{args.algorithm.capitalize()} Training Performance:")
    print(f"Accuracy: {accuracy:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}, F1 Score: {f1:.4f}")

  
    try:
        os.makedirs('model')
    except FileExistsError:
        pass
    save_model(model, f'model\\{args.algorithm}_model.pkl')

if __name__ == "__main__":
    main()
