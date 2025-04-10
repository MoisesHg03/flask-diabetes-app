from flask import Flask, request, render_template, send_file, redirect, url_for
from models.diabetes_model import train_model, predict_diabetes
from database.db import init_db, save_prediction, get_historial
from utils.pdf_generator import generate_pdf
import sqlite3

app = Flask(__name__)

# Inicializar modelo y scaler
try:
    model, scaler = train_model("diabetes.csv")
    print("Modelo y scaler inicializados correctamente")
except Exception as e:
    print(f"Error al inicializar el modelo: {e}")
    model, scaler = None, None

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    resultado_clase = None
    explicacion = None
    historial = get_historial()

    if request.method == "POST":
        try:
            nuevos_datos = [
                float(request.form["glucosa"]),
                float(request.form["presion"]),
                float(request.form["piel"]),
                float(request.form["insulina"]),
                float(request.form["imc"]),
                float(request.form["pedigri"]),
                float(request.form["edad"]),
                float(request.form["embarazos"])
            ]
            if model is None or scaler is None:
                raise ValueError("Modelo o scaler no inicializados")

            # Extraer glucosa (índice 0) y pedigrí (índice 5)
            glucosa = nuevos_datos[0]
            pedigri = nuevos_datos[5]

            # Aplicar condiciones específicas
            if glucosa > 100:
                prediccion = 1  # Positivo si glucosa > 100
                print(f"Condición: Glucosa {glucosa} > 100, forzando Positivo")
            elif pedigri > 0.6:
                prediccion = 1  # Positivo si pedigrí > 0.6
                print(f"Condición: Pedigrí {pedigri} > 0.6, forzando Positivo")
            elif glucosa <= 100 and pedigri < 0.5:
                prediccion = 0  # Negativo si glucosa <= 100 y pedigrí < 0.5
                print(f"Condición: Glucosa {glucosa} <= 100 y Pedigrí {pedigri} < 0.5, forzando Negativo")
            else:
                # Si no se cumplen las condiciones específicas, usar el modelo
                prediccion = predict_diabetes(model, scaler, nuevos_datos)
                print(f"Usando modelo: Datos ingresados: {nuevos_datos}, Predicción: {prediccion}")

            # Asignar resultado según la predicción
            resultado = "Positivo" if prediccion == 1 else "Negativo"
            resultado_clase = "positivo" if prediccion == 1 else "negativo"
            explicacion = ("Positivo: Alta probabilidad de diabetes. Consulta a un médico." 
                          if prediccion == 1 else 
                          "Negativo: Baja probabilidad de diabetes, pero mantén un seguimiento.")
            print(f"Resultado mostrado: {resultado}")

            # Guardar predicción
            save_prediction(nuevos_datos, resultado)
            historial = get_historial()

        except ValueError as e:
            resultado = f"Error: {str(e)}"
            resultado_clase = "error"
            explicacion = "Revisa los datos ingresados o la inicialización del modelo."
            print(f"Error: {e}")

    return render_template("index.html", resultado=resultado, resultado_clase=resultado_clase, explicacion=explicacion, historial=historial)

@app.route("/download/<int:id>")
def download_pdf(id):
    conn = sqlite3.connect("diabetes.db")
    c = conn.cursor()
    c.execute("SELECT * FROM predicciones WHERE id = ?", (id,))
    registro = c.fetchone()
    conn.close()

    if registro:
        pdf_buffer = generate_pdf(registro)
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"prediccion_{registro[0]}_{registro[10].replace(' ', '_')}.pdf"
        )
    return "Registro no encontrado", 404

@app.route("/reset_historial", methods=["POST"])
def reset_historial():
    conn = sqlite3.connect("diabetes.db")
    c = conn.cursor()
    c.execute("DELETE FROM predicciones")
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
