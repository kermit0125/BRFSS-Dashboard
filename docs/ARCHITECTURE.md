# System Architecture

## Overview

The BRFSS Dashboard is built using a modern web application architecture with a Python backend and interactive frontend powered by Dash and Plotly.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Layer                              │
│              (Web Browser - User Interface)                  │
└────────────────────┬────────────────────────────────────────┘
                      │ HTTP/WebSocket
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Application Server Layer                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Dash Application (dashboard_app.py)            │  │
│  │  • Request Routing                                    │  │
│  │  • Callback Management                                │  │
│  │  • State Management                                    │  │
│  └────────────────────┬──────────────────────────────────┘  │
│                       │                                      │
│  ┌────────────────────▼──────────────────────────────────┐  │
│  │         Business Logic Layer                           │  │
│  │  • Data Aggregation Functions                         │  │
│  │  • Chart Generation Functions                         │  │
│  │  • Statistical Calculations                           │  │
│  └────────────────────┬──────────────────────────────────┘  │
└───────────────────────┼──────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  Data Access Layer                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Data Loader                                  │  │
│  │  • Parquet File Reader                               │  │
│  │  • Quality Filtering                                 │  │
│  │  • Type Validation                                   │  │
│  └────────────────────┬──────────────────────────────────┘  │
└───────────────────────┼──────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  Data Storage Layer                          │
│  • cleaned_data_final_enhanced.parquet                      │
│  • Columnar Storage (Fast Queries)                          │
│  • Compressed Format                                        │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend Components

#### 1. Layout Components
- **Header**: Title, description, data source indicator
- **Filter Card**: Question selection dropdowns, age granularity toggle
- **Visualization Cards**: 7 analysis panels

#### 2. Interactive Components
- **Dropdowns**: Class, Topic, Question, Response selectors
- **Radio Items**: Age granularity toggle
- **Graphs**: Plotly interactive charts

### Backend Components

#### 1. Data Processing
- **Data Loader**: Loads and validates parquet files
- **Quality Filter**: Applies data quality filters
- **Aggregator**: Performs statistical aggregations

#### 2. Visualization Engine
- **Chart Generators**: Create various chart types
- **Map Generator**: Creates geographic visualizations
- **Statistics Calculator**: Computes summary statistics

## Data Flow

### Request Flow

```
User Action (Select Question)
    ↓
Dash Callback Triggered
    ↓
Filter Dataset by Selection
    ↓
Aggregate by Dimension
    ↓
Calculate Statistics
    ↓
Generate Visualizations
    ↓
Return HTML/JSON to Browser
    ↓
Render in Browser
```

### Data Processing Flow

```
Raw Data (CSV)
    ↓
Step 0: Preprocessing
    ↓
Step 1: QuestionID Merge
    ↓
Step 2: ResponseID Merge
    ↓
Step 3: BreakoutID Merge
    ↓
Step 4: Numeric Cleaning
    ↓
Step 5: Aggregation
    ↓
Step 6: Quality Enhancement
    ↓
Final Parquet File
```

## Technology Stack

### Backend
- **Python 3.8+**: Core language
- **Pandas**: Data manipulation
- **NumPy**: Numerical computations
- **Dash**: Web framework

### Frontend
- **Dash Components**: UI components
- **Plotly**: Interactive visualizations
- **HTML/CSS**: Styling

### Data Storage
- **Parquet**: Columnar storage format
- **PyArrow**: Parquet I/O

## Performance Considerations

1. **Data Loading**: Parquet format enables fast columnar reads
2. **Caching**: Dash callbacks can be cached for better performance
3. **Lazy Loading**: Data loaded only when needed
4. **Efficient Aggregation**: Uses Pandas groupby operations

## Scalability

- **Horizontal Scaling**: Can deploy multiple instances behind load balancer
- **Data Partitioning**: Can partition by year or state for larger datasets
- **Caching Layer**: Can add Redis for caching frequent queries

