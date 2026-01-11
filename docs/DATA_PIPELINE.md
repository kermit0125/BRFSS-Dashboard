# Data Pipeline Documentation

## Overview

The BRFSS data cleaning pipeline consists of 7 sequential steps that transform raw survey data into a clean, analysis-ready dataset.

## Pipeline Steps

### Step 0: Preprocessing
**Purpose**: Initial data cleaning and text normalization

**Operations**:
- Text normalization (Class, Topic, Question)
- Response text standardization
- Special character handling
- Encoding issue resolution

**Input**: `dataset.csv`
**Output**: `dataset_preprocessed.csv`

### Step 1: QuestionID Merging
**Purpose**: Merge duplicate QuestionIDs for identical questions

**Operations**:
- Identify questions with same text but different IDs
- Select shortest QuestionID as canonical
- Preserve original QuestionID for reference

**Input**: `dataset_preprocessed.csv`
**Output**: `cleaned_data_question_merged.csv`

### Step 2: ResponseID Merging
**Purpose**: Handle historical response changes and merge variants

**Operations**:
- Merge employment variants ("Emplyd" → "Employed")
- Consolidate income brackets
- Unify race/ethnicity categories

**Input**: `cleaned_data_question_merged.csv`
**Output**: `cleaned_data_response_merged.csv`

### Step 3: BreakoutID Merging
**Purpose**: Normalize demographic breakout categories

**Operations**:
- Normalize age groups (7 categories)
- Consolidate income brackets (5 categories)
- Unify education levels
- Standardize race/ethnicity

**Input**: `cleaned_data_response_merged.csv`
**Output**: `cleaned_data_breakout_merged.csv`

### Step 4: Numeric Cleaning
**Purpose**: Validate and clean numeric fields

**Operations**:
- Type conversion and validation
- Filter invalid samples (Sample_Size ≤ 0)
- Validate percentage ranges (0-100%)
- Generate proportion and persons columns

**Input**: `cleaned_data_breakout_merged.csv`
**Output**: `cleaned_data_final.csv`

### Step 5: Aggregation
**Purpose**: Aggregate duplicate rows and recalculate statistics

**Operations**:
- Group by unique combinations
- Sum sample sizes and persons
- Recalculate proportions
- Recompute 95% confidence intervals

**Input**: `cleaned_data_final.csv`
**Output**: `cleaned_data_final.parquet`

### Step 6: Quality Enhancement
**Purpose**: Final quality checks and validation

**Operations**:
- Missing value handling
- Data consistency validation
- Geographic data validation
- Statistical anomaly detection
- Generate quality report

**Input**: `cleaned_data_final.csv`
**Output**: `cleaned_data_final_enhanced.parquet`, `data_quality_report.txt`

## Running the Pipeline

### Full Pipeline
```bash
python scripts/run_pipeline.py
```

### Individual Steps
```bash
python src/data_cleaning/step0_preprocessing.py
python src/data_cleaning/step1_question_merge.py
# ... etc
```

## Data Quality Metrics

After Step 6, check the quality report for:
- Missing value statistics
- Numeric field distributions
- Categorical field counts
- Year distribution
- Quality metrics

