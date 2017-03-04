import ConfigParser
from boto3 import client
import tempfile
import urllib
from flask import Flask#, flash, redirect, render_template, \
from boto3.s3.transfer import S3Transfer
import boto3
from flask import Flask, flash, redirect, render_template, \
     request, url_for
import requests
import sys
import os
import platform
import os.path, time
import cgi, io
import cgitb; cgitb.enable()
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask import Response
from flask import make_response
from boto.s3.key import Key
from boto3.session import Session
import boto3.session
from botocore.exceptions import ClientError
import botocore.session
app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.secret_key = 'sdg is crazy'
config = ConfigParser.ConfigParser()

aid = ''
apwd=''
bucket_name=''
@app.route('/')
def hello_world():
        return render_template('index.html')

@app.route('/test',methods=['GET', 'POST'])
def test():
        global aid
        global apwd
        global bucket_name
        username=request.form['userName']
                                                                                                                             1,1           Top
        s3 = boto3.resource('s3',aws_access_key_id='access_key',aws_secret_access_key='secret key')
        fContent=s3.Object('sdg-cred', 'creds.txt').get()['Body'].read()
        fw=open('/var/www/html/flaskapp/input1.txt','w+')
        fw.write(fContent)
        fw.close()
        myfile=open('/var/www/html/flaskapp/input1.txt','r')
        config = ConfigParser.ConfigParser()
        config.readfp(myfile)
        conn=boto3.resource('s3',aws_access_key_id=config.get(username, 'aws_access_key_id'),aws_secret_access_key=config.get(username, 'aws_secret_access_key'))
        aid=aws_access_key_id=config.get(username, 'aws_access_key_id')
        apwd=aws_secret_access_key=config.get(username, 'aws_secret_access_key')
        bucket_name='sdg-'+username
        return render_template('welcome.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#------------------------------------- Delete File ---------------------------------
@app.route('/DeleteFile',methods=['GET','POST'])
def DeleteFile():
        return render_template('file-delete.htm')

@app.route('/delfile',methods=['POST'])
def delfile():
        filename=request.form['fileName']
        s3 = boto3.resource('s3',aws_access_key_id=aid,aws_secret_access_key=apwd)
        s3.Object(bucket_name, filename).delete()
        return 'File deleted'

#-----------------------------------File Upload ------------------------------
@app.route('/file-upload', methods=['GET', 'POST'])
def fileUpload():
        return render_template('file-upload.htm')

@app.route('/save-file', methods=['GET','POST'])
def saveFile():
        #print 'save'
        import os, time
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
                filename =  file.filename
                fContent = file.read()

                temporary_file = tempfile.NamedTemporaryFile()
                fw=open(temporary_file.name,'w+')
                fw.write(fContent)
                fw.close()
                data=open(temporary_file.name,'r')
                s3 = boto3.resource('s3',aws_access_key_id=aid,aws_secret_access_key=apwd)
                s3.Bucket(bucket_name).put_object(Key=filename, Body=data)
                return 'file uploaded'
        return 'Invalid File extension'

#----------------------- List Files -------------------------------
@app.route('/ListFiles',methods=['GET','POST'])
def ListFiles():
        html = ''
        s3 = boto3.resource('s3',aws_access_key_id=aid,aws_secret_access_key=apwd)
        temp = []
        bucket=s3.Bucket(bucket_name)
        for obj in bucket.objects.all():
                temp.append(obj.key)
        html = '''<html>
                       <title>Attributes</title>
                       %s
               </html>''' %(temp)
        return html

#------------------File Download ---------------------------------
@app.route('/fileDownload',methods=['GET','POST'])
def fileDownload():
        return render_template('file-download.htm')

@app.route('/downloadfile',methods=['POST'])
def downloadfile():
        filename=request.form['fileName']
        s3 = boto3.resource('s3',aws_access_key_id=aid,aws_secret_access_key=apwd)
        fContent=s3.Object(bucket_name, filename).get()['Body'].read()
        response = make_response(fContent)
        response.headers["Content-Disposition"] = "attachment; filename="+filename+";"
        return response


if __name__ == '__main__':
  app.run()



