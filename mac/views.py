from flask import render_template, request, redirect, url_for
from . import app
import requests
import xml.etree.ElementTree as ET
from . import macbeth
import pygal
from pygal.style import DefaultStyle
import sys
import numpy
from imp import reload
reload(sys)
sys.setdefaultencoding("utf-8")

@app.route("/", methods=["GET"])
def select():
    return render_template('whatplay.html')

@app.route("/", methods=["POST"])
def results():
    
    if len(request.form['play']) > 0:
        url = request.form['play']
    else:
        url = 'http://www.ibiblio.org/xml/examples/shakespeare/macbeth.xml'
    
    response = requests.get(url)
    tree = ET.fromstring(response.content)
    results = macbeth.acts(tree)
    median = numpy.median(numpy.array(results.values()))
    above = [x for x in results.items() if x[1] > median]
    below = [x for x in results.items() if x[1] <= median]
    
    top_title = "Number of lines per charcter (with lines above median)"
    top_half = pygal.Bar(width=1200,
        height=600, title=top_title,)
    top_half.force_uri_protocol = 'http'
    for k, v in sorted(above, key=lambda character: character[1], reverse=True):
        top_half.add(k, [{'value': v, 'label': k}])
    
    bottom_title = "Number of lines per charcter (with lines below median)"
    bottom_half = pygal.Bar(width=1200,
        height=600, title=bottom_title,)
    bottom_half.force_uri_protocol = 'https'
    for k, v in sorted(below, key=lambda character: character[1], reverse=True):
        bottom_half.add(k, [{'value': v, 'label': k}])
    
    top_half = top_half.render_data_uri()
    bottom_half = bottom_half.render_data_uri()
    
    return render_template("results.html",
        top_half = top_half,
        bottom_half = bottom_half,
    )