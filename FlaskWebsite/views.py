"""
Routes and views for the flask application.
"""

import codecs
from datetime import datetime, timedelta
from flask import request, redirect
from flask import render_template
from flask import Flask, make_response, send_file
from flask.wrappers import Response
import numpy as np
# import matplotlib.pyplot as plt, mpld3
from urllib import parse


import csv
from datetime import datetime
import io
from io import StringIO
import pandas as pd

from FlaskWebsite import app
from FlaskWebsite.data.twitter import get_tweets
from FlaskWebsite.data.youtube import get_captions
# from FlaskWebsite.data.visualization import get_visualization

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Election Corpus',
        DateFrom=datetime.now().date() - timedelta(days=7),
        DateTo=datetime.now().date(),
        candidate_list = get_candidate()
    )

@app.route('/create_corpus', methods=['POST'])
def create_corpus():
    twitterId = request.form['TwitterId']
    dateFrom = request.form['DateFrom']
    dateTo = request.form['DateTo']
    dfTweeets = get_tweets(twitterId, dateFrom, dateTo)

    # your code
    return render_template(
        'index.html',
        title='Election Corpus',
        DateFrom=datetime.now().date() - timedelta(days=7),
        DateTo=datetime.now().date(),
        candidate_list = get_candidate(),
        column_names= dfTweeets.columns.values,
        tweets = list(dfTweeets.values.tolist())
    )

@app.route('/download_corpus', methods=['POST'])
def download_corpus():
    twitterId = request.form['TwitterId']
    dateFrom = request.form['DateFrom']
    dateTo = request.form['DateTo']
    dfTweeets = get_tweets(twitterId, dateFrom, dateTo)

    dateToday = datetime.now()
    bom = codecs.BOM_UTF8.decode()
    resp = make_response(bom + dfTweeets.to_csv())
    resp.headers["Content-Disposition"] = f'attachment; filename={twitterId}-{dateToday}.csv'
    resp.headers["Content-Type"] = "text/csv; charset=utf-8"
    return resp

@app.route('/download_youtube', methods=['POST'])
def download_youtube():
    url = request.form['Url']
    parameters = dict(parse.parse_qsl(parse.urlsplit(url).query))
    df = get_captions(parameters["v"])
    dateToday = datetime.now()
    bom = codecs.BOM_UTF8.decode()
    resp = make_response(bom + df.to_csv())
    resp.headers["Content-Disposition"] = f'attachment; filename=youtube-{dateToday}.csv'
    resp.headers["Content-Type"] = "text/csv; charset=utf-8"
    return resp

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/show_plot', methods=['POST'])
def show_plot():
    file_name = "" #get_visualization()

    # fig, ax = plt.subplots(subplot_kw=dict(facecolor='#EEEEEE'))
    # N = 100

    # scatter = ax.scatter(np.random.normal(size=N),
    #                      np.random.normal(size=N),
    #                      c=np.random.random(size=N),
    #                      s=1000 * np.random.random(size=N),
    #                      alpha=0.3,
    #                      cmap=plt.cm.jet)
    # ax.grid(color='white', linestyle='solid')

    # ax.set_title("Scatter Plot (with tooltips!)", size=20)

    # labels = ['point {0}'.format(i + 1) for i in range(N)]
    # tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=labels)
    # mpld3.plugins.connect(fig, tooltip)

    # return mpld3.show()
    return file_name 
    


def get_candidate():
    candidate_list = {
        'n_arthaud': 'Nathalie Arthaud',
        'upr_asselineau': 'François Asselineau',
        'dupontaignan': 'Nicolas Dupont-Aignan',
        'Anne_Hidalgo':'Anne Hidalgo',
        'yjadot':'Yannick Jadot',
        'jeanlassalle':'Jean Lassalle',
        'MLP_officiel':'Marine Le Pen',
        'JLMelenchon':'Jean-Luc Melenchon',
        'PhilippePoutou':'Philippe Poutou',
        'ChTaubira' : 'Christiane Taubira',
        'AnasseKazib' : 'Anasse Kazib',
        'FabriceGrimal':'Fabrice Grimal',
        'larrouturou':'Pierre Larrouturou',
        'Waechter2022':'Antoine Waechter',
        'EmmanuelMacron':'Emmanuel Macron',
        'vpecresse':'Valérie Pécresse',
        'antoine27955080':'Antoine Martinez',
        'f_philippot':'Florian Philippot',
        'ZemmourEric':'Eric Zemmour',
        'Cau_Marie_': 'Marie Cau',
        'ClaraEgger1':'Clara Egger',
        'AlexLanglois_':'Alexandre Langlois',
        'HeleneThouy':'HélèneThouy',
        'MouvementSimple': 'Gaspard Koenig',
        'Vukuzman':'Georges Kuzmanovic',
        'Fabien_Roussel':'Fabien Roussel'
    }
    return candidate_list
