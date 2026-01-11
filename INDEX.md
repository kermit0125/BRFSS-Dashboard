# Project Index - Quick Navigation

## 📚 Documentation Files

| File | Purpose | Audience |
|------|---------|----------|
| [README.md](README.md) | Main project documentation | Everyone |
| [QUICKSTART.md](QUICKSTART.md) | 5-minute setup guide | New users |
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | Detailed setup instructions | Developers |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Executive summary | Managers |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | File organization | Developers |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines | Contributors |
| [CHANGELOG.md](CHANGELOG.md) | Version history | Everyone |

## 📖 Technical Documentation

| File | Purpose |
|------|---------|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture |
| [docs/DATA_PIPELINE.md](docs/DATA_PIPELINE.md) | Data processing pipeline |
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | Deployment guide |
| [docs/API.md](docs/API.md) | API documentation |

## 💻 Source Code

### Main Application
- `src/dashboard_app.py` - Main Dash application

### Data Cleaning Pipeline
- `src/data_cleaning/data_clean_Step0_preprocessing.py` - Text normalization
- `src/data_cleaning/data_clean_Step1.py` - QuestionID merging
- `src/data_cleaning/data_clean_Step2.py` - ResponseID merging
- `src/data_cleaning/data_clean_Step3.py` - BreakoutID merging
- `src/data_cleaning/data_clean_Step4.py` - Numeric cleaning
- `src/data_cleaning/data_clean_Step5.py` - Data aggregation
- `src/data_cleaning/data_clean_Step6.py` - Quality enhancement

### Scripts
- `scripts/run_pipeline.py` - Execute full pipeline

## 🗂️ Data Files

- `data/raw/` - Place raw dataset.csv here (gitignored)
- `data/processed/cleaned_data_final_enhanced.parquet` - Final processed data

## 🔧 Configuration Files

- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore rules
- `Makefile` - Convenient commands
- `.github/workflows/ci.yml` - CI/CD pipeline

## 🚀 Quick Commands

```bash
# Setup
make install          # Install dependencies
python scripts/run_pipeline.py  # Process data

# Development
make run              # Start dashboard
make lint             # Check code style
make format           # Format code
make test             # Run tests

# Cleanup
make clean            # Remove temporary files
```

## 📍 Key Locations

- **Dashboard**: `src/dashboard_app.py`
- **Data Pipeline**: `src/data_cleaning/`
- **Processed Data**: `data/processed/`
- **Documentation**: `docs/`
- **Scripts**: `scripts/`

## 🎯 Getting Started

1. Read [QUICKSTART.md](QUICKSTART.md) for 5-minute setup
2. Follow [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions
3. Review [README.md](README.md) for full documentation
4. Check [docs/](docs/) for technical details

## 🔍 For Different Roles

- **New Developer**: Start with [QUICKSTART.md](QUICKSTART.md) → [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Data Scientist**: Focus on [docs/DATA_PIPELINE.md](docs/DATA_PIPELINE.md)
- **Frontend Dev**: Check `src/dashboard_app.py` and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **DevOps**: See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- **Project Manager**: Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

