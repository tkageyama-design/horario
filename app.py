from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta
import os

app = Flask(__name__)

historico = []

@app.route("/", methods=["GET","POST"])
def index():

    saida_prevista=None
    horas_trabalhadas=None
    horas_restantes=None
    horas_extras=None

    entrada=""
    saida_almoco=""
    retorno_almoco=""
    saida_real=""

    if request.method=="POST":

        entrada=request.form["entrada"]
        saida_almoco=request.form["saida_almoco"]
        retorno_almoco=request.form["retorno_almoco"]
        saida_real=request.form.get("saida_real","")

        fmt="%H:%M"

        entrada_dt=datetime.strptime(entrada,fmt)
        saida_almoco_dt=datetime.strptime(saida_almoco,fmt)
        retorno_almoco_dt=datetime.strptime(retorno_almoco,fmt)

        jornada=timedelta(hours=8)

        tempo_trabalhado=saida_almoco_dt-entrada_dt
        horas_restantes_td=jornada-tempo_trabalhado

        saida_prevista_dt=retorno_almoco_dt+horas_restantes_td
        saida_prevista=saida_prevista_dt.strftime("%H:%M")

        horas_trabalhadas=str(tempo_trabalhado)[:-3]
        horas_restantes=str(horas_restantes_td)[:-3]

        if saida_real!="":

            saida_real_dt=datetime.strptime(saida_real,fmt)

            extras=saida_real_dt-saida_prevista_dt

            if extras.total_seconds()>0:
                horas_extras=str(extras)[:-3]
            else:
                horas_extras="00:00"

        historico.insert(0,{
            "entrada":entrada,
            "saida_almoco":saida_almoco,
            "retorno_almoco":retorno_almoco,
            "saida_prevista":saida_prevista,
            "saida_real":saida_real,
            "extras":horas_extras
        })

    return render_template(
        "index.html",
        entrada=entrada,
        saida_almoco=saida_almoco,
        retorno_almoco=retorno_almoco,
        saida_real=saida_real,
        saida_prevista=saida_prevista,
        horas_trabalhadas=horas_trabalhadas,
        horas_restantes=horas_restantes,
        horas_extras=horas_extras,
        historico=historico
    )

@app.route("/limpar")
def limpar():

    historico.clear()
    return redirect("/")

if __name__=="__main__":

    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port)