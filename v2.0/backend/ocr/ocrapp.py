from sanic.views import HTTPMethodView
from sanic.response import json

class Health(HTTPMethodView):
    async def get(self, request, *args, **kwargs):
        return json({
            "status" : 200,
            "message" : "Backend Server is running"
        })