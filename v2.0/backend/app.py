from sanic import Sanic
from urls import URLS

app = Sanic(__name__)

for url in URLS:
    app.add_route(url[0],url[1],methods=url[2],name=url[3])

if __name__ == '__main__':
    app.run(debug=True)