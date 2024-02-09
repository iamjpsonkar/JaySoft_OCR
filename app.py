from flask import Flask, render_template
from logger import getLogger

app = Flask(__name__)
logger = getLogger()

@app.route("/")
def home():
    logger.info("Home route invoked")
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)