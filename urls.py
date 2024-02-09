from ocr.ocrapp import Home, OCR, ImageProcess

URLS = [
    ('/',Home.as_view('Home'),['GET']),
    ('/image',ImageProcess.as_view('ImageProcess'),['GET','POST']),
    ('/ocr/',OCR.as_view('OCR'),['GET']),
]

