from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Cargar el archivo Excel
archivo_excel = "datos.xlsx"
excel_data = pd.ExcelFile(archivo_excel)
hojas = excel_data.sheet_names

# ==========================
# RUTAS
# ==========================
PRESENTACION_DIR = os.path.join("static", "presentacion")
PDF_DIR = os.path.join("static", "presentacion", "pdfs")

# ==========================
# PRESENTACIONES
# ==========================
presentaciones = sorted([
    carpeta for carpeta in os.listdir(PRESENTACION_DIR)
    if os.path.isdir(os.path.join(PRESENTACION_DIR, carpeta))
])

# ==========================
# PDFS
# ==========================
pdfs = sorted([
    f for f in os.listdir(PDF_DIR)
    if f.lower().endswith(".pdf")
]) if os.path.exists(PDF_DIR) else []

print("================================")
print("PRESENTACION_DIR:", PRESENTACION_DIR)
print("PDF_DIR:", PDF_DIR)
print("Existe carpeta:", os.path.exists(PDF_DIR))
print("PDF encontrados:", pdfs)
print("================================")

@app.route("/", methods=["GET", "POST"])
def index():

    datos = None
    hoja_seleccionada = None
    vista = "tabla"
    presentacion_seleccionada = None
    imagenes = []
    pdf_seleccionado = None

    if request.method == "POST":

        vista = request.form.get("vista", "tabla")

        if vista == "tabla":

            hoja_seleccionada = request.form.get("hoja")

            if hoja_seleccionada in hojas:
                datos = excel_data.parse(
                    hoja_seleccionada
                ).to_html(
                    classes="table table-bordered",
                    index=False
                )

        elif vista == "presentacion":

            presentacion_seleccionada = request.form.get("presentacion")

            ruta_presentacion = os.path.join(
                PRESENTACION_DIR,
                presentacion_seleccionada
            )

            if os.path.isdir(ruta_presentacion):
                imagenes = sorted([
                    f for f in os.listdir(ruta_presentacion)
                    if f.lower().endswith((".jpg", ".jpeg", ".png"))
                ])

        elif vista == "pdf":
            pdf_seleccionado = request.form.get("pdf")

    return render_template(
        "index.html",
        hojas=hojas,
        datos=datos,
        hoja_seleccionada=hoja_seleccionada,
        vista=vista,
        presentaciones=presentaciones,
        presentacion_seleccionada=presentacion_seleccionada,
        imagenes=imagenes,
        pdfs=pdfs,
        pdf_seleccionado=pdf_seleccionado,
        range=range
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
