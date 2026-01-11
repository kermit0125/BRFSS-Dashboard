# BRFSS Dashboard - Behavioral Risk Factor Surveillance System Data Explorer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Dash](https://img.shields.io/badge/Dash-2.14+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production-brightgreen.svg)

**An interactive, production-ready web dashboard for exploring CDC's Behavioral Risk Factor Surveillance System (BRFSS) data**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Architecture](#architecture) • [Documentation](#documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Data Pipeline](#data-pipeline)
- [Architecture](#architecture)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The BRFSS Dashboard is a comprehensive data visualization platform that enables researchers, public health professionals, and policymakers to explore and analyze health-related survey data from the Centers for Disease Control and Prevention (CDC). The system processes over 1.7 million records from the Behavioral Risk Factor Surveillance System (BRFSS), providing interactive visualizations across multiple dimensions including demographics, geography, and temporal trends.

### Key Highlights

- **Data Scale**: Processes 1.7M+ records with 98 unique health questions
- **Geographic Coverage**: 56 U.S. states and territories
- **Time Range**: 2011-2023 (13 years of data)
- **Data Quality**: Automated quality filtering and validation
- **Interactive Visualizations**: 7 multi-dimensional analysis panels

### What is BRFSS?

The Behavioral Risk Factor Surveillance System (BRFSS) is the world's largest, ongoing telephone health survey system, tracking health conditions and risk behaviors in the United States since 1984. It collects data from over 400,000 adult interviews annually across all 50 states, the District of Columbia, and U.S. territories.

---

## ✨ Features

### 🎨 Interactive Dashboard

- **Multi-Dimensional Analysis**: Explore data across 7 different dimensions
  - Overall distribution analysis
  - Gender-based comparisons
  - Age group analysis (with granularity control)
  - Education level comparisons
  - Household income analysis
  - Geographic distribution (interactive U.S. map)
  - Temporal trends (2011-2023)

- **Advanced Filtering**
  - Hierarchical question selection (Class → Topic → Question)
  - Response option selector for geographic analysis
  - Age granularity toggle (7 groups vs 3 groups)

- **Enhanced Visualizations**
  - Confidence intervals displayed on all charts
  - Interactive hover tooltips with detailed statistics
  - Professional color schemes optimized for data ranges
  - Responsive design for various screen sizes

### 📊 Data Quality & Processing

- **Automated Data Cleaning Pipeline**
  - 7-step cleaning process (Step0-Step6)
  - Handles historical data inconsistencies
  - Merges duplicate QuestionIDs, ResponseIDs, and BreakoutIDs
  - Normalizes text fields and handles missing values

- **Quality Filters**
  - Minimum sample size threshold (≥30 for statistical reliability)
  - Confidence interval validation
  - Data consistency checks
  - Geographic data validation

- **Statistical Accuracy**
  - Proper aggregation with sample size weighting
  - 95% confidence interval recalculation
  - Binomial distribution approximation

### 🗺️ Geographic Visualization

- **Interactive U.S. Map**
  - Choropleth visualization with intelligent color mapping
  - Response selector for different survey responses
  - Statistical summary panel (mean, median, min, max, std dev)
  - Enhanced hover information with confidence intervals

- **Smart Color Scaling**
  - Automatic color scheme selection based on data range
  - Perceptually uniform color spaces (Viridis, Plasma, Cividis)
  - Full data range utilization

---

## 🛠️ Technology Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.8+ | Core programming language |
| **Pandas** | 2.0+ | Data manipulation and analysis |
| **NumPy** | 1.24+ | Numerical computations |
| **PyArrow** | 12.0+ | Parquet file handling |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Dash** | 2.14+ | Web application framework |
| **Plotly** | 5.17+ | Interactive visualizations |
| **Plotly Express** | 5.17+ | High-level chart creation |
| **HTML/CSS** | - | UI styling and layout |

### Data Processing

| Component | Purpose |
|-----------|---------|
| **Data Cleaning Pipeline** | 7-step automated cleaning process |
| **Parquet Format** | Efficient data storage and retrieval |
| **Quality Validation** | Automated data quality checks |

### Development Tools

| Tool | Purpose |
|------|---------|
| **Git** | Version control |
| **VS Code / PyCharm** | IDE recommendations |
| **Jupyter Notebook** | Data exploration (optional) |

---

## 📁 Project Structure

```
BRFSS-Dashboard/
│
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── setup.py                 # Package setup (optional)
│
├── src/                     # Source code
│   ├── dashboard_app.py    # Main dashboard application
│   ├── data_cleaning/      # Data cleaning pipeline
│   │   ├── step0_preprocessing.py
│   │   ├── step1_question_merge.py
│   │   ├── step2_response_merge.py
│   │   ├── step3_breakout_merge.py
│   │   ├── step4_numeric_clean.py
│   │   ├── step5_aggregation.py
│   │   └── step6_quality_enhancement.py
│   └── utils/              # Utility functions
│       └── data_loader.py
│
├── data/                    # Data files
│   ├── raw/                # Raw data (not in repo)
│   │   └── dataset.csv
│   ├── processed/          # Processed data
│   │   ├── cleaned_data_final_enhanced.parquet
│   │   └── cleaned_data_final.parquet
│   └── reports/            # Quality reports
│       └── data_quality_report.txt
│
├── docs/                    # Documentation
│   ├── ARCHITECTURE.md     # System architecture
│   ├── DATA_PIPELINE.md    # Data processing pipeline
│   ├── API.md              # API documentation
│   └── DEPLOYMENT.md       # Deployment guide
│
├── scripts/                 # Utility scripts
│   ├── run_pipeline.py     # Run full cleaning pipeline
│   └── validate_data.py    # Data validation script
│
└── tests/                   # Unit tests (optional)
    └── test_data_cleaning.py
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 8GB+ RAM recommended for data processing
- Modern web browser (Chrome, Firefox, Edge)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd BRFSS-Dashboard
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download Data

1. Download BRFSS data from [CDC Data Portal](https://data.cdc.gov/Behavioral-Risk-Factors/Behavioral-Risk-Factor-Surveillance-System-BRFSS-P/dttw-5yxu)
2. Place `dataset.csv` in `data/raw/` directory

### Step 5: Run Data Cleaning Pipeline

```bash
python scripts/run_pipeline.py
```

This will generate `data/processed/cleaned_data_final_enhanced.parquet`

---

## 💻 Usage

### Starting the Dashboard

```bash
python src/dashboard_app.py
```

The dashboard will be available at: `http://127.0.0.1:8050`

### Using the Dashboard

1. **Select a Question**
   - Choose a Class (e.g., "Health Status")
   - Select a Topic (e.g., "General Health")
   - Pick a Question (e.g., "Would you say that in general your health is...")

2. **Explore Visualizations**
   - **Overall Panel**: View distribution across all responses
   - **Gender Panel**: Compare by sex
   - **Age Panel**: Analyze by age groups (toggle granularity)
   - **Education Panel**: Compare by education level
   - **Income Panel**: Analyze by household income
   - **Geographic Panel**: View U.S. map (select response to display)
   - **Temporal Panel**: See trends over time (2011-2023)

3. **Interact with Charts**
   - Hover over bars/points for detailed information
   - Use Plotly's built-in zoom and pan features
   - Click legend items to show/hide series

### Command Line Options

```bash
# Run with custom port
python src/dashboard_app.py --port 8080

# Run with debug mode
python src/dashboard_app.py --debug
```

---

## 🔄 Data Pipeline

### Overview

The data cleaning pipeline consists of 7 sequential steps, each handling specific data quality issues:

```
Raw Data (dataset.csv)
    ↓
Step 0: Preprocessing
    ↓
Step 1: QuestionID Merging
    ↓
Step 2: ResponseID Merging
    ↓
Step 3: BreakoutID Merging
    ↓
Step 4: Numeric Cleaning
    ↓
Step 5: Aggregation
    ↓
Step 6: Quality Enhancement
    ↓
Final Data (cleaned_data_final_enhanced.parquet)
```

### Step Details

#### Step 0: Preprocessing
- Text normalization (Class, Topic, Question)
- Response text standardization
- Special character handling
- Encoding issue resolution

#### Step 1: QuestionID Merging
- Merges duplicate QuestionIDs for identical questions
- Selects shortest QuestionID as canonical
- Preserves original QuestionID for reference

#### Step 2: ResponseID Merging
- Handles historical response changes
- Merges variants (e.g., "Emplyd" → "Employed")
- Consolidates income brackets
- Unifies race/ethnicity categories

#### Step 3: BreakoutID Merging
- Normalizes age groups (7 categories)
- Consolidates income brackets (5 categories)
- Unifies education levels
- Standardizes race/ethnicity categories

#### Step 4: Numeric Cleaning
- Type conversion and validation
- Filters invalid samples (Sample_Size ≤ 0)
- Validates percentage ranges (0-100%)
- Generates proportion and persons columns

#### Step 5: Aggregation
- Aggregates duplicate rows
- Recalculates confidence intervals
- Uses binomial distribution approximation
- Maintains statistical accuracy

#### Step 6: Quality Enhancement
- Missing value handling
- Data consistency validation
- Geographic data validation
- Year range verification
- Statistical anomaly detection
- Generates quality report

### Running the Pipeline

```bash
# Run all steps sequentially
python scripts/run_pipeline.py

# Run individual steps
python src/data_cleaning/step0_preprocessing.py
python src/data_cleaning/step1_question_merge.py
# ... etc
```

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│              (Web Browser - Dash Frontend)              │
└────────────────────┬────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              Dash Application Server                     │
│  ┌──────────────────────────────────────────────────┐   │
│  │         Dashboard App (dashboard_app.py)         │   │
│  │  - Callbacks for interactivity                    │   │
│  │  - Chart generation functions                    │   │
│  │  - Data aggregation logic                        │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              Data Layer                                  │
│  ┌──────────────────────────────────────────────────┐   │
│  │     Parquet Data Files (Enhanced/Cleaned)        │   │
│  │  - cleaned_data_final_enhanced.parquet           │   │
│  │  - Fast columnar storage                         │   │
│  │  - Efficient querying                            │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Component Architecture

#### Frontend Components

1. **Header Component**
   - Title and description
   - Data source indicator
   - Quality filter status

2. **Filter Card**
   - Class/Topic/Question dropdowns
   - Age granularity toggle
   - Question information panel

3. **Visualization Cards** (7 panels)
   - Overall analysis chart
   - Gender comparison chart
   - Age analysis chart
   - Education comparison chart
   - Income analysis chart
   - Geographic map
   - Temporal trend chart

#### Backend Components

1. **Data Loader**
   - Automatic dataset detection
   - Quality filtering
   - Type validation

2. **Aggregation Engine**
   - Group-by operations
   - Confidence interval calculation
   - Statistical computations

3. **Chart Generators**
   - Bar charts with CI
   - Grouped bar charts
   - Choropleth maps
   - Temporal line charts

### Data Flow

```
User Selection (Class/Topic/Question)
    ↓
Filter Dataset
    ↓
Aggregate by Dimension
    ↓
Calculate Statistics
    ↓
Generate Visualizations
    ↓
Render in Browser
```

---

## 📚 API Documentation

### Dashboard Callbacks

#### `update_topic_dropdown(class_value)`
Updates topic dropdown based on selected class.

**Inputs:**
- `class-dropdown.value`: Selected class

**Outputs:**
- `topic-dropdown.options`: Available topics
- `topic-dropdown.value`: Default topic

#### `update_question_dropdown(class_value, topic_value)`
Updates question dropdown based on selected class and topic.

**Inputs:**
- `class-dropdown.value`: Selected class
- `topic-dropdown.value`: Selected topic

**Outputs:**
- `question-dropdown.options`: Available questions
- `question-dropdown.value`: Default question

#### `update_map_response_dropdown(class_value, topic_value, question_value)`
Updates response dropdown for geographic map.

**Inputs:**
- `class-dropdown.value`: Selected class
- `topic-dropdown.value`: Selected topic
- `question-dropdown.value`: Selected question

**Outputs:**
- `map-response-dropdown.options`: Available responses
- `map-response-dropdown.value`: Default response

#### `update_all_panels(class_value, topic_value, question_value, age_mode, map_response)`
Main callback that updates all visualization panels.

**Inputs:**
- `class-dropdown.value`: Selected class
- `topic-dropdown.value`: Selected topic
- `question-dropdown.value`: Selected question
- `age-mode-radio.value`: Age granularity ("more" or "less")
- `map-response-dropdown.value`: Selected response for map

**Outputs:**
- `overall-graph.figure`: Overall analysis chart
- `gender-graph.figure`: Gender comparison chart
- `age-graph.figure`: Age analysis chart
- `education-graph.figure`: Education comparison chart
- `income-graph.figure`: Income analysis chart
- `location-graph.figure`: Geographic map
- `year-graph.figure`: Temporal trend chart
- `map-stats-panel.children`: Geographic statistics panel

### Core Functions

#### `aggregate_groups(sub_df, group_cols)`
Aggregates data by specified columns and recalculates confidence intervals.

**Parameters:**
- `sub_df`: DataFrame subset
- `group_cols`: List of columns to group by

**Returns:**
- DataFrame with aggregated statistics

#### `make_location_map(df_q, selected_response=None)`
Creates enhanced geographic visualization.

**Parameters:**
- `df_q`: Filtered DataFrame for selected question
- `selected_response`: Response to display (optional)

**Returns:**
- `(figure, responses, stats)`: Plotly figure, available responses, statistics

---

## 🧪 Development

### Development Workflow (SDE Best Practices)

#### 1. Environment Setup

```bash
# Clone repository
git clone <repository-url>
cd BRFSS-Dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development tools (optional)
pip install black flake8 mypy pytest
```

#### 2. Code Style & Standards

**Python Style Guide (PEP 8)**:
- Maximum line length: 100 characters
- Use 4 spaces for indentation
- Use descriptive variable names
- Add type hints for function parameters and returns

**Code Formatting**:
```bash
# Format code with Black
black src/

# Check style with flake8
flake8 src/ --max-line-length=100

# Type checking with mypy
mypy src/
```

**Documentation Standards**:
- All functions must have docstrings
- Use Google-style docstrings
- Document complex algorithms
- Include examples in docstrings

#### 3. Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: add new feature description"

# Push and create PR
git push origin feature/your-feature-name
```

**Commit Message Convention**:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

#### 4. Testing Strategy

**Unit Tests**:
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/ --cov-report=html

# Run specific test file
pytest tests/test_data_cleaning.py
```

**Test Structure**:
```
tests/
├── test_data_cleaning.py
├── test_dashboard.py
└── test_utils.py
```

**Integration Tests**:
- Test data pipeline end-to-end
- Test dashboard callbacks
- Test data loading and filtering

#### 5. Code Review Process

1. **Self-Review**: Review your own code before submitting PR
2. **Peer Review**: At least one reviewer required
3. **Automated Checks**: CI/CD runs linting and tests
4. **Documentation**: Update docs for user-facing changes

#### 6. Debugging

**Local Debugging**:
```python
# Enable debug mode
app.run(debug=True, host='127.0.0.1', port=8050)
```

**Debugging Tools**:
- Use Python debugger (pdb)
- Use IDE breakpoints
- Check browser console for frontend issues
- Review server logs

#### 7. Performance Profiling

```python
# Profile data loading
import cProfile
cProfile.run('load_data()')

# Memory profiling
from memory_profiler import profile
@profile
def your_function():
    ...
```

#### 8. Continuous Integration

**GitHub Actions** (example):
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest tests/
      - run: flake8 src/
```

### Development Best Practices

1. **Modular Design**: Keep functions focused and reusable
2. **Error Handling**: Use try-except blocks appropriately
3. **Logging**: Use Python logging module for debugging
4. **Configuration**: Use environment variables for settings
5. **Documentation**: Keep code and docs in sync
6. **Version Control**: Commit frequently with clear messages
7. **Code Review**: Always review before merging
8. **Testing**: Write tests for new features

---

## 📊 Data Quality

### Quality Metrics

- **Completeness**: 99.76% (only 0.24% missing confidence intervals)
- **Validity**: All records pass range checks
- **Consistency**: Automated validation of relationships
- **Reliability**: Minimum sample size ≥ 30

### Quality Report

After running Step 6, check `data/reports/data_quality_report.txt` for:
- Missing value statistics
- Numeric field distributions
- Categorical field unique counts
- Year distribution
- Data quality metrics

---

## 🚢 Deployment

### Local Deployment

```bash
python src/dashboard_app.py
```

### Production Deployment

#### Option 1: Using Gunicorn

```bash
pip install gunicorn
gunicorn dashboard_app:server
```

#### Option 2: Using Docker

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

#### Option 3: Deploy to Heroku/Railway/Render

1. Create `Procfile`:
```
web: python src/dashboard_app.py
```

2. Deploy using platform CLI

---

## 🤝 Contributing

### Contribution Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Review Process

- All code must pass linting checks
- Tests must be added for new features
- Documentation must be updated
- Code must follow project style guide

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **CDC** for providing the BRFSS dataset
- **Plotly** for excellent visualization libraries
- **Dash** team for the web framework
- **Pandas** community for data processing tools

---

## 👥 Team & Roles

### Software Development Engineer (SDE) Workflow

This project follows industry-standard SDE practices:

#### Frontend Development
- **Framework**: Dash (Python-based, no separate frontend build)
- **Components**: Dash HTML Components, Dash Core Components
- **Styling**: Inline CSS with modern design system
- **Interactivity**: Dash callbacks for real-time updates

#### Backend Development
- **Language**: Python 3.8+
- **Data Processing**: Pandas, NumPy
- **API**: Dash server (no REST API needed)
- **Data Storage**: Parquet files (columnar format)

#### Data Engineering
- **Pipeline**: 7-step ETL process
- **Quality**: Automated validation and filtering
- **Format**: Parquet for efficient storage
- **Monitoring**: Quality reports and logs

#### DevOps
- **Deployment**: Gunicorn, Docker, or cloud platforms
- **CI/CD**: GitHub Actions (recommended)
- **Monitoring**: Application logs and error tracking
- **Scaling**: Horizontal scaling with load balancer

### Development Roles

| Role | Responsibilities | Key Files |
|------|-----------------|-----------|
| **Frontend Developer** | UI/UX, Dash components, styling | `src/dashboard_app.py` |
| **Backend Developer** | Data processing, callbacks, logic | `src/dashboard_app.py`, `src/data_cleaning/` |
| **Data Engineer** | Pipeline, quality, ETL | `src/data_cleaning/*.py` |
| **DevOps Engineer** | Deployment, CI/CD, infrastructure | `docs/DEPLOYMENT.md`, `.github/workflows/` |
| **QA Engineer** | Testing, validation, quality assurance | `tests/`, `data_quality_report.txt` |

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/kermit0125/BRFSS-Dashboard/issues)
- **Email**: [xing.kem@northeastern.edu]
- **Documentation**: [Full Documentation](docs/)
- **Quick Start**: See [QUICKSTART.md](QUICKSTART.md)

---

## 📈 Future Enhancements

- [ ] Add data export functionality (CSV, Excel, PDF)
- [ ] Implement user authentication
- [ ] Add comparison mode (compare two questions)
- [ ] Create API endpoints for data access
- [ ] Add machine learning predictions
- [ ] Implement caching for better performance
- [ ] Add unit tests and integration tests
- [ ] Create Docker containerization
- [ ] Add CI/CD pipeline

---

<div align="center">

**Built with ❤️ for Public Health Research**

[Back to Top](#brfss-dashboard---behavioral-risk-factor-surveillance-system-data-explorer)

</div>
# BRFSS Dashboard - Behavioral Risk Factor Surveillance System Data Explorer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Dash](https://img.shields.io/badge/Dash-2.14+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production-brightgreen.svg)

**An interactive, production-ready web dashboard for exploring CDC's Behavioral Risk Factor Surveillance System (BRFSS) data**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Architecture](#architecture) • [Documentation](#documentation)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Data Pipeline](#data-pipeline)
- [Architecture](#architecture)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

The BRFSS Dashboard is a comprehensive data visualization platform that enables researchers, public health professionals, and policymakers to explore and analyze health-related survey data from the Centers for Disease Control and Prevention (CDC). The system processes over 1.7 million records from the Behavioral Risk Factor Surveillance System (BRFSS), providing interactive visualizations across multiple dimensions including demographics, geography, and temporal trends.

### Key Highlights

- **Data Scale**: Processes 1.7M+ records with 98 unique health questions
- **Geographic Coverage**: 56 U.S. states and territories
- **Time Range**: 2011-2023 (13 years of data)
- **Data Quality**: Automated quality filtering and validation
- **Interactive Visualizations**: 7 multi-dimensional analysis panels

### What is BRFSS?

The Behavioral Risk Factor Surveillance System (BRFSS) is the world's largest, ongoing telephone health survey system, tracking health conditions and risk behaviors in the United States since 1984. It collects data from over 400,000 adult interviews annually across all 50 states, the District of Columbia, and U.S. territories.

---

## ✨ Features

### 🎨 Interactive Dashboard

- **Multi-Dimensional Analysis**: Explore data across 7 different dimensions
  - Overall distribution analysis
  - Gender-based comparisons
  - Age group analysis (with granularity control)
  - Education level comparisons
  - Household income analysis
  - Geographic distribution (interactive U.S. map)
  - Temporal trends (2011-2023)

- **Advanced Filtering**
  - Hierarchical question selection (Class → Topic → Question)
  - Response option selector for geographic analysis
  - Age granularity toggle (7 groups vs 3 groups)

- **Enhanced Visualizations**
  - Confidence intervals displayed on all charts
  - Interactive hover tooltips with detailed statistics
  - Professional color schemes optimized for data ranges
  - Responsive design for various screen sizes

### 📊 Data Quality & Processing

- **Automated Data Cleaning Pipeline**
  - 7-step cleaning process (Step0-Step6)
  - Handles historical data inconsistencies
  - Merges duplicate QuestionIDs, ResponseIDs, and BreakoutIDs
  - Normalizes text fields and handles missing values

- **Quality Filters**
  - Minimum sample size threshold (≥30 for statistical reliability)
  - Confidence interval validation
  - Data consistency checks
  - Geographic data validation

- **Statistical Accuracy**
  - Proper aggregation with sample size weighting
  - 95% confidence interval recalculation
  - Binomial distribution approximation

### 🗺️ Geographic Visualization

- **Interactive U.S. Map**
  - Choropleth visualization with intelligent color mapping
  - Response selector for different survey responses
  - Statistical summary panel (mean, median, min, max, std dev)
  - Enhanced hover information with confidence intervals

- **Smart Color Scaling**
  - Automatic color scheme selection based on data range
  - Perceptually uniform color spaces (Viridis, Plasma, Cividis)
  - Full data range utilization

---

## 🛠️ Technology Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.8+ | Core programming language |
| **Pandas** | 2.0+ | Data manipulation and analysis |
| **NumPy** | 1.24+ | Numerical computations |
| **PyArrow** | 12.0+ | Parquet file handling |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Dash** | 2.14+ | Web application framework |
| **Plotly** | 5.17+ | Interactive visualizations |
| **Plotly Express** | 5.17+ | High-level chart creation |
| **HTML/CSS** | - | UI styling and layout |

### Data Processing

| Component | Purpose |
|-----------|---------|
| **Data Cleaning Pipeline** | 7-step automated cleaning process |
| **Parquet Format** | Efficient data storage and retrieval |
| **Quality Validation** | Automated data quality checks |

### Development Tools

| Tool | Purpose |
|------|---------|
| **Git** | Version control |
| **VS Code / PyCharm** | IDE recommendations |
| **Jupyter Notebook** | Data exploration (optional) |

---

## 📁 Project Structure

```
BRFSS-Dashboard/
│
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── setup.py                 # Package setup (optional)
│
├── src/                     # Source code
│   ├── dashboard_app.py    # Main dashboard application
│   ├── data_cleaning/      # Data cleaning pipeline
│   │   ├── step0_preprocessing.py
│   │   ├── step1_question_merge.py
│   │   ├── step2_response_merge.py
│   │   ├── step3_breakout_merge.py
│   │   ├── step4_numeric_clean.py
│   │   ├── step5_aggregation.py
│   │   └── step6_quality_enhancement.py
│   └── utils/              # Utility functions
│       └── data_loader.py
│
├── data/                    # Data files
│   ├── raw/                # Raw data (not in repo)
│   │   └── dataset.csv
│   ├── processed/          # Processed data
│   │   ├── cleaned_data_final_enhanced.parquet
│   │   └── cleaned_data_final.parquet
│   └── reports/            # Quality reports
│       └── data_quality_report.txt
│
├── docs/                    # Documentation
│   ├── ARCHITECTURE.md     # System architecture
│   ├── DATA_PIPELINE.md    # Data processing pipeline
│   ├── API.md              # API documentation
│   └── DEPLOYMENT.md       # Deployment guide
│
├── scripts/                 # Utility scripts
│   ├── run_pipeline.py     # Run full cleaning pipeline
│   └── validate_data.py    # Data validation script
│
└── tests/                   # Unit tests (optional)
    └── test_data_cleaning.py
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 8GB+ RAM recommended for data processing
- Modern web browser (Chrome, Firefox, Edge)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd BRFSS-Dashboard
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download Data

1. Download BRFSS data from [CDC Data Portal](https://data.cdc.gov/Behavioral-Risk-Factors/Behavioral-Risk-Factor-Surveillance-System-BRFSS-P/dttw-5yxu)
2. Place `dataset.csv` in `data/raw/` directory

### Step 5: Run Data Cleaning Pipeline

```bash
python scripts/run_pipeline.py
```

This will generate `data/processed/cleaned_data_final_enhanced.parquet`

---

## 💻 Usage

### Starting the Dashboard

```bash
python src/dashboard_app.py
```

The dashboard will be available at: `http://127.0.0.1:8050`

### Using the Dashboard

1. **Select a Question**
   - Choose a Class (e.g., "Health Status")
   - Select a Topic (e.g., "General Health")
   - Pick a Question (e.g., "Would you say that in general your health is...")

2. **Explore Visualizations**
   - **Overall Panel**: View distribution across all responses
   - **Gender Panel**: Compare by sex
   - **Age Panel**: Analyze by age groups (toggle granularity)
   - **Education Panel**: Compare by education level
   - **Income Panel**: Analyze by household income
   - **Geographic Panel**: View U.S. map (select response to display)
   - **Temporal Panel**: See trends over time (2011-2023)

3. **Interact with Charts**
   - Hover over bars/points for detailed information
   - Use Plotly's built-in zoom and pan features
   - Click legend items to show/hide series

### Command Line Options

```bash
# Run with custom port
python src/dashboard_app.py --port 8080

# Run with debug mode
python src/dashboard_app.py --debug
```

---

## 🔄 Data Pipeline

### Overview

The data cleaning pipeline consists of 7 sequential steps, each handling specific data quality issues:

```
Raw Data (dataset.csv)
    ↓
Step 0: Preprocessing
    ↓
Step 1: QuestionID Merging
    ↓
Step 2: ResponseID Merging
    ↓
Step 3: BreakoutID Merging
    ↓
Step 4: Numeric Cleaning
    ↓
Step 5: Aggregation
    ↓
Step 6: Quality Enhancement
    ↓
Final Data (cleaned_data_final_enhanced.parquet)
```

### Step Details

#### Step 0: Preprocessing
- Text normalization (Class, Topic, Question)
- Response text standardization
- Special character handling
- Encoding issue resolution

#### Step 1: QuestionID Merging
- Merges duplicate QuestionIDs for identical questions
- Selects shortest QuestionID as canonical
- Preserves original QuestionID for reference

#### Step 2: ResponseID Merging
- Handles historical response changes
- Merges variants (e.g., "Emplyd" → "Employed")
- Consolidates income brackets
- Unifies race/ethnicity categories

#### Step 3: BreakoutID Merging
- Normalizes age groups (7 categories)
- Consolidates income brackets (5 categories)
- Unifies education levels
- Standardizes race/ethnicity categories

#### Step 4: Numeric Cleaning
- Type conversion and validation
- Filters invalid samples (Sample_Size ≤ 0)
- Validates percentage ranges (0-100%)
- Generates proportion and persons columns

#### Step 5: Aggregation
- Aggregates duplicate rows
- Recalculates confidence intervals
- Uses binomial distribution approximation
- Maintains statistical accuracy

#### Step 6: Quality Enhancement
- Missing value handling
- Data consistency validation
- Geographic data validation
- Year range verification
- Statistical anomaly detection
- Generates quality report

### Running the Pipeline

```bash
# Run all steps sequentially
python scripts/run_pipeline.py

# Run individual steps
python src/data_cleaning/step0_preprocessing.py
python src/data_cleaning/step1_question_merge.py
# ... etc
```

---

## 🏗️ Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│              (Web Browser - Dash Frontend)              │
└────────────────────┬────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              Dash Application Server                     │
│  ┌──────────────────────────────────────────────────┐   │
│  │         Dashboard App (dashboard_app.py)         │   │
│  │  - Callbacks for interactivity                    │   │
│  │  - Chart generation functions                    │   │
│  │  - Data aggregation logic                        │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              Data Layer                                  │
│  ┌──────────────────────────────────────────────────┐   │
│  │     Parquet Data Files (Enhanced/Cleaned)        │   │
│  │  - cleaned_data_final_enhanced.parquet           │   │
│  │  - Fast columnar storage                         │   │
│  │  - Efficient querying                            │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Component Architecture

#### Frontend Components

1. **Header Component**
   - Title and description
   - Data source indicator
   - Quality filter status

2. **Filter Card**
   - Class/Topic/Question dropdowns
   - Age granularity toggle
   - Question information panel

3. **Visualization Cards** (7 panels)
   - Overall analysis chart
   - Gender comparison chart
   - Age analysis chart
   - Education comparison chart
   - Income analysis chart
   - Geographic map
   - Temporal trend chart

#### Backend Components

1. **Data Loader**
   - Automatic dataset detection
   - Quality filtering
   - Type validation

2. **Aggregation Engine**
   - Group-by operations
   - Confidence interval calculation
   - Statistical computations

3. **Chart Generators**
   - Bar charts with CI
   - Grouped bar charts
   - Choropleth maps
   - Temporal line charts

### Data Flow

```
User Selection (Class/Topic/Question)
    ↓
Filter Dataset
    ↓
Aggregate by Dimension
    ↓
Calculate Statistics
    ↓
Generate Visualizations
    ↓
Render in Browser
```

---

## 📚 API Documentation

### Dashboard Callbacks

#### `update_topic_dropdown(class_value)`
Updates topic dropdown based on selected class.

**Inputs:**
- `class-dropdown.value`: Selected class

**Outputs:**
- `topic-dropdown.options`: Available topics
- `topic-dropdown.value`: Default topic

#### `update_question_dropdown(class_value, topic_value)`
Updates question dropdown based on selected class and topic.

**Inputs:**
- `class-dropdown.value`: Selected class
- `topic-dropdown.value`: Selected topic

**Outputs:**
- `question-dropdown.options`: Available questions
- `question-dropdown.value`: Default question

#### `update_map_response_dropdown(class_value, topic_value, question_value)`
Updates response dropdown for geographic map.

**Inputs:**
- `class-dropdown.value`: Selected class
- `topic-dropdown.value`: Selected topic
- `question-dropdown.value`: Selected question

**Outputs:**
- `map-response-dropdown.options`: Available responses
- `map-response-dropdown.value`: Default response

#### `update_all_panels(class_value, topic_value, question_value, age_mode, map_response)`
Main callback that updates all visualization panels.

**Inputs:**
- `class-dropdown.value`: Selected class
- `topic-dropdown.value`: Selected topic
- `question-dropdown.value`: Selected question
- `age-mode-radio.value`: Age granularity ("more" or "less")
- `map-response-dropdown.value`: Selected response for map

**Outputs:**
- `overall-graph.figure`: Overall analysis chart
- `gender-graph.figure`: Gender comparison chart
- `age-graph.figure`: Age analysis chart
- `education-graph.figure`: Education comparison chart
- `income-graph.figure`: Income analysis chart
- `location-graph.figure`: Geographic map
- `year-graph.figure`: Temporal trend chart
- `map-stats-panel.children`: Geographic statistics panel

### Core Functions

#### `aggregate_groups(sub_df, group_cols)`
Aggregates data by specified columns and recalculates confidence intervals.

**Parameters:**
- `sub_df`: DataFrame subset
- `group_cols`: List of columns to group by

**Returns:**
- DataFrame with aggregated statistics

#### `make_location_map(df_q, selected_response=None)`
Creates enhanced geographic visualization.

**Parameters:**
- `df_q`: Filtered DataFrame for selected question
- `selected_response`: Response to display (optional)

**Returns:**
- `(figure, responses, stats)`: Plotly figure, available responses, statistics

---

## 🧪 Development

### Development Workflow (SDE Best Practices)

#### 1. Environment Setup

```bash
# Clone repository
git clone <repository-url>
cd BRFSS-Dashboard

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development tools (optional)
pip install black flake8 mypy pytest
```

#### 2. Code Style & Standards

**Python Style Guide (PEP 8)**:
- Maximum line length: 100 characters
- Use 4 spaces for indentation
- Use descriptive variable names
- Add type hints for function parameters and returns

**Code Formatting**:
```bash
# Format code with Black
black src/

# Check style with flake8
flake8 src/ --max-line-length=100

# Type checking with mypy
mypy src/
```

**Documentation Standards**:
- All functions must have docstrings
- Use Google-style docstrings
- Document complex algorithms
- Include examples in docstrings

#### 3. Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: add new feature description"

# Push and create PR
git push origin feature/your-feature-name
```

**Commit Message Convention**:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

#### 4. Testing Strategy

**Unit Tests**:
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/ --cov-report=html

# Run specific test file
pytest tests/test_data_cleaning.py
```

**Test Structure**:
```
tests/
├── test_data_cleaning.py
├── test_dashboard.py
└── test_utils.py
```

**Integration Tests**:
- Test data pipeline end-to-end
- Test dashboard callbacks
- Test data loading and filtering

#### 5. Code Review Process

1. **Self-Review**: Review your own code before submitting PR
2. **Peer Review**: At least one reviewer required
3. **Automated Checks**: CI/CD runs linting and tests
4. **Documentation**: Update docs for user-facing changes

#### 6. Debugging

**Local Debugging**:
```python
# Enable debug mode
app.run(debug=True, host='127.0.0.1', port=8050)
```

**Debugging Tools**:
- Use Python debugger (pdb)
- Use IDE breakpoints
- Check browser console for frontend issues
- Review server logs

#### 7. Performance Profiling

```python
# Profile data loading
import cProfile
cProfile.run('load_data()')

# Memory profiling
from memory_profiler import profile
@profile
def your_function():
    ...
```

#### 8. Continuous Integration

**GitHub Actions** (example):
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest tests/
      - run: flake8 src/
```

### Development Best Practices

1. **Modular Design**: Keep functions focused and reusable
2. **Error Handling**: Use try-except blocks appropriately
3. **Logging**: Use Python logging module for debugging
4. **Configuration**: Use environment variables for settings
5. **Documentation**: Keep code and docs in sync
6. **Version Control**: Commit frequently with clear messages
7. **Code Review**: Always review before merging
8. **Testing**: Write tests for new features

---

## 📊 Data Quality

### Quality Metrics

- **Completeness**: 99.76% (only 0.24% missing confidence intervals)
- **Validity**: All records pass range checks
- **Consistency**: Automated validation of relationships
- **Reliability**: Minimum sample size ≥ 30

### Quality Report

After running Step 6, check `data/reports/data_quality_report.txt` for:
- Missing value statistics
- Numeric field distributions
- Categorical field unique counts
- Year distribution
- Data quality metrics

---

## 🚢 Deployment

### Local Deployment

```bash
python src/dashboard_app.py
```

### Production Deployment

#### Option 1: Using Gunicorn

```bash
pip install gunicorn
gunicorn dashboard_app:server
```

#### Option 2: Using Docker

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

#### Option 3: Deploy to Heroku/Railway/Render

1. Create `Procfile`:
```
web: python src/dashboard_app.py
```

2. Deploy using platform CLI

---

## 🤝 Contributing

### Contribution Guidelines

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Review Process

- All code must pass linting checks
- Tests must be added for new features
- Documentation must be updated
- Code must follow project style guide

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **CDC** for providing the BRFSS dataset
- **Plotly** for excellent visualization libraries
- **Dash** team for the web framework
- **Pandas** community for data processing tools

---

## 👥 Team & Roles

### Software Development Engineer (SDE) Workflow

This project follows industry-standard SDE practices:

#### Frontend Development
- **Framework**: Dash (Python-based, no separate frontend build)
- **Components**: Dash HTML Components, Dash Core Components
- **Styling**: Inline CSS with modern design system
- **Interactivity**: Dash callbacks for real-time updates

#### Backend Development
- **Language**: Python 3.8+
- **Data Processing**: Pandas, NumPy
- **API**: Dash server (no REST API needed)
- **Data Storage**: Parquet files (columnar format)

#### Data Engineering
- **Pipeline**: 7-step ETL process
- **Quality**: Automated validation and filtering
- **Format**: Parquet for efficient storage
- **Monitoring**: Quality reports and logs

#### DevOps
- **Deployment**: Gunicorn, Docker, or cloud platforms
- **CI/CD**: GitHub Actions (recommended)
- **Monitoring**: Application logs and error tracking
- **Scaling**: Horizontal scaling with load balancer

### Development Roles

| Role | Responsibilities | Key Files |
|------|-----------------|-----------|
| **Frontend Developer** | UI/UX, Dash components, styling | `src/dashboard_app.py` |
| **Backend Developer** | Data processing, callbacks, logic | `src/dashboard_app.py`, `src/data_cleaning/` |
| **Data Engineer** | Pipeline, quality, ETL | `src/data_cleaning/*.py` |
| **DevOps Engineer** | Deployment, CI/CD, infrastructure | `docs/DEPLOYMENT.md`, `.github/workflows/` |
| **QA Engineer** | Testing, validation, quality assurance | `tests/`, `data_quality_report.txt` |

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Email**: xing.kem@northeastern.edu
- **Documentation**: [Full Documentation](docs/)
- **Quick Start**: See [QUICKSTART.md](QUICKSTART.md)

---

## 📈 Future Enhancements

- [ ] Add data export functionality (CSV, Excel, PDF)
- [ ] Implement user authentication
- [ ] Add comparison mode (compare two questions)
- [ ] Create API endpoints for data access
- [ ] Add machine learning predictions
- [ ] Implement caching for better performance
- [ ] Add unit tests and integration tests
- [ ] Create Docker containerization
- [ ] Add CI/CD pipeline

---

<div align="center">

**Built with ❤️ for Public Health Research**

[Back to Top](#brfss-dashboard---behavioral-risk-factor-surveillance-system-data-explorer)

</div>


>>>>>>> f6026c6a98956f5ab275bc713b219b172fc0f751
