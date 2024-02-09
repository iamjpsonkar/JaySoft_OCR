from flask import Flask
from logger import getLogger

app = Flask(__name__)
logger = getLogger()

@app.route("/")
def home():
    logger.info("Home route invoked")
    return "<h1>Welcome</h1>"

if __name__ == '__main__':
    app.run(debug=True)