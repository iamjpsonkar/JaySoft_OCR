from flask import render_template, request, url_for, send_from_directory
from flask.views import MethodView
from logger import getLogger
import os
from config import UPLOAD_FOLDER

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
        if 'image' not in request.files:
            return 'No file part'

        file = request.files['image']

        if file.filename == '':
            return 'No selected file'
        else:

            # Ensure the uploads directory exists
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            # Save the file with its original name to the uploads directory
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

        # Pass the image filename to the template for display
        return render_template('imageview.html', filename=file.filename)

class OCR(MethodView):
    def get(self):
        logger.info("OCR route invoked")
        return render_template('base.html')