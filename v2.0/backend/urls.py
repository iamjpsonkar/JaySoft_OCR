from ocr.ocrapp import Health


URLS = [
    (Health.as_view(), "/backend/healthz", ["GET"], 'healthz_get'),
]