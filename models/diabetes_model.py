from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

def train_model(dataset_path):
    """Entrena el modelo de predicción de diabetes con el dataset proporcionado."""
    try:
        data = pd.read_csv(dataset_path)
        print(f"Dataset cargado: {data.shape} filas, columnas: {list(data.columns)}")
        X = data.drop("Outcome", axis=1)
        y = data["Outcome"]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
        model.fit(X_scaled, y)
        print("Modelo Random Forest entrenado correctamente")
        return model, scaler
    except Exception as e:
        print(f"Error al entrenar el modelo: {e}")
        return None, None

def predict_diabetes(model, scaler, nuevos_datos):
    """Realiza una predicción con los datos proporcionados."""
    try:
        nuevos_datos_scaled = scaler.transform([nuevos_datos])
        prediccion = model.predict(nuevos_datos_scaled)[0]
        print(f"Datos escalados: {nuevos_datos_scaled}, Predicción: {prediccion}")
        return prediccion
    except Exception as e:
        print(f"Error al predecir: {e}")
        return 1  # Por defecto, para evitar fallo silencioso
