# Deployment Guide

## Local Development

### Prerequisites
- Python 3.8+
- Virtual environment
- Dependencies installed

### Run Locally
```bash
python src/dashboard_app.py
```

Access at: `http://127.0.0.1:8050`

## Production Deployment

### Option 1: Gunicorn

```bash
pip install gunicorn
gunicorn dashboard_app:server --bind 0.0.0.0:8050
```

### Option 2: Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
COPY data/processed/ ./data/processed/
EXPOSE 8050
CMD ["python", "src/dashboard_app.py"]
```

Build and run:
```bash
docker build -t brfss-dashboard .
docker run -p 8050:8050 brfss-dashboard
```

### Option 3: Cloud Platforms

#### Heroku
1. Create `Procfile`: `web: python src/dashboard_app.py`
2. Deploy: `git push heroku main`

#### Railway/Render
1. Connect GitHub repository
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `python src/dashboard_app.py`

## Environment Variables

Optional environment variables:
- `PORT`: Server port (default: 8050)
- `DEBUG`: Debug mode (default: False)
- `DATA_PATH`: Path to data file

## Performance Tuning

- Use production WSGI server (Gunicorn)
- Enable caching for callbacks
- Use CDN for static assets
- Consider data partitioning for very large datasets

