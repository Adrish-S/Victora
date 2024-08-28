from flask import Flask, render_template, request, Response, redirect, url_for, jsonify, g
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot
import json
import plotly
import pyrfc
import datetime
import io
import numpy as np

app = Flask(__name__)

connection_params = {"ashost":"","sysnr":"","lang": "EN","saprouter": ""}

def get_sap_conn():
        if 'sap_connection' not in g:
            client_no = str(request.form['client_no'])
            username = str(request.form['username'])
            password = str(request.form['password'])
            sap_params = connection_params.copy()
            sap_params.update({"user": username,"passwd": password,"client":client_no})
            g.sap_connection = pyrfc.Connection(**sap_params)
        return g.sap_connection

@app.route('/')
def login():
    return render_template('index.html')

@app.route("/", methods=["POST"])
def index():   
    def validate_login():
        sap_conn = get_sap_connection()
    if sap_conn.alive():
        return render_template('data_input.html')
    else:
        return("Invalid login credentials. Please try again.")

@app.route('/process_data', methods=['POST'])
def process_data():
    param = {'SIGN': request.form.get('SIGN'), 'OPTION': request.form.get('OPTION'), 'LOW':datetime.datetime.strptime(request.form.get("LOW"), '%Y-%m-%d').date(),'HIGH':datetime.datetime.strptime(request.form.get("HIGH"), '%Y-%m-%d').date()}
    input_params={"I_EDATU":param,"C_SALES":'X'}
    df1= call_pyrfc(input_params)

    kunnr_10 = df1[df1['VTWEG']=='10']
    kunnr_11 = df1[df1['VTWEG']=='11']
    kunnr_12 = df1[df1['VTWEG']=='12']

    # Create a Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df1['KUNNR'], y=df1['Sales'], mode='lines', name='Sales'))
    fig.update_layout(title='Sales vs. KUNNR', xaxis_title='KUNNR', yaxis_title='Sales')

    # Plot the figure to HTML
    graph_html = plot(fig, output_type='div', include_plotlyjs=False)
    
    # Convert the figure and layout to JSON-compatible format
    chart_data_json = json.dumps(fig.to_dict(), cls=plotly.utils.PlotlyJSONEncoder)
    chart_layout_json = json.dumps(fig.layout.to_plotly_json(), cls=plotly.utils.PlotlyJSONEncoder)
    
    # Return the JSON data
    return jsonify(chartData=chart_data_json, chartLayout=chart_layout_json)


def call_pyrfc(input_params):
    sap_conn = get_sap_connection()
    ZFMR_SALES
    sap_conn.call("ZTEST_SALEFM", I_EDATU=inp_params["I_EDATU"], C_SALES=inp_params["C_SALES"])
    df1 = pd.DataFrame(result['IT_SALE']) if 'IT_SALE' in result else None
    df1.replace('', pd.NA, inplace=True)
    df1 = df1.drop(columns="SNO").dropna(axis=1, how='all')

    return df1

if __name__ == '__main__':
    app.run(debug=True)
