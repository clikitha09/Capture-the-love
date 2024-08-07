from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import io
from google.oauth2 import service_account
import googleapiclient.discovery
from googleapiclient.http import MediaIoBaseUpload

app = Flask(__name__)
app.secret_key = '02618e81a1ee2ef03f97d3d809f11cd55e9ff21a'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] =  500 * 1024 * 1024  # 16MB upload limit

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Google Drive API setup
SERVICE_ACCOUNT_FILE = "C:\\Users\\cliki\\OneDrive\\Desktop\\griha_pravesh\\gruha-pravesh-02618e81a1ee.json"
SCOPES = ['https://www.googleapis.com/auth/drive.file']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = googleapiclient.discovery.build('drive', 'v3', credentials=credentials)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # Upload to Google Drive
        folder_id = '1yk0ZynvzJvLASfw_8O2HzcsxDWqonKKK'
        file_metadata = {'name': filename, 'parents': [folder_id]}
        media = MediaIoBaseUpload(io.FileIO(file_path, 'rb'), mimetype=file.mimetype)
        drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        flash('File successfully uploaded')
        return redirect(url_for('upload_form'))

#if __name__ == "__main__":
 #   app.run(debug=True)
