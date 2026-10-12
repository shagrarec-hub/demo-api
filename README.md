# Demo Flask API

A simple REST API with health check and data endpoints, built with local Ollama models.

## Features

- **GET /health** — Service health status with uptime
- **GET /api/data** — Sample dataset with optional `limit` parameter
- **Error handling** — Custom validation, 404, 405, 500 handlers
- **Type hints** — Full Python type annotations

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API
python app.py

# Test
curl http://localhost:5000/health
curl http://localhost:5000/api/data
curl http://localhost:5000/api/data?limit=2
```

## Testing

```bash
# Run tests
pytest test_app.py -v
```

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Service health status |
| `/api/data` | GET | Sample dataset |
| `/api/data?limit=N` | GET | First N items |

## Error Handling

| Status Code | Error Type | Description |
|-------------|------------|-------------|
| 400 | validation_error | Invalid parameters |
| 404 | not_found | Resource not found |
| 405 | method_not_allowed | HTTP method not allowed |
| 500 | internal_error | Server error |

## Built With

- Flask
- Python 3.9+
- Local Ollama models (no cloud)
