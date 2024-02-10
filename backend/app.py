from sanic import Sanic
from urls import URLS
from sanic_cors import CORS

app = Sanic(__name__)
CORS(app)

for url in URLS:
    app.add_route(url[0],url[1],methods=url[2],name=url[3])

if __name__ == '__main__':
    app.run(debug=True)