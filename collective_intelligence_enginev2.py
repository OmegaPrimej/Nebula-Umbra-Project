import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, mean_squared_error
import numpy as np
import json

class DataIngestion:
    def ingest_csv(self, file_path):
        """Ingests data from a CSV file."""
        return pd.read_csv(file_path)

    def ingest_json(self, file_path):
        """Ingests data from a JSON file."""
        with open(file_path, 'r') as f:
            data = json.load(f)
        return pd.DataFrame(data)

    def ingest_dataframe(self, dataframe):
        """Ingests data from a pandas DataFrame."""
        return dataframe

class DataProcessing:
    def clean_data(self, df):
        """Cleans the data by handling missing values and outliers."""
        df = df.dropna()  # Remove rows with missing values
        # Example outlier removal (simplistic, needs refinement)
        for col in df.select_dtypes(include=np.number).columns:
            if col != 'target' and col != 'label': # avoid removing outliers on target variable.
                 mean = df[col].mean()
                 std = df[col].std()
                 df = df[(df[col] > mean - 3 * std) & (df[col] < mean + 3 * std)]
        return df

    def transform_data(self, df, categorical_cols=None):
        """Transforms data by encoding categorical variables."""
        if categorical_cols:
            df = pd.get_dummies(df, columns=categorical_cols, dummy_na=True)
        return df

    def feature_engineering(self, df, new_features=None):
        """Creates new features from existing data."""
        if new_features:
            for feature_name, function in new_features.items():
                df[feature_name] = df.apply(function, axis=1)
        return df

class ModelTraining:
    def train_random_forest(self, df, target_col, test_size=0.2, random_state=42):
        """Trains a Random Forest Classifier."""
        X = df.drop(target_col, axis=1)
        y = df[target_col]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        model = RandomForestClassifier(random_state=random_state)
        model.fit(X_train, y_train)
        return model, X_test, y_test

    # Add other model training methods here (e.g., neural networks)

class ModelDeployment:
    def evaluate_model(self, model, X_test, y_test):
        """Evaluates the trained model."""
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        #if regression:
        #    mse = mean_squared_error(y_test, y_pred)
        #    return {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1, "mse":mse}
        #else:
        return {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1}

    def predict(self, model, data):
        """Makes predictions using the trained model."""
        return model.predict(data)

class ContinuousLearning:
    def update_model(self, model, new_data, target_col):
        """Updates the model with new data."""
        X_new = new_data.drop(target_col, axis=1)
        y_new = new_data[target_col]
        model.fit(X_new, y_new) # Simplistic, will overwrite previous learning.
        return model

# Example usage:
if __name__ == "__main__":
    # Simulate data ingestion
    data_ingestion = DataIngestion()
    data = pd.DataFrame({
        'feature1': np.random.rand(100),
        'feature2': np.random.rand(100),
        'category': np.random.choice(['A', 'B', 'C'], 100),
        'target': np.random.choice([0, 1], 100)
    })

    # Data processing
    data_processing = DataProcessing()
    cleaned_data = data_processing.clean_data(data.copy())
    transformed_data = data_processing.transform_data(cleaned_data, categorical_cols=['category'])
    #Feature engineering
    new_features = {'combined_feature': lambda row: row['feature1'] + row['feature2']}
    engineered_data = data_processing.feature_engineering(transformed_data, new_features)

    # Model training
    model_training = ModelTraining()
    model, X_test, y_test = model_training.train_random_forest(engineered_data, 'target')

    # Model deployment
    model_deployment = ModelDeployment()
    evaluation_metrics = model_deployment.evaluate_model(model, X_test, y_test)
    print("Evaluation Metrics:", evaluation_metrics)

    # Example prediction
    sample_prediction = model_deployment.predict(model, X_test.iloc[[0]])
    print("Sample Prediction:", sample_prediction)

    # Continuous learning simulation
    continuous_learning = ContinuousLearning()
    new_data = pd.DataFrame({
        'feature1': np.random.rand(20),
        'feature2': np.random.rand(20),
        'category': np.random.choice(['A', 'B', 'C'], 20),
        'target': np.random.choice([0, 1], 20)
    })
    new_data = data_processing.clean_data(new_data)
    new_data = data_processing.transform_data(new_data, categorical_cols=['category'])
    new_data = data_processing.feature_engineering(new_data, new_features)

    updated_model = continuous_learning.update_model(model, new_data, 'target')
    updated_evaluation = model_deployment.evaluate_model(updated_model, X_test, y_test)
    print("Updated Model Evaluation Metrics:", updated_evaluation)
