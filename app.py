from flask import Flask, send_from_directory
from urls import URLS
from logger import getLogger
from config import UPLOAD_FOLDER
import os

logger = getLogger()

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER']), filename)

for url in URLS:
    app.add_url_rule(rule=url[0],view_func=url[1],methods=url[2])


if __name__ == '__main__':
    app.run(debug=True)