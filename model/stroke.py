import pandas as pd
from sklearn.model_selection import train_test_split
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

    def clean_data(self):
        # Fill missing values if any
        self.stroke_data.fillna(method='ffill', inplace=True)
        
        # One-hot encode categorical features
        self.stroke_data = pd.get_dummies(self.stroke_data, columns=self.categorical_features, drop_first=True)
        self.features.extend([col for col in self.stroke_data.columns if col.startswith(tuple(self.categorical_features))])

    def train_model(self):
        X = self.stroke_data[self.features]
        y = self.stroke_data[self.target]

        # Set minimum number of samples for training
        min_train_samples = 100

        # Split data into train and test sets with a minimum number of samples for training
        while True:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
            if len(X_train) >= min_train_samples:
                break
        
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
            cls._instance.clean_data()
            cls._instance.train_model()
        return cls._instance

    def predict_stroke_probability(self, patient_info):
        # Clean and prepare patient data for prediction
        patient_df = pd.DataFrame(patient_info, index=[0])

        # Check if all required columns are present in patient_df for one-hot encoding
        missing_columns = set(self.categorical_features) - set(patient_df.columns)
        if missing_columns:
            raise ValueError(f"Columns {missing_columns} are missing in patient data.")

        # One-hot encode categorical features
        patient_df = pd.get_dummies(patient_df, columns=self.categorical_features, drop_first=True)
        
        # Ensure the features are in the same order as in the training data
        patient_df = patient_df.reindex(columns=self.features, fill_value=0)

        # Predicting stroke probability
        stroke_probability = self.model.predict_proba(patient_df)
        return stroke_probability[0][1] * 100  # Return the probability of stroke in percentage
def testStroke():
    print("Step 1: Define patient data for prediction:")
    patient_info = {
        'age': [67],
        'gender': ['Male'],           # Make sure the keys match the expected column names
        'hypertension': [0],
        'heart_disease': [1],
        'ever_married': ['Yes'],      # Make sure the keys match the expected column names
        'work_type': ['Private'],     # Make sure the keys match the expected column names
        'Residence_type': ['Urban'],  # Make sure the keys match the expected column names
        'avg_glucose_level': [228.69],
        'bmi': [36.6]
    }
    print("\t", patient_info)
    print()

    strokeModel = StrokeModel.get_instance("./healthcare-dataset-stroke-data.csv")
    stroke_probability = strokeModel.predict_stroke_probability(patient_info)
    print('\t Predicted stroke probability:', stroke_probability)
    print()

if __name__ == "__main__":
    print("Begin:", testStroke.__doc__)
    testStroke()
