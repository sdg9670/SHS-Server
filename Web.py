from flask import Flask, render_template, request
from werkzeug import secure_filename
import requests as rq
app = Flask(__name__)


@app.route('/')
def hello():
    return hello

@app.route('/upload')
def upload_file():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':

        f = request.files['file']
        f.save(secure_filename(f.filename))
        print(f)
        return 'file uploaded successfully'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
'''
import requests
url = 'http://simddong.ga/uploader'
payload = {'file': filename}
r = requests.post(url, data=payload)
print(r.text)
print(r.status_code)

    rq.post('simddong.ga:5000/uploader', files={'file': ('main.py', open('main.py', 'rb'))})
'''