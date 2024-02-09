from flask import render_template, request, url_for, send_from_directory
from flask.views import MethodView
from logger import getLogger
import os
from config import UPLOAD_FOLDER
import easyocr

reader = easyocr.Reader(['en'])

logger = getLogger()

class Home(MethodView):
    def get(self):
        logger.info("Home route invoked")
        return render_template('base.html')

class ImageProcess(MethodView):
    def get(self):
        logger.info("Image Upload route invoked")
        return render_template('imageupload.html')
    
    def post(self):
        file_path = ""
        text_list = []
        if 'image' not in request.files:
            return 'No file part'

        file = request.files['image']

        if file.filename == '':
            return 'No selected file'
        else:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            result = reader.readtext(file_path)

            for detection in result:
                text_list.append(detection[1])

        return render_template('imageview.html', filename=file.filename, text_list=text_list)
