from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
import requests
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm4

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")


@app.route('/histogramme/')
def histogramme():
    return render_template('histogramme/index.html')

import requests  # <-- ajoute cette ligne en haut AVEC les autres imports


@app.route('/commits/')
def commits_chart():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url)
    commits = response.json()

    # Tableau avec 60 cases pour compter les commits par minute
    minutes_count = [0] * 60

    for commit in commits:
        try:
            date_str = commit["commit"]["author"]["date"]
            date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            minute = date_obj.minute
            minutes_count[minute] += 1
        except:
            pass

    # Format attendu par Google Charts
    data = [["Minute", "Commits"]]
    for i in range(60):
        data.append([i, minutes_count[i]])

    return render_template("commits.html", data=data)

if __name__ == "__main__":
  app.run(debug=True)
