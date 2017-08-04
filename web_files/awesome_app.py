from flask import Flask, render_template, request, json, flash

import sys, os
sys.path.append("../script")

import mongod_helper as mh
import MarkRecapHelper as mark

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = '/tmp/'
app.config['ALLOWED_EXTENSIONS'] = set(['json'])
app.secret_key = 'some_secret'

@app.route("/")
def main():
    return render_template('home.html')


@app.route("/showEstimation")
def showEstimation():
    return render_template("estimation.html")

@app.route("/showUploader")
def showUploader():
    return render_template("upload_json.html")

@app.route("/upload", methods=["POST", "GET"])
def upload():
    exifFile = request.files['ExifFile']
    mapFile = request.files['MapFile']

    source_name = request.form['inputSourceName']
    ''
    if exifFile.filename == '' or mapFile.filename == '':
        return render_template("upload_json.html",
                               msg="File(s) not specified")

    exifFile.save(os.path.join(app.config['UPLOAD_FOLDER'], exifFile.filename))
    print("File %s uploaded" %exifFile.filename)

    mapFile.save(os.path.join(app.config['UPLOAD_FOLDER'], mapFile.filename))
    print("File %s uploaded" % mapFile.filename)


    return render_template("upload_json.html",
                           msg="Upload for " + exifFile.filename + " & "  + mapFile.filename + " successful! ")

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

    return output

if __name__ =="__main__":
    app.run()