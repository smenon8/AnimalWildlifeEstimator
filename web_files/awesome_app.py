from flask import Flask, render_template, request, json, flash

import sys, os, logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(filename)s: '    
                            '[%(levelname)s:] '
                            '%(funcName)s(): '
                            '%(lineno)d:\t'
                            '%(message)s')

sys.path.append("../script")

import mongod_helper as mh
import MarkRecapHelper as mark
import DB_Setup as db

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

@app.route("/showUploader_exif")
def showUploader_exif():
    return render_template("upload_exif.html")

@app.route("/showUploader_ibeis")
def showUploader_ibeis():
    return render_template("upload_ibeis_data.html")

@app.route("/upload_exif", methods=["POST", "GET"])
def upload_exif():
    exifFile = request.files['ExifFile']
    mapFile = request.files['MapFile']

    source_name = request.form['inputSourceName']
    ''
    if exifFile.filename == '' or mapFile.filename == '':
        return render_template("upload_exif.html",
                               msg="File(s) not specified")

    exifFile.save(os.path.join(app.config['UPLOAD_FOLDER'], exifFile.filename))

    logging.debug("File %s uploaded" %exifFile.filename)

    mapFile.save(os.path.join(app.config['UPLOAD_FOLDER'], mapFile.filename))
    logging.debug("File %s uploaded" % mapFile.filename)

    db.add_exif_data(mh.mongod_instance(),
                     os.path.join(app.config['UPLOAD_FOLDER'], mapFile.filename),
                     os.path.join(app.config['UPLOAD_FOLDER'], exifFile.filename),
                     source_name)

    logging.info("Upload to mongod complete")

    return render_template("upload_exif.html",
                           msg="Upload for " + exifFile.filename + " & "  + mapFile.filename + " successful! ")

@app.route("/upload_ibeis_data", methods=["POST", "GET"])
def upload_ibeis_data():
    aidFtrFile = request.files['AidFtrMapFile']
    gidAidFile = request.files['GidAidMapFile']
    mapFile = request.files['MapFile'] # fileNm map

    source_name = request.form['inputSourceName']
    ''
    if aidFtrFile.filename == '' or mapFile.filename == '' or gidAidFile.filename == '':
        return render_template("upload_ibeis_data.html",
                               msg="File(s) not specified")

    aidFtrFile.save(os.path.join(app.config['UPLOAD_FOLDER'], aidFtrFile.filename))
    logging.debug("File %s uploaded" %aidFtrFile.filename)

    gidAidFile.save(os.path.join(app.config['UPLOAD_FOLDER'], gidAidFile.filename))
    logging.debug("File %s uploaded" % gidAidFile.filename)

    mapFile.save(os.path.join(app.config['UPLOAD_FOLDER'], mapFile.filename))
    logging.debug("File %s uploaded" % mapFile.filename)

    db.add_ibeis_data(mh.mongod_instance(),
                     os.path.join(app.config['UPLOAD_FOLDER'], mapFile.filename),
                     os.path.join(app.config['UPLOAD_FOLDER'], gidAidFile.filename),
                     os.path.join(app.config['UPLOAD_FOLDER'], aidFtrFile.filename),
                     source_name)

    logging.info("Upload to mongod complete")

    return render_template("upload_ibeis_data.html",
                           msg="Upload for " + gidAidFile.filename + ", " + aidFtrFile.filename + " & "  + mapFile.filename + " successful! ")

@app.route("/estimation", methods=["POST", "GET"])
def estimation():
    species_name = request.form['inputSpeciesName']
    source_name = request.form['inputDataSourceName']

    logging.debug(species_name)
    logging.debug(source_name)

    days_dict = {'2015-03-01': 1, "2015-03-02": 2}
    estimate = mark.runMarkRecap(source_name, days_dict, filter_species=species_name)

    logging.debug(estimate)
    outputLine0 = "<h3>Population Estimate for %s</h3>" %species_name
    outputLine1 = "<b>Number of marks =</b> %i" %estimate[0]
    outputLine2 = "<b>Number of recaptures =</b> %i" %estimate[1]
    outputLine3  = "<b>Estimated Population =</b> %f" %estimate[2]
    output = "<p>%s<br />%s<br />%s<br />%s<br />" %(outputLine0, outputLine1, outputLine2, outputLine3)

    return output

if __name__ =="__main__":
    app.run()