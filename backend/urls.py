from ocr.ocrapp import OCR

URLS = [
    (OCR.as_view(), "/process/image", ["POST"], 'OCR'),
    (OCR.as_view(), "/images", ["GET"], 'images'),
]