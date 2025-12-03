from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
import requests
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
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


@app.route("/commits/")
def commits_chart():
    import requests

    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"

    # Fix obligatoire pour GitHub + AlwaysData
    headers = {
        "User-Agent": "AlwaysDataStudent",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, headers=headers)

    # Si l'API plante → on évite l'erreur 500
    if response.status_code != 200:
        return f"Erreur GitHub API : {response.status_code}<br>{response.text}"

    commits = response.json()

    minute_count = {}

    for commit in commits:
        try:
            date_str = commit["commit"]["author"]["date"]
            date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            minute = date_obj.minute

            minute_count[minute] = minute_count.get(minute, 0) + 1
        except Exception as e:
            print("Erreur commit :", e)
            continue

    data_list = [["Minute", "Commits"]]
    for minute, count in sorted(minute_count.items()):
        data_list.append([minute, count])

    return render_template("commits.html", data=data_list)


if __name__ == "__main__":
  app.run(debug=True)
