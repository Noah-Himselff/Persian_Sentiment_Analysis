from flask import Flask, request
from joblib import load
from postman_cleaner import pre_process

app = Flask(__name__)
classifier = load('svm_model.joblib')
vectorizer = load('vectorizer.joblib')

@app.route('/classify', methods=['POST'])
def classify_sentence():
    data = request.get_json()
    sentence = data['sentence']
    # Apply pre-processing
    cleaned_sentence = pre_process(sentence)
    
    vector = vectorizer.transform([cleaned_sentence])


    # Classify using the SVM model
    prediction = classifier.predict(vector)

    print (cleaned_sentence)
    print(prediction)
    return {'prediction': prediction[0]}
if __name__ == '__main__':
    app.run(port=5000)
