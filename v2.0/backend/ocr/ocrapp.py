from sanic.views import HTTPMethodView
from sanic.response import json
from sanic.exceptions import FileNotFound
import base64
# from app import logger
import logging

# logger = getLogger()
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
            
            # Check if image exists
            if not base64_image:
                raise FileNotFound("Image data is missing")

            # Decode base64 image data
            image_data = base64.b64decode(base64_image)

            # Save the decoded image to a desired location
            filename = 'uploaded_image.png'  # Example filename
            with open("uploads/"+filename, 'wb') as f:
                f.write(image_data)

            # Respond with a success message or any other data
            return json({'message': 'Image uploaded successfully'})
        except FileNotFound as e:
            logger.info({'error': str(e)}, 400)
            return json({'error': str(e)}, status=400)
        except Exception as e:
            logger.info({'error': 'An error occurred while processing the image'}, 500)
            return json({'error': 'An error occurred while processing the image'}, status=500)
