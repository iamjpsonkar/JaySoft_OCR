from sanic.views import HTTPMethodView
from sanic.response import json
from sanic.exceptions import FileNotFound
import httpx
import logging
from .ocr_secrets import ocr_api, apikey

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Health(HTTPMethodView):
    async def get(self, request):
        logger.info("Healthz get request invoked")
        return json({
            "status" : 200,
            "message" : "Backend Server is running"
        })

class OCR(HTTPMethodView):
    async def get(self, request):
        logger.info("OCR get request invoked")
        return json({
            "status" : 200,
            "message" : "GET request received"
        })

    async def post(self, request):
        logger.info("OCR post request invoked")
        try:
            data = request.json
            base64_image = data.get('image')

            if not base64_image:
                raise FileNotFound("Image data is missing")

            data_to_send = {
                "apikey": apikey,
                "base64Image" : base64_image,
                "OCREngine": 3
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(ocr_api, json=data_to_send)
                response_data = response.json()
            logger.info("ocr_api_response",response_data)
            return json(response_data)
        except FileNotFound as e:
            logger.info({'error': str(e)}, 400)
            return json({'error': str(e)}, status=400)
        except Exception as e:
            logger.info({'error': 'An error occurred while processing the image'}, 500)
            return json({'error': 'An error occurred while processing the image'}, status=500)