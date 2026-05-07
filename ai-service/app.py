import os
import time

from dotenv import load_dotenv
from flask import Flask, jsonify

from routes.describe import describe_bp
from routes.recommend import recommend_bp
from routes.generate_report import generate_report_bp


def create_app() -> Flask:
    load_dotenv()

    app = Flask(__name__)
    app.config["START_TIME"] = time.time()
    app.config["GROQ_MODEL"] = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    app.register_blueprint(describe_bp)
    app.register_blueprint(recommend_bp)
    app.register_blueprint(generate_report_bp)

    @app.get("/")
    def index():
        return jsonify(
            {
                "service": "ai-service",
                "endpoints": {
                    "health": "GET /health",
                    "describe": "POST /describe",
                    "recommend": "POST /recommend",
                    "generate_report": "POST /generate-report",
                },
            }
        )

    @app.get("/health")
    def health():
        uptime_s = max(0, int(time.time() - app.config["START_TIME"]))
        return jsonify(
            {
                "status": "ok",
                "service": "ai-service",
                "model": app.config["GROQ_MODEL"],
                "uptime_s": uptime_s,
            }
        )

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=False
    )