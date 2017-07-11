from flask import render_template, request, redirect, url_for
from . import app
import requests
import xml.etree.ElementTree as ET
from . import shake
import pygal
from pygal.style import DefaultStyle

@app.route("/", methods=["GET"])
def select():
    return render_template('whatplay.html')

@app.route("/", methods=["POST"])
def results():
    if len(request.form['play']) > 0:
        url = request.form['play']
    else:
        url = 'http://www.ibiblio.org/xml/examples/shakespeare/macbeth.xml'
    
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        return render_template("results.html", error = e)
    try:
        tree = ET.fromstring(response.content)
    except ET.ParseError:
        return render_template("results.html", 
            error = "That url doesn't have the right xml format :("
        )

    results = shake.parse_play(tree)
    median = results[len(results)//2][1]
    above = [x for x in results if x[1] > median]
    below = [x for x in results if x[1] <= median]
    
    top_title = "Number of lines per character (with lines above median)"
    top_half = pygal.Bar(width=1200,
        height=600, title=top_title,)
    for k, v in above:
        top_half.add(k, [{'value': v, 'label': k}])
    top_half = top_half.render_data_uri()
    
    bottom_title = "Number of lines per character (with lines below median)"
    bottom_half = pygal.Bar(width=1200,
        height=600, title=bottom_title,)
    for k, v in below:
        bottom_half.add(k, [{'value': v, 'label': k}])
    bottom_half = bottom_half.render_data_uri()
    
    return render_template("results.html",
        top_half = top_half,
        bottom_half = bottom_half,
    )