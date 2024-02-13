from flask import Flask, render_template, send_from_directory, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
import os

auth = HTTPBasicAuth()

users = {'username': 'mmlab', 'password': '50984309'}


@auth.get_password
def get_password(username):
    if users['username'] == username:
        return users['password']
    return None

app = Flask(__name__)

# 設定靜態資料夾的路徑
static_folder = './static/'

@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        print(request.files)
        f.save("uploadFile/" + secure_filename(f.filename))
        return 'file uploaded successfully'
    else:
        return '404 error'
    
@app.route('/')
@auth.login_required
def index():
    # 取得靜態資料夾中的檔案列表
    file_list = os.listdir(static_folder)
    return render_template('index.html', files=file_list)

@app.route('/download/<filename>')
def download(filename):
    # 建立下載的超連結
    return send_from_directory(static_folder, filename, as_attachment=True)

if __name__ == '__main__':
    app.run("140.136.146.81", port=80)
