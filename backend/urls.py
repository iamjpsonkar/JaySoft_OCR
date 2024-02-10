from ocr.ocrapp import Health, OCR

URLS = [
    (Health.as_view(), "/backend/healthz", ["GET"], 'healthz_get'),
    (OCR.as_view(), "/process/image", ["GET", "POST"], 'OCR'),
]