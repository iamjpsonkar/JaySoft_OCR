from sanic.views import HTTPMethodView
from sanic.response import json
from sanic.exceptions import FileNotFound
import httpx
import logging
from .ocr_secrets import ocr_api, apikey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .models import Image, DB_URI
import uuid
import json as ujson

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database initialization
database_url = DB_URI
engine = create_async_engine(DB_URI, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

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
            image_name = data.get('imageName')
            image_type = data.get('imageType')

            if not base64_image:
                raise FileNotFound("Image data is missing")

            data_to_send = {
                "apikey": apikey,
                "base64Image" : base64_image,
                "language": "eng",
                "OCREngine": 2
            }

            try:
                data_to_send.update({
                    "filetype": image_type.split("/")[1].upper()
                })
                logger.info(f'Image Type {image_type.split("/")[1].upper()}')
            except Exception as e:
                logger.info(f"Image Type Error {image_type}", e)
            response_data = {}
            async with httpx.AsyncClient() as client:
                response = await client.post(ocr_api, json=data_to_send)
                response_data = response.json()

            # Generate UUID for image ID
            image_id = str(uuid.uuid4())

            # Save image to database
            async with SessionLocal() as session:
                new_image = Image(
                    image_id=image_id,
                    image_name=image_name,
                    image_type=image_type,
                    base64image=base64_image,
                    ocr_json=ujson.dumps(response_data)
                )
                session.add(new_image)
                await session.commit()

            logger.info("ocr_api_response",response_data)
            return json(response_data)
        except FileNotFound as e:
            logger.info({'error': str(e)}, 400)
            return json({'error': str(e)}, status=400)
        except Exception as e:
            logger.error({'error': 'An error occurred while processing the image'}, exc_info=True)
            return json({'error': 'An error occurred while processing the image'}, status=500)
