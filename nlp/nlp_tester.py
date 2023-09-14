import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


def nlp_title_classification(title):
        # Load the trained model and TF-IDF vectorizer
        with open("nlp/model.h5", "rb") as model:
                lr = joblib.load(model)
        with open("nlp/tfidf_vectorizer.pkl", "rb") as pkl:
                tfidf_vectorizer = joblib.load(pkl)

        user_input = title

        # Preprocess the user input using the TF-IDF vectorizer
        tfidf_input = tfidf_vectorizer.transform([user_input])

        # Predict using the model and get probability estimates
        predicted_probabilities = lr.predict_proba(tfidf_input)

                # Display the result with probability estimates
        classes = lr.classes_
        print('')
        for i, class_name in enumerate(classes):
                print(f'Probability for {class_name}: {predicted_probabilities[0, i]}')

        # Determine the predicted class based on probability thresholds
        threshold = 0.5  # You can adjust this threshold as needed
        predicted_class = classes[np.argmax(predicted_probabilities > threshold)]

                # Display the final classification
        print(f'\nProduct title: {title}\nClass: {predicted_class}\n')
        return predicted_class

        