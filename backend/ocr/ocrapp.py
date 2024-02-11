from sanic.views import HTTPMethodView
from sanic.response import json
from sanic.exceptions import FileNotFound
import httpx
import logging

import hashlib

from sqlalchemy import select
from .ocr_secrets import ocr_api, apikey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .models import Image, DB_URI
import uuid
import json as ujson

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Database initialization
database_url = DB_URI
engine = create_async_engine(DB_URI, echo=True, future=True)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession # type: ignore
)

class OCR(HTTPMethodView):
    async def get(self, request):
        logger.info("Get all images request invoked")
        async with SessionLocal() as session: # type: ignore
            query = await session.execute(select(Image))
            images = query.scalars().all()

        image_list = []
        for image in images:
            image_list.append({
                "base64html": image.base64image,
                "image_id": image.image_id,
                "image_name": image.image_name
            })

        return json(image_list)

    async def post(self, request):
        logger.info("OCR post request invoked")
        try:
            data = request.json
            base64_image = data.get("image")
            image_name = data.get("imageName")
            image_type = data.get("imageType")
            image_id = data.get("image_id")

            if not base64_image:
                raise FileNotFound("Image data is missing")

            if image_id == None:
                # Calculate checksum using base64Image
                image_id = hashlib.sha256(base64_image.encode()).hexdigest()

            async with SessionLocal() as session: # type: ignore
                image = await session.get(Image, image_id)
                if image:
                    # Image with given image_id exists in the database
                    response_data = ujson.loads(image.ocr_json)
                    return json({"image": base64_image, "response_data": response_data})

            # Process OCR if image not found in database
            response_data = await self.process_ocr(base64_image=base64_image, image_type=image_type)

            logger.info("ocr response", response_data)

            # Save image to database
            async with SessionLocal() as session: # type: ignore
                new_image = Image(
                    image_id=image_id,
                    image_name=image_name,
                    image_type=image_type,
                    base64image=base64_image,
                    ocr_json=ujson.dumps(response_data),
                )
                session.add(new_image)
                await session.commit()
            response = {
                "image": base64_image,
                "response_data": response_data
            }

            return json(response)
        except FileNotFound as e:
            logger.info({"error": str(e)}, 400)
            return json({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(
                {"error": "An error occurred while processing the image"}, exc_info=True
            )
            return json(
                {"error": "An error occurred while processing the image"}, status=500
            )

    async def process_ocr(self, base64_image, image_type=None):
        async def using_free_ocr(base64_image, image_type):
            # using free ocr api
            data_to_send = {
                "apikey": apikey,
                "base64Image": base64_image,
                "language": "eng",
                "OCREngine": 2,
            }

            try:
                data_to_send.update({"filetype": image_type.split("/")[1].upper()})
                logger.info(f'Image Type {image_type.split("/")[1].upper()}')
            except Exception as e:
                logger.info(f"Image Type Error {image_type}", e)
            response_data = {}
            async with httpx.AsyncClient() as client:
                response = await client.post(ocr_api, json=data_to_send)
                response_data = response.json()
            return response_data

        async def using_easy_ocr(base64_image):
            import base64
            from io import BytesIO
            import easyocr
            from PIL import Image

            # Decode Base64 string to obtain image bytes
            image_bytes = base64.b64decode(base64_image)

            # Convert bytes to PIL Image
            image = Image.open(BytesIO(image_bytes))

            # Convert RGBA image to RGB mode if necessary
            if image.mode == "RGBA":
                image = image.convert("RGB")

            # Convert PIL Image to bytes
            with BytesIO() as output:
                image.save(output, format="JPEG")
                image_bytes = output.getvalue()

            # Perform OCR using EasyOCR
            reader = easyocr.Reader(["en"])  # 'en' for English language
            result = reader.readtext(image_bytes)

            # Extract recognized text
            recognized_text = ' '.join(text[1] for text in result)
            return {"recognized_text": recognized_text}

        # return await using_free_ocr(base64_image,image_type)

        return await using_easy_ocr(base64_image)
