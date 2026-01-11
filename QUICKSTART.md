# Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Download Data
Place `dataset.csv` in `data/raw/` directory

### 3. Run Data Pipeline
```bash
python scripts/run_pipeline.py
```

### 4. Start Dashboard
```bash
python src/dashboard_app.py
```

### 5. Open Browser
Navigate to: `http://127.0.0.1:8050`

## Common Issues

### Issue: Module not found
**Solution**: Ensure you're in the project root directory and virtual environment is activated

### Issue: Data file not found
**Solution**: Check that `data/processed/cleaned_data_final_enhanced.parquet` exists

### Issue: Port already in use
**Solution**: Change port in `dashboard_app.py` or kill process using port 8050

## Next Steps

- Read [README.md](README.md) for full documentation
- Check [docs/](docs/) for detailed guides
- Explore the dashboard features

