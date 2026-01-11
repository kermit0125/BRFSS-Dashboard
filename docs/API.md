# API Documentation

## Dashboard Callbacks

### Callback: `update_topic_dropdown`

Updates topic dropdown options based on selected class.

**Signature:**
```python
@app.callback(
    Output("topic-dropdown", "options"),
    Output("topic-dropdown", "value"),
    Input("class-dropdown", "value"),
)
def update_topic_dropdown(selected_class: str) -> tuple[list, str]:
```

**Parameters:**
- `selected_class` (str): Selected class value

**Returns:**
- `options` (list): List of topic options
- `value` (str): Default topic value

---

### Callback: `update_question_dropdown`

Updates question dropdown based on selected class and topic.

**Signature:**
```python
@app.callback(
    Output("question-dropdown", "options"),
    Output("question-dropdown", "value"),
    Input("class-dropdown", "value"),
    Input("topic-dropdown", "value"),
)
def update_question_dropdown(selected_class: str, selected_topic: str) -> tuple[list, str]:
```

**Parameters:**
- `selected_class` (str): Selected class value
- `selected_topic` (str): Selected topic value

**Returns:**
- `options` (list): List of question options
- `value` (str): Default question value

---

### Callback: `update_map_response_dropdown`

Updates response dropdown for geographic map visualization.

**Signature:**
```python
@app.callback(
    Output("map-response-dropdown", "options"),
    Output("map-response-dropdown", "value"),
    Input("class-dropdown", "value"),
    Input("topic-dropdown", "value"),
    Input("question-dropdown", "value"),
)
def update_map_response_dropdown(sel_class: str, sel_topic: str, sel_question: str) -> tuple[list, str]:
```

**Parameters:**
- `sel_class` (str): Selected class
- `sel_topic` (str): Selected topic
- `sel_question` (str): Selected question

**Returns:**
- `options` (list): List of response options
- `value` (str): Default response value ("Yes" if available)

---

### Callback: `update_all_panels`

Main callback that updates all visualization panels.

**Signature:**
```python
@app.callback(
    Output("overall-graph", "figure"),
    Output("gender-graph", "figure"),
    Output("age-graph", "figure"),
    Output("education-graph", "figure"),
    Output("income-graph", "figure"),
    Output("location-graph", "figure"),
    Output("year-graph", "figure"),
    Output("map-stats-panel", "children"),
    Input("class-dropdown", "value"),
    Input("topic-dropdown", "value"),
    Input("question-dropdown", "value"),
    Input("age-mode-radio", "value"),
    Input("map-response-dropdown", "value"),
)
def update_all_panels(
    sel_class: str,
    sel_topic: str,
    sel_question: str,
    age_mode: str,
    map_response: str
) -> tuple:
```

**Parameters:**
- `sel_class` (str): Selected class
- `sel_topic` (str): Selected topic
- `sel_question` (str): Selected question
- `age_mode` (str): Age granularity ("more" or "less")
- `map_response` (str): Selected response for map

**Returns:**
- Tuple of 8 outputs:
  1. Overall graph figure
  2. Gender graph figure
  3. Age graph figure
  4. Education graph figure
  5. Income graph figure
  6. Location map figure
  7. Year graph figure
  8. Map statistics panel HTML

---

## Core Functions

### `aggregate_groups(sub_df: pd.DataFrame, group_cols: list) -> pd.DataFrame`

Aggregates data by specified columns and recalculates confidence intervals.

**Parameters:**
- `sub_df` (pd.DataFrame): Subset of data to aggregate
- `group_cols` (list): List of column names to group by

**Returns:**
- `pd.DataFrame`: Aggregated data with recalculated statistics

**Algorithm:**
1. Group by `group_cols`
2. Sum `Sample_Size` and `persons`
3. Calculate new `proportion`
4. Recompute standard error
5. Calculate 95% confidence intervals

---

### `make_location_map(df_q: pd.DataFrame, selected_response: str = None) -> tuple`

Creates enhanced geographic visualization.

**Parameters:**
- `df_q` (pd.DataFrame): Filtered DataFrame for selected question
- `selected_response` (str, optional): Response to display

**Returns:**
- `tuple`: (figure, responses, stats)
  - `figure`: Plotly choropleth figure
  - `responses`: List of available responses
  - `stats`: Dictionary of statistics

**Statistics Dictionary:**
```python
{
    'mean': float,
    'median': float,
    'min': float,
    'max': float,
    'std': float,
    'min_state': str,
    'max_state': str,
    'min_value': float,
    'max_value': float,
    'num_states': int,
}
```

---

## Data Structures

### DataFrame Schema

**Required Columns:**
- `Year`: int (2011-2023)
- `Locationabbr`: str (state code)
- `Class`: str
- `Topic`: str
- `Question`: str
- `Response`: str
- `Break_Out`: str
- `Break_Out_Category`: str
- `Sample_Size`: float
- `Data_value`: float (0-100)
- `Confidence_limit_Low`: float (0-100)
- `Confidence_limit_High`: float (0-100)
- `proportion`: float (0-1)
- `persons`: float

**Optional Columns:**
- `ClassId`: str
- `TopicId`: str
- `QuestionID`: str
- `ResponseID`: str
- `BreakoutID`: str
- `BreakOutCategoryID`: str
- `GeoLocation`: str
- `QuestionID_original`: str

---

## Error Handling

### Common Exceptions

1. **ValueError**: Missing required columns
2. **FileNotFoundError**: Data file not found
3. **KeyError**: Missing dictionary key
4. **TypeError**: Incorrect data types

### Error Recovery

- Missing data: Returns empty figure with message
- Invalid selection: Falls back to default values
- Data quality issues: Logs warning and continues

