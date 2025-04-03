from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

def train_model(dataset_path):
    """Entrena el modelo de predicción de diabetes con el dataset proporcionado."""
    data = pd.read_csv(dataset_path)
    X = data.drop("Outcome", axis=1)
    y = data["Outcome"]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model = DecisionTreeClassifier(max_depth=5)
    model.fit(X_scaled, y)
    return model, scaler

def predict_diabetes(model, scaler, nuevos_datos):
    """Realiza una predicción con los datos proporcionados."""
    nuevos_datos_scaled = scaler.transform([nuevos_datos])
    prediccion = model.predict(nuevos_datos_scaled)[0]
    return prediccion