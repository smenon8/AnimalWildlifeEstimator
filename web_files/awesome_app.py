from flask import Flask, render_template, request, json

import sys
sys.path.append("../script")

import mongod_helper as mh
import MarkRecapHelper as mark

app = Flask(__name__)
app.debug = True

def get_days_dict():
    pass

@app.route("/")
def main():
    return render_template('home.html')


@app.route("/showEstimation")
def showEstimation():
    return render_template("estimation.html")


@app.route("/estimation", methods=["POST", "GET"])
def estimation():
    species_name = request.form['inputSpeciesName']
    source_name = request.form['inputDataSourceName']

    print(species_name)
    print(source_name)

    days_dict = {'2015-03-01': 1, "2015-03-02": 2}
    estimate = mark.runMarkRecap(source_name, days_dict, filter_species=species_name)

    print(estimate)
    outputLine0 = "<h3>Population Estimate for %s</h3>" %species_name
    outputLine1 = "<b>Number of marks =</b> %i" %estimate[0]
    outputLine2 = "<b>Number of recaptures =</b> %i" %estimate[1]
    outputLine3  = "<b>Estimated Population =</b> %f" %estimate[2]
    output = "<p>%s<br />%s<br />%s<br />%s<br />" %(outputLine0, outputLine1, outputLine2, outputLine3)

    print(output)
    return output

if __name__ =="__main__":
    app.run()