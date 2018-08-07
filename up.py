#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, request, flash, redirect, url_for,render_template, Response, jsonify
from flask import send_file
from werkzeug import secure_filename
import os, random, json
import essaivtk3
import convertion
import uri


app = Flask(__name__)
app.secret_key = 'd66HR8dç"f_-àgjYYic*dh'
app.config['UPLOAD_PATH']= '/home/quentin/Desktop/Interface/ups/'
app.config['UPLOAD_PATH2']= '/home/quentin/Desktop/Interface/display/'

def extension_ok(nomfic):
    """ Return True if file extension is correct """
    return '.' in nomfic and nomfic.rsplit('.', 1)[1] in ('dcm')


@app.route('/')
def my_index():
	return render_template('up_up.html')

#home page
@app.route('/', methods=['POST'])
def upload():

     #delete all old files in ups folder
    if request.method == 'POST' and 'fic' in request.files:
        os.system('rm ./ups/*.*')

        #save every file in ups folder indicated by UPLOAD_PATH
        for f in request.files.getlist('fic'):
            f.save(os.path.join(app.config['UPLOAD_PATH'], f.filename))		

    return redirect(url_for('upload2')) #goes to /upload2 route


#web page when all the dicom files are successfully uploaded
#it is time to upload one file to upload in order to display it
@app.route('/upload2', methods=['GET', 'POST'])
def upload2():
    if request.method == 'POST' and 'fic2' in request.files:
    	os.system('rm ./display/*.*') 
    	for f in request.files.getlist('fic2'):

    		f.save(os.path.join(app.config['UPLOAD_PATH2'], f.filename))

    return render_template('up_up2.html')

#web page where the dicom image selected before is displayed.The user can click on the image to return bone value
@app.route('/click/', methods=['GET', 'POST'])
def click():
    folderpath='./display'
    convertion.convert(folderpath) #convert the DICOM file selected into PNG
    dataURI=uri.generateURI('./display/output.png') #generate the URI address of the dicom image selected

    return render_template('click_v1.html', dataURI=dataURI)


@app.route('/model/', methods=['GET', 'POST'])
def model():
        request_json = request.get_json()
        data = request_json['name'] #we get the bone value 
        #value=int('boneValue')
        essaivtk3.modelisation(data) #we used this bone value as threshold for the segmentation algorithm called essaivtk3.py
        print(data)
        return 'success'

#web page that displays the STL file (3D model) created        
@app.route('/view/', methods=['GET', 'POST'])
def view():

        return render_template('misc_exporter_stl.html')

if __name__ == '__main__':
    app.run(debug=True)


