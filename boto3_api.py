import os
import boto3
from flask import Flask, render_template, request, redirect, url_for 

app = Flask(__name__)

s3 = boto3.resource(
    's3',
    endpoint_url='https://s3-openshift-storage.apps.mlops.software.bl.platform',
    aws_access_key_id=os.getenv("aws_access_key_id".upper()),
    aws_secret_access_key=os.getenv("aws_secret_access_key".upper())
)

# Nombre del bucket  
BUCKET_NAME = 'mlops-af3743d5-d41b-4d46-8016-314a956bb9f1'  

@app.route('/')

def index():
    # Obtener los objetos del bucket
    objects = s3.list_objects_v2(Bucket=BUCKET_NAME)  
    return render_template('index.html', objects=objects.get('Contents', []))  

@app.route('/create-folder', methods=['POST'])  
def create_folder():  
    folder_name = request.form['folder_name']  
    if not folder_name.endswith('/'):  
        folder_name += '/'  
    s3.put_object(Bucket=BUCKET_NAME, Key=folder_name)  
    return redirect(url_for('index'))  
  
@app.route('/delete-folder', methods=['POST'])  
def delete_folder():  
    folder_name = request.form['folder_name']  
    # Listar y eliminar todos los objetos dentro de la carpeta  
    objects_to_delete = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=folder_name).get('Contents', [])  
    for obj in objects_to_delete:  
        s3.delete_object(Bucket=BUCKET_NAME, Key=obj['Key'])  
    return redirect(url_for('index'))  
  
if __name__ == '__main__':  
    app.run(debug=True)  
