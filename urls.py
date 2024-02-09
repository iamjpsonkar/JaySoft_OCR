from ocr.ocrapp import Home, ImageProcess

URLS = [
    ('/',Home.as_view('Home'),['GET']),
    ('/image',ImageProcess.as_view('ImageProcess'),['GET','POST'])
]

