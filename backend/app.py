from sanic import Sanic
from urls import URLS
from sanic_cors import CORS
from ocr.ocrapp import engine
from ocr.models import Base
import asyncio

app = Sanic(__name__)
CORS(app)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)

for url in URLS:
    app.add_route(url[0],url[1],methods=url[2],name=url[3])


if __name__ == '__main__':
    asyncio.run(create_tables())
    app.run(debug=True)