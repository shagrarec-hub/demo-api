"""
Flask REST API with health check and data endpoints.

Run with:
    pip install flask
    python app.py
"""

from __future__ import annotations

import logging
import time
from typing import Any

from flask import Flask, jsonify, request

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app: Flask = Flask(__name__)
app.json.sort_keys = False  # preserve key order in responses

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)

# Simulated in-memory data store
SAMPLE_DATA: dict[str, Any] = {
    "id": 1,
    "name": "Flask API",
    "version": "1.0.0",
    "items": [
        {"id": 1, "label": "alpha"},
        {"id": 2, "label": "beta"},
        {"id": 3, "label": "gamma"},
    ],
}

START_TIME: float = time.time()


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.route("/health", methods=["GET"])
def health() -> tuple[dict[str, Any], int]:
    """Return service health status."""
    status: dict[str, Any] = {
        "status": "healthy",
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    return jsonify(status), 200


@app.route("/api/data", methods=["GET"])
def get_data() -> tuple[dict[str, Any], int]:
    """Return the sample dataset.

    Query params:
        limit (int) – max number of items to return (default: all)
    """
    limit: int | None = request.args.get("limit", type=int)

    if limit is not None and limit < 0:
        raise ValidationError("'limit' must be a non-negative integer")

    data: dict[str, Any] = dict(SAMPLE_DATA)
    if limit is not None:
        data["items"] = data["items"][:limit]

    return jsonify(data), 200


# ---------------------------------------------------------------------------
# Custom exceptions
# ---------------------------------------------------------------------------


class ValidationError(Exception):
    """Raised when a request parameter is invalid."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------


@app.errorhandler(ValidationError)
def handle_validation_error(exc: ValidationError) -> tuple[dict[str, str], int]:
    logger.warning("Validation error: %s", exc.message)
    return jsonify({"error": "validation_error", "message": exc.message}), 400


@app.errorhandler(404)
def handle_not_found(_exc: Exception) -> tuple[dict[str, str], int]:
    return jsonify({"error": "not_found", "message": "Resource not found"}), 404


@app.errorhandler(405)
def handle_method_not_allowed(_exc: Exception) -> tuple[dict[str, str], int]:
    return jsonify({"error": "method_not_allowed", "message": "HTTP method not allowed"}), 405


@app.errorhandler(500)
def handle_server_error(_exc: Exception) -> tuple[dict[str, str], int]:
    logger.exception("Unhandled server error")
    return jsonify({"error": "internal_error", "message": "Something went wrong"}), 500


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
