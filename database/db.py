import sqlite3
from datetime import datetime

def init_db():
    """Inicializa la base de datos SQLite si no existe."""
    conn = sqlite3.connect("diabetes.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS predicciones (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 glucosa REAL, presion REAL, piel REAL, insulina REAL,
                 imc REAL, pedigri REAL, edad REAL, embarazos REAL,
                 resultado TEXT, fecha TEXT)''')
    conn.commit()
    conn.close()

def save_prediction(datos, resultado):
    """Guarda una predicción en la base de datos."""
    conn = sqlite3.connect("diabetes.db")
    c = conn.cursor()
    c.execute("INSERT INTO predicciones (glucosa, presion, piel, insulina, imc, pedigri, edad, embarazos, resultado, fecha) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              datos + [resultado, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    conn.commit()
    conn.close()

def get_historial():
    """Obtiene el historial de predicciones ordenado por fecha descendente."""
    conn = sqlite3.connect("diabetes.db")
    c = conn.cursor()
    c.execute("SELECT * FROM predicciones ORDER BY fecha DESC")
    historial = c.fetchall()
    conn.close()
    return historial