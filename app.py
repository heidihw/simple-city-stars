import apihelper
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("form.html", locations=apihelper.locations_data.keys(), days=apihelper.all_days, hours=apihelper.all_hours)

@app.route("/results", methods=["GET", "POST"])
def results():
    if request.method == "POST":
        locations = {}
        for location in apihelper.locations_data.keys():
            if request.form.get(location) == "on":
                locations[location] = apihelper.locations_data.get(location)
        days = []
        for day in apihelper.all_days:
            if request.form.get(str(day)) == "on":
                days.append(day)
        hours = []
        for hour in apihelper.all_hours:
            if request.form.get(str(hour)) == "on":
                hours.append(hour)

        # print(locations)
        # print(days)
        # print(hours)

        data = apihelper.get(locations, days, hours)
        return render_template("results.html", loc_data=data, locations=len(locations), days=len(days), hours=len(hours), 
                               ii=range(len(locations)), jj=range(len(days)), kk=range(len(hours)))
    else:
        return "Wrong HTTP method", 400
