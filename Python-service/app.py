from flask import Flask
from routes.report import report_bp
from config import load_config

app = Flask(__name__)
app.register_blueprint(report_bp, url_prefix="/api/v1")


if __name__ == "__main__":
    config = load_config()
    app.run(port=config.port, debug=False)
