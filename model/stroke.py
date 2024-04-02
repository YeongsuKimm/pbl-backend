# Importing required libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

class StrokeModel:
    """This class encompasses the stroke prediction model based on various patient factors."""
    
    _instance = None

    def __init__(self, csv_file):
        self.stroke_data = pd.read_csv(csv_file)
        self.model = None
        self.features = ['age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi']
        self.categorical_features = ['gender', 'ever_married', 'work_type', 'Residence_type']
        self.target = 'stroke'
        self.encoder = OneHotEncoder(drop='first')

    def _clean(self):
        # Fill missing values if any
        self.stroke_data.fillna(method='ffill', inplace=True)
        
        # One-hot encode categorical features
        encoded_features = pd.get_dummies(self.stroke_data[self.categorical_features], drop_first=True)
        self.stroke_data = pd.concat([self.stroke_data, encoded_features], axis=1)
        self.features.extend(encoded_features.columns)

    def _train(self):
        X = self.stroke_data[self.features]
        y = self.stroke_data[self.target]

        # Set minimum number of samples for training
        min_train_samples = 100

        # Split data into train and test sets with a minimum number of samples for training
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, 
                                                            shuffle=True, stratify=None)
        
        # Ensure that the training set has at least the minimum number of samples
        while len(X_train) < min_train_samples:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, 
                                                                shuffle=True, stratify=None)

        # Creating and training the logistic regression model
        self.model = LogisticRegression()
        self.model.fit(X_train, y_train)

        # Making predictions on the test set
        y_pred = self.model.predict(X_test)

        # Calculating accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print("Model accuracy:", accuracy)

    @classmethod
    def get_instance(cls, csv_file):
        if cls._instance is None:
            cls._instance = cls(csv_file)
            cls._instance._clean()
            cls._instance._train()
        return cls._instance

    def predict_stroke(self, patient):
        # Clean and prepare patient data for prediction
        patient_df = pd.DataFrame(patient, index=[0])

        # One-hot encode categorical features
        encoded_features = pd.get_dummies(patient_df[self.categorical_features], drop_first=True)
        patient_df = pd.concat([patient_df, encoded_features], axis=1)

        # Ensure the features are in the same order as in the training data
        patient_df = patient_df.reindex(columns=self.features, fill_value=0)

        # Predicting stroke probability
        stroke_probability = self.model.predict_proba(patient_df)
        return stroke_probability[:, 1][0]

def testStroke():
    print("Step 1: Define patient data for prediction:")
    patient_info = {
        'age': [67],
        'gender': ['Male'],
        'hypertension': [0],
        'heart_disease': [1],
        'ever_married': ['Yes'],
        'work_type': ['Private'],
        'Residence_type': ['Urban'],
        'avg_glucose_level': [228.69],
        'bmi': [36.6]
    }
    print("\t", patient_info)
    print()

    strokeModel = StrokeModel.get_instance("/Users/aiden/Downloads/healthcare-dataset-stroke-data 2.csv")
    print("Step 2:", StrokeModel.get_instance.__doc__)

    print("Step 3:", StrokeModel.predict_stroke.__doc__)
    stroke_probability = strokeModel.predict_stroke(patient_info)
    print('\t Predicted stroke probability:', stroke_probability)
    print()

if __name__ == "__main__":
    print("Begin:", testStroke.__doc__)
    testStroke()
