from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

archivo_excel = "datos.xlsx"
excel_data = pd.ExcelFile(archivo_excel)
hojas = excel_data.sheet_names  # nombres de pestañas

@app.route("/", methods=["GET", "POST"])
def index():
    datos = None
    hoja_seleccionada = None

    if request.method == "POST":
        hoja_seleccionada = request.form["hoja"]
        datos = excel_data.parse(hoja_seleccionada).to_html(classes='table table-bordered', index=False)

    return render_template("index.html", hojas=hojas, datos=datos, hoja_seleccionada=hoja_seleccionada)

app.run(host="0.0.0.0", port=3000)
