# Setup Guide for SDEs

## Initial Setup (First Time)

### 1. Clone Repository
```bash
git clone <repository-url>
cd BRFSS-Dashboard
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Download Data
- Download BRFSS dataset from [CDC Data Portal](https://data.cdc.gov/Behavioral-Risk-Factors/Behavioral-Risk-Factor-Surveillance-System-BRFSS-P/dttw-5yxu)
- Place `dataset.csv` in `data/raw/` directory
- Create directory if it doesn't exist: `mkdir -p data/raw`

### 5. Run Data Pipeline
```bash
python scripts/run_pipeline.py
```

This will:
- Process raw data through 7 cleaning steps
- Generate `data/processed/cleaned_data_final_enhanced.parquet`
- Create `data/reports/data_quality_report.txt`

### 6. Verify Setup
```bash
# Check if processed data exists
ls data/processed/cleaned_data_final_enhanced.parquet

# Run dashboard
python src/dashboard_app.py
```

## Daily Development Workflow

### Starting Work
```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate

# Pull latest changes
git pull origin main

# Run dashboard
make run  # or python src/dashboard_app.py
```

### Making Changes
```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes...

# Format code
make format

# Run linter
make lint

# Run tests
make test

# Commit changes
git add .
git commit -m "feat: description of changes"
git push origin feature/your-feature
```

## Environment Variables

Create `.env` file (optional):
```
PORT=8050
DEBUG=False
DATA_PATH=data/processed/cleaned_data_final_enhanced.parquet
```

## Troubleshooting

### Issue: ModuleNotFoundError
**Solution**: Ensure virtual environment is activated and dependencies installed

### Issue: Data file not found
**Solution**: Run data pipeline first: `python scripts/run_pipeline.py`

### Issue: Port already in use
**Solution**: 
```bash
# Find process using port 8050
lsof -i :8050  # macOS/Linux
netstat -ano | findstr :8050  # Windows

# Kill process or change port in dashboard_app.py
```

### Issue: Memory errors during data processing
**Solution**: 
- Process data in chunks
- Increase system RAM
- Use 64-bit Python

## IDE Configuration

### VS Code
1. Install Python extension
2. Select Python interpreter (venv)
3. Configure `.vscode/settings.json`:
```json
{
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true
}
```

### PyCharm
1. Open project
2. File → Settings → Project → Python Interpreter
3. Select venv interpreter
4. Mark `src/` as Sources Root

