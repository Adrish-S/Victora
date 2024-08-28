from flask import Flask, render_template, request, Response, redirect, url_for
import pyrfc
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import numpy as np

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])

def index():
    if request.method == "POST":
        DATE = {
            'SIGN': request.form.get("SIGN"),
            'OPTION': request.form.get("OPTION"),
            'LOW': datetime.datetime.strptime(request.form.get("LOW"), '%Y-%m-%d').date(),
            'HIGH': datetime.datetime.strptime(request.form.get("HIGH"), '%Y-%m-%d').date()
        }
        sale = str(request.form.get("SALE"))
        input_params={"I_EDATU":DATE,"C_SALES":sale}
        result, df1, df2 = call_pyrfc(input_params)
        return render_template("index.html", result=result, df1=df1, df2=df2)
    return render_template("index.html", result=None, df1=None, df2=None)

def call_pyrfc(inp_params):
    connection_params = {
        "user": "",
        "passwd": "",
        "ashost": "",
        "sysnr": "",
        "client": "",
        "lang": "EN",
        "saprouter": ""
    }
    
    with pyrfc.Connection(**connection_params) as conn:
        result = conn.call("ZTEST_SALEFM", I_EDATU=inp_params["I_EDATU"], C_SALES=inp_params["C_SALES"])
        df1 = pd.DataFrame(result['IT_SCH']) if 'IT_SCH' in result else None
        df1.replace('', pd.NA, inplace=True)
        df1 = df1.drop(columns="SNO").dropna(axis=1, how='all')
        df2 = pd.DataFrame(result['IT_SALE']) if 'IT_SALE' in result else None
        df2.replace('', pd.NA, inplace=True)
        df2 = df2.drop(columns="SNO").dropna(axis=1, how='all')
        return result,df1,df2

if __name__ == "__main__":
    app.run(debug=True)
