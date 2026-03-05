from flask import Flask, render_template, request
from datetime import datetime, timedelta
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():

    saida = None

    if request.method == "POST":

        entrada = request.form["entrada"]
        saida_almoco = request.form["saida_almoco"]
        retorno_almoco = request.form["retorno_almoco"]

        fmt = "%H:%M"

        entrada = datetime.strptime(entrada, fmt)
        saida_almoco = datetime.strptime(saida_almoco, fmt)
        retorno_almoco = datetime.strptime(retorno_almoco, fmt)

        tempo_almoco = retorno_almoco - saida_almoco
        jornada = timedelta(hours=8)

        saida_final = entrada + jornada + tempo_almoco

        saida = saida_final.strftime("%H:%M")

return render_template(
    "index.html",
    saida=saida,
    horas_trabalhadas=horas_trabalhadas,
    horas_restantes=horas_restantes,
    historico=historico,
    entrada=entrada if request.method=="POST" else "",
    saida_almoco=saida_almoco if request.method=="POST" else "",
    retorno_almoco=retorno_almoco if request.method=="POST" else ""
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)