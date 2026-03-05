from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta
import os

app = Flask(__name__)

historico = []

@app.route("/", methods=["GET","POST"])
def index():

    saida = None
    horas_trabalhadas = None
    horas_restantes = None

    entrada = ""
    saida_almoco = ""
    retorno_almoco = ""

    if request.method == "POST":

        entrada = request.form["entrada"]
        saida_almoco = request.form["saida_almoco"]
        retorno_almoco = request.form["retorno_almoco"]

        fmt = "%H:%M"

        entrada_dt = datetime.strptime(entrada, fmt)
        saida_almoco_dt = datetime.strptime(saida_almoco, fmt)
        retorno_almoco_dt = datetime.strptime(retorno_almoco, fmt)

        jornada = timedelta(hours=8)

        tempo_trabalhado = saida_almoco_dt - entrada_dt
        tempo_almoco = retorno_almoco_dt - saida_almoco_dt

        horas_restantes_td = jornada - tempo_trabalhado

        saida_final = retorno_almoco_dt + horas_restantes_td

        saida = saida_final.strftime("%H:%M")

        horas_trabalhadas = str(tempo_trabalhado)[:-3]
        horas_restantes = str(horas_restantes_td)[:-3]

        historico.insert(0,{
            "entrada":entrada,
            "saida_almoco":saida_almoco,
            "retorno_almoco":retorno_almoco,
            "saida":saida
        })

    return render_template(
        "index.html",
        saida=saida,
        horas_trabalhadas=horas_trabalhadas,
        horas_restantes=horas_restantes,
        historico=historico,
        entrada=entrada,
        saida_almoco=saida_almoco,
        retorno_almoco=retorno_almoco
    )


@app.route("/limpar")
def limpar():
    historico.clear()
    return redirect("/")


if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)