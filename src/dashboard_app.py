# =========================
# BRFSS Dashboard - Enhanced UI Version with Quality Filters
# Modern, interactive dashboard for exploring BRFSS data
# Uses cleaned_data_final_enhanced.parquet with quality filters
# =========================
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os

# =========================
# 1. Data loading and validation
# =========================
# 使用增强版数据（自动检测）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

# 优先使用增强版数据
enhanced_path = os.path.join(PROJECT_DIR, "cleaned_data_final_enhanced.parquet")
standard_path = os.path.join(PROJECT_DIR, "cleaned_data_final.parquet")

if os.path.exists(enhanced_path):
    DATA_PATH = enhanced_path
    print(f"📥 Loading enhanced dataset from: {DATA_PATH}")
else:
    DATA_PATH = standard_path
    print(f"📥 Loading standard dataset from: {DATA_PATH}")

df = pd.read_parquet(DATA_PATH)
print("Data loaded! Shape:", df.shape)

# =========================
# 2. Data quality filters based on quality report
# =========================
print("\n🔍 Applying data quality filters...")

# 2.1 过滤缺失置信区间的数据（0.24%的数据）
before_filter = len(df)
df = df.dropna(subset=["Confidence_limit_Low", "Confidence_limit_High"])
print(f"  ✅ Removed {before_filter - len(df)} rows with missing confidence intervals")

# 2.2 过滤样本量过小的数据（根据质量报告，最小样本量是1，但建议至少30）
MIN_SAMPLE_SIZE = 30  # 统计上更可靠的最小样本量
before_filter = len(df)
df = df[df["Sample_Size"] >= MIN_SAMPLE_SIZE].copy()
print(f"  ✅ Removed {before_filter - len(df)} rows with sample size < {MIN_SAMPLE_SIZE}")

# 2.3 确保数值列类型正确
for col in ["Sample_Size", "Data_value",
            "Confidence_limit_Low", "Confidence_limit_High",
            "proportion", "persons"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 2.4 验证数据完整性
required_cols = [
    "Year", "Locationabbr", "Class", "Topic", "Question", "Response",
    "Break_Out", "Break_Out_Category",
    "Sample_Size", "Data_value",
    "Confidence_limit_Low", "Confidence_limit_High",
    "proportion", "persons",
]
missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    raise ValueError(f"Dataset missing required columns: {missing_cols}")

print(f"  ✅ Final dataset shape: {df.shape}")
print(f"  ✅ Data quality: {len(df):,} high-quality records")

# =========================
# 3. Constants and configuration
# =========================
BREAKOUT_OVERALL = "Overall"
BREAKOUT_GENDER = "Sex"
BREAKOUT_AGE = "Age Group"
BREAKOUT_EDU = "Education Attained"
BREAKOUT_INC = "Household Income"
Z = 1.96

# Enhanced color scheme - modern, accessible palette
COLORS = {
    'primary': '#2563eb',      # Blue
    'secondary': '#7c3aed',    # Purple
    'success': '#10b981',     # Green
    'warning': '#f59e0b',     # Amber
    'danger': '#ef4444',      # Red
    'info': '#06b6d4',        # Cyan
    'dark': '#1e293b',        # Slate
    'light': '#f8fafc',       # Light gray
    'border': '#e2e8f0',      # Border gray
    'text': '#334155',        # Text gray
    'text-light': '#64748b',  # Light text
    'bg': '#ffffff',          # White background
    'bg-alt': '#f1f5f9',      # Alternate background
}

# Chart color palette - more vibrant and accessible
CHART_COLORS = [
    '#3b82f6',  # Blue
    '#8b5cf6',  # Purple
    '#10b981',  # Green
    '#f59e0b',  # Amber
    '#ef4444',  # Red
    '#06b6d4',  # Cyan
    '#ec4899',  # Pink
    '#84cc16',  # Lime
]

# Extended palette for more categories
CHART_COLORS_EXTENDED = CHART_COLORS + [
    '#6366f1', '#14b8a6', '#f97316', '#a855f7',
    '#22c55e', '#eab308', '#06b6d4', '#f43f5e',
]

# =========================
# 4. Helper functions for data aggregation
# =========================
def aggregate_groups(sub_df: pd.DataFrame, group_cols):
    """Aggregate groups and recompute confidence intervals"""
    if sub_df.empty:
        return pd.DataFrame(columns=list(group_cols) + [
            "Sample_Size", "persons",
            "proportion", "Data_value",
            "Confidence_limit_Low", "Confidence_limit_High",
        ])

    g = (
        sub_df.groupby(list(group_cols), as_index=False)
        .agg(
            Sample_Size=("Sample_Size", "sum"),
            persons=("persons", "sum"),
        )
    )

    g["proportion"] = g["persons"] / g["Sample_Size"]
    g.loc[g["Sample_Size"] <= 0, "proportion"] = np.nan

    se = np.sqrt(g["proportion"] * (1 - g["proportion"]) / g["Sample_Size"])
    g["Data_value"] = g["proportion"] * 100.0
    g["Confidence_limit_Low"] = (g["proportion"] - Z * se) * 100.0
    g["Confidence_limit_High"] = (g["proportion"] + Z * se) * 100.0

    g["Confidence_limit_Low"] = g["Confidence_limit_Low"].clip(0, 100)
    g["Confidence_limit_High"] = g["Confidence_limit_High"].clip(0, 100)

    return g

# =========================
# 5. Enhanced chart creation functions
# =========================
def make_bar_with_ci(df_panel, x_col, title, subtitle="", color=None):
    """Create a bar chart with confidence intervals"""
    if df_panel.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for this selection",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=COLORS['text-light'])
        )
        fig.update_layout(
            title=dict(text=title, font=dict(size=18, color=COLORS['dark'])),
            xaxis_title=x_col,
            yaxis_title="Percent (%)",
            template="plotly_white",
            height=400,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Inter, sans-serif", color=COLORS['text']),
        )
        return fig

    x = df_panel[x_col].astype(str)
    y = df_panel["Data_value"]
    err_plus = df_panel["Confidence_limit_High"] - df_panel["Data_value"]
    err_minus = df_panel["Data_value"] - df_panel["Confidence_limit_Low"]

    bar_color = color if color else COLORS['primary']

    fig = go.Figure(
        data=[
            go.Bar(
                x=x,
                y=y,
                marker=dict(
                    color=bar_color,
                    line=dict(color=bar_color, width=1),
                ),
                error_y=dict(
                    type="data",
                    array=err_plus,
                    arrayminus=err_minus,
                    visible=True,
                    thickness=2,
                    color=COLORS['text-light'],
                ),
                hovertemplate="<b>%{x}</b><br>" +
                             "Value: %{y:.2f}%<br>" +
                             "95% CI: [%{customdata[0]:.2f}, %{customdata[1]:.2f}]%<br>" +
                             "Sample Size: %{customdata[2]:.0f}<br>" +
                             "<extra></extra>",
                customdata=np.column_stack([
                    df_panel["Confidence_limit_Low"],
                    df_panel["Confidence_limit_High"],
                    df_panel["Sample_Size"]
                ]),
            )
        ]
    )
    
    title_text = title
    if subtitle:
        title_text = f"{title}<br><sub style='font-size:0.7em;color:{COLORS['text-light']}'>{subtitle}</sub>"
    
    fig.update_layout(
        title=dict(text=title_text, font=dict(size=18, color=COLORS['dark'])),
        xaxis_title=x_col,
        yaxis_title="Percent (%)",
        template="plotly_white",
        height=420,
        margin=dict(l=50, r=20, t=80, b=50),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Inter, sans-serif", color=COLORS['text'], size=12),
        xaxis=dict(
            showgrid=True,
            gridcolor=COLORS['border'],
            gridwidth=1,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=COLORS['border'],
            gridwidth=1,
            range=[0, max(100, y.max() * 1.1)],
        ),
    )
    return fig

def make_grouped_bar_with_ci(df_panel, x_col, color_col, title, subtitle=""):
    """Create a grouped bar chart with confidence intervals"""
    if df_panel.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for this selection",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=COLORS['text-light'])
        )
        fig.update_layout(
            title=dict(text=title, font=dict(size=18, color=COLORS['dark'])),
            xaxis_title=x_col,
            yaxis_title="Percent (%)",
            template="plotly_white",
            height=420,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Inter, sans-serif", color=COLORS['text']),
        )
        return fig

    df_panel = df_panel.copy()
    df_panel[x_col] = df_panel[x_col].astype(str)
    df_panel[color_col] = df_panel[color_col].astype(str)
    df_panel["err_plus"] = df_panel["Confidence_limit_High"] - df_panel["Data_value"]
    df_panel["err_minus"] = df_panel["Data_value"] - df_panel["Confidence_limit_Low"]

    # Use extended color palette for more categories
    unique_colors = df_panel[color_col].nunique()
    color_sequence = CHART_COLORS_EXTENDED[:unique_colors] if unique_colors > len(CHART_COLORS) else CHART_COLORS[:unique_colors]

    fig = px.bar(
        df_panel,
        x=x_col,
        y="Data_value",
        color=color_col,
        barmode="group",
        error_y="err_plus",
        error_y_minus="err_minus",
        labels={"Data_value": "Percent (%)"},
        color_discrete_sequence=color_sequence,
    )
    
    title_text = title
    if subtitle:
        title_text = f"{title}<br><sub style='font-size:0.7em;color:{COLORS['text-light']}'>{subtitle}</sub>"
    
    fig.update_layout(
        title=dict(text=title_text, font=dict(size=18, color=COLORS['dark'])),
        xaxis_title=x_col,
        yaxis_title="Percent (%)",
        template="plotly_white",
        height=420,
        margin=dict(l=50, r=20, t=80, b=50),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Inter, sans-serif", color=COLORS['text'], size=12),
        xaxis=dict(
            showgrid=True,
            gridcolor=COLORS['border'],
            gridwidth=1,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=COLORS['border'],
            gridwidth=1,
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11),
        ),
    )
    return fig

# =========================
# 6. Panel creation functions
# =========================
def make_overall_panel(df_q):
    sub = df_q[df_q["Break_Out_Category"] == BREAKOUT_OVERALL].copy()
    if sub.empty:
        return make_bar_with_ci(pd.DataFrame(), "Response", "Overall Analysis")
    
    agg = aggregate_groups(sub, ["Response"])
    agg = agg.sort_values("Response")
    return make_bar_with_ci(agg, "Response", "Overall Analysis", 
                           "Distribution across all responses", COLORS['primary'])

def make_gender_panel(df_q):
    sub = df_q[df_q["Break_Out_Category"] == BREAKOUT_GENDER].copy()
    if sub.empty:
        return make_grouped_bar_with_ci(pd.DataFrame(), "Response", "Break_Out",
                                        "Gender Analysis")
    
    agg = aggregate_groups(sub, ["Break_Out", "Response"])
    return make_grouped_bar_with_ci(agg, "Response", "Break_Out",
                                   "Gender Analysis", 
                                   "Comparison by sex")

def make_education_panel(df_q):
    sub = df_q[df_q["Break_Out_Category"] == BREAKOUT_EDU].copy()
    if sub.empty:
        return make_grouped_bar_with_ci(pd.DataFrame(), "Response", "Break_Out",
                                        "Education Analysis")
    
    agg = aggregate_groups(sub, ["Break_Out", "Response"])
    order = ["Less than H.S.", "H.S. or G.E.D.",
             "Some post-H.S.", "College graduate"]
    agg["Break_Out"] = pd.Categorical(agg["Break_Out"], ordered=True, categories=order)
    agg = agg.sort_values(["Break_Out", "Response"])
    return make_grouped_bar_with_ci(agg, "Response", "Break_Out",
                                   "Education Analysis",
                                   "Comparison by education level")

def make_income_panel(df_q):
    sub = df_q[df_q["Break_Out_Category"] == BREAKOUT_INC].copy()
    if sub.empty:
        return make_grouped_bar_with_ci(pd.DataFrame(), "Response", "Break_Out",
                                        "Income Analysis")
    
    agg = aggregate_groups(sub, ["Break_Out", "Response"])
    return make_grouped_bar_with_ci(agg, "Response", "Break_Out",
                                   "Income Analysis",
                                   "Comparison by household income")

def make_age_panel(df_q, mode="more"):
    sub = df_q[df_q["Break_Out_Category"] == BREAKOUT_AGE].copy()
    if sub.empty:
        return make_grouped_bar_with_ci(pd.DataFrame(), "Response", "Break_Out",
                                        "Age Analysis")
    
    if mode == "more":
        agg = aggregate_groups(sub, ["Break_Out", "Response"])
        age_order = [
            "18-24", "25-34", "35-44", "45-54",
            "55-64", "65-74", "75+",
        ]
        agg["Break_Out"] = pd.Categorical(
            agg["Break_Out"], ordered=True, categories=age_order
        )
        agg = agg.sort_values(["Break_Out", "Response"])
        return make_grouped_bar_with_ci(agg, "Response", "Break_Out",
                                        "Age Analysis",
                                        "Detailed age groups (7 categories)")
    else:
        mapping = {
            "18-24": "18-34",
            "25-34": "18-34",
            "35-44": "35-64",
            "45-54": "35-64",
            "55-64": "35-64",
            "65-74": "65+",
            "75+": "65+",
        }
        sub = sub[sub["Break_Out"].isin(mapping.keys())].copy()
        if sub.empty:
            return make_grouped_bar_with_ci(pd.DataFrame(), "Response", "Break_Out",
                                            "Age Analysis")
        
        sub["Age_Group_3"] = sub["Break_Out"].map(mapping)
        agg = aggregate_groups(sub, ["Age_Group_3", "Response"])
        agg = agg.rename(columns={"Age_Group_3": "Break_Out"})
        order = ["18-34", "35-64", "65+"]
        agg["Break_Out"] = pd.Categorical(
            agg["Break_Out"], ordered=True, categories=order
        )
        agg = agg.sort_values(["Break_Out", "Response"])
        return make_grouped_bar_with_ci(agg, "Response", "Break_Out",
                                       "Age Analysis",
                                       "Broad age groups (3 categories)")

def make_year_panel(df_q):
    sub = df_q[df_q["Break_Out_Category"] == BREAKOUT_OVERALL].copy()
    if sub.empty:
        return make_grouped_bar_with_ci(pd.DataFrame(), "Year", "Response",
                                        "Temporal Analysis")
    
    agg = aggregate_groups(sub, ["Year", "Response"])
    agg = agg.sort_values(["Year", "Response"])
    return make_grouped_bar_with_ci(agg, "Year", "Response",
                                   "Temporal Analysis",
                                   "Trends over time (2011-2023)")

def make_location_map(df_q, selected_response=None):
    """
    Create an enhanced geographic visualization with:
    - Better color mapping
    - Response selector
    - Statistical summary
    - Enhanced hover information
    - Sample size visualization
    """
    sub = df_q[df_q["Break_Out_Category"] == BREAKOUT_OVERALL].copy()
    
    if sub.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available for this selection",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=COLORS['text-light'])
        )
        fig.update_layout(
            title=dict(text="Geographic Analysis", font=dict(size=18, color=COLORS['dark'])),
            template="plotly_white",
            height=550,
            plot_bgcolor='white',
            paper_bgcolor='white',
        )
        return fig, None, None
    
    # Get available responses
    responses = sorted(sub["Response"].dropna().unique())
    
    # Select response (use provided or default to "Yes" or first available)
    if selected_response and selected_response in responses:
        target_resp = selected_response
    else:
        target_resp = "Yes" if "Yes" in responses else (responses[0] if responses else None)
    
    if not target_resp:
        fig = go.Figure()
        fig.add_annotation(
            text="No response options available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=COLORS['text-light'])
        )
        fig.update_layout(
            title=dict(text="Geographic Analysis", font=dict(size=18, color=COLORS['dark'])),
            template="plotly_white",
            height=550,
        )
        return fig, responses, None
    
    # Filter by selected response
    sub = sub[sub["Response"] == target_resp].copy()
    
    if sub.empty:
        fig = go.Figure()
        fig.add_annotation(
            text=f"No data available for response: {target_resp}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=COLORS['text-light'])
        )
        fig.update_layout(
            title=dict(text="Geographic Analysis", font=dict(size=18, color=COLORS['dark'])),
            template="plotly_white",
            height=550,
        )
        return fig, responses, None
    
    # Aggregate by location
    agg = aggregate_groups(sub, ["Locationabbr"])
    agg = agg.dropna(subset=["Locationabbr"])
    
    if agg.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No geographic data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=COLORS['text-light'])
        )
        fig.update_layout(
            title=dict(text="Geographic Analysis", font=dict(size=18, color=COLORS['dark'])),
            template="plotly_white",
            height=550,
        )
        return fig, responses, None
    
    # Calculate statistics for summary
    stats = {
        'mean': agg['Data_value'].mean(),
        'median': agg['Data_value'].median(),
        'min': agg['Data_value'].min(),
        'max': agg['Data_value'].max(),
        'std': agg['Data_value'].std(),
        'min_state': agg.loc[agg['Data_value'].idxmin(), 'Locationabbr'],
        'max_state': agg.loc[agg['Data_value'].idxmax(), 'Locationabbr'],
        'min_value': agg['Data_value'].min(),
        'max_value': agg['Data_value'].max(),
        'num_states': len(agg),
    }
    
    # Determine color scale based on data distribution
    # Use perceptually uniform color scales for better visualization
    if stats['max'] - stats['min'] < 15:
        # For small ranges, use Plasma for better differentiation
        color_scale = "Plasma"
    elif stats['max'] - stats['min'] < 30:
        # Medium range - use Viridis
        color_scale = "Viridis"
    else:
        # Large range - use Cividis for better contrast
        color_scale = "Cividis"
    
    # Create enhanced choropleth map
    fig = px.choropleth(
        agg,
        locations="Locationabbr",
        locationmode="USA-states",
        color="Data_value",
        scope="usa",
        color_continuous_scale=color_scale,
        range_color=[stats['min'], stats['max']],  # Use full data range
        hover_data={
            "Locationabbr": True,
            "Data_value": ":.2f",
            "Confidence_limit_Low": ":.2f",
            "Confidence_limit_High": ":.2f",
            "Sample_Size": ":.0f",
        },
        labels={"Data_value": f"{target_resp} (%)"},
        custom_data=["Locationabbr", "Data_value", "Confidence_limit_Low", 
                    "Confidence_limit_High", "Sample_Size"],
    )
    
    # Enhanced hover template with better formatting
    fig.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br>" +
                     f"{target_resp}: <b>%{{customdata[1]:.2f}}%</b><br>" +
                     "95% CI: [%{customdata[2]:.2f}, %{customdata[3]:.2f}]%<br>" +
                     "Sample Size: %{customdata[4]:,.0f}<br>" +
                     "<extra></extra>",
    )
    
    # Update layout with enhanced styling
    fig.update_layout(
        title=dict(
            text=f"Geographic Distribution: {target_resp}",
            font=dict(size=20, color=COLORS['dark'], family="Inter, sans-serif"),
            x=0.5,
            xanchor='center',
        ),
        height=550,
        margin=dict(l=0, r=0, t=80, b=20),
        font=dict(family="Inter, sans-serif", color=COLORS['text'], size=12),
        geo=dict(
            bgcolor='white',
            lakecolor='#e0f2fe',
            landcolor=COLORS['light'],
            showlakes=True,
            showland=True,
            showcoastlines=True,
            coastlinecolor=COLORS['border'],
            showocean=True,
            oceancolor='#f0f9ff',
            subunitcolor=COLORS['border'],
            subunitwidth=0.5,
            countrycolor=COLORS['border'],
            countrywidth=1,
            projection_type='albers usa',
        ),
        coloraxis_colorbar=dict(
            title=dict(text=f"{target_resp} (%)", font=dict(size=12, family="Inter, sans-serif")),
            thickness=18,
            len=0.65,
            x=1.02,
            xanchor="left",
            y=0.5,
            yanchor="middle",
            tickfont=dict(size=10, family="Inter, sans-serif"),
            tickformat=".1f",
        ),
    )
    
    return fig, responses, stats

# =========================
# 7. Default values
# =========================
default_class = sorted(df["Class"].dropna().unique())[0]
default_topic = (
    df[df["Class"] == default_class]["Topic"].dropna().sort_values().iloc[0]
)
default_question = (
    df[(df["Class"] == default_class) & (df["Topic"] == default_topic)]["Question"]
    .dropna()
    .sort_values()
    .iloc[0]
)

# =========================
# 8. App initialization
# =========================
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# =========================
# 9. Custom CSS styles
# =========================
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>BRFSS Dashboard - Data Explorer</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background-color: #f8fafc;
                color: #334155;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# =========================
# 10. Layout components
# =========================
def create_header():
    """Create the dashboard header"""
    return html.Div(
        [
            html.Div(
                [
                    html.H1(
                        "BRFSS Dashboard",
                        style={
                            "fontSize": "2.5rem",
                            "fontWeight": "700",
                            "color": COLORS['dark'],
                            "marginBottom": "0.5rem",
                        }
                    ),
                    html.P(
                        "Behavioral Risk Factor Surveillance System - Data Explorer",
                        style={
                            "fontSize": "1rem",
                            "color": COLORS['text-light'],
                            "marginBottom": "0",
                        }
                    ),
                ],
                style={"flex": "1"},
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Span("📊", style={"fontSize": "1.5rem", "marginRight": "0.5rem"}),
                            html.Div(
                                [
                                    html.Strong("Data Source", style={"display": "block", "fontSize": "0.875rem"}),
                                    html.Span("CDC BRFSS", style={"fontSize": "0.75rem", "color": COLORS['text-light']}),
                                ]
                            ),
                        ],
                        style={
                            "display": "flex",
                            "alignItems": "center",
                            "padding": "0.75rem 1rem",
                            "backgroundColor": "white",
                            "borderRadius": "8px",
                            "border": f"1px solid {COLORS['border']}",
                        }
                    ),
                    html.Div(
                        [
                            html.Span("✅", style={"fontSize": "1.5rem", "marginRight": "0.5rem"}),
                            html.Div(
                                [
                                    html.Strong("Quality Filtered", style={"display": "block", "fontSize": "0.875rem"}),
                                    html.Span(f"Min Sample: {MIN_SAMPLE_SIZE}", style={"fontSize": "0.75rem", "color": COLORS['text-light']}),
                                ]
                            ),
                        ],
                        style={
                            "display": "flex",
                            "alignItems": "center",
                            "padding": "0.75rem 1rem",
                            "backgroundColor": "white",
                            "borderRadius": "8px",
                            "border": f"1px solid {COLORS['border']}",
                        }
                    ),
                ],
                style={"display": "flex", "gap": "1rem"},
            ),
        ],
        style={
            "display": "flex",
            "justifyContent": "space-between",
            "alignItems": "center",
            "padding": "2rem",
            "backgroundColor": "white",
            "borderBottom": f"1px solid {COLORS['border']}",
            "marginBottom": "2rem",
        }
    )

def create_filter_card():
    """Create the filter control card"""
    return html.Div(
        [
            html.Div(
                [
                    html.H3(
                        "📋 Select Question",
                        style={
                            "fontSize": "1.25rem",
                            "fontWeight": "600",
                            "color": COLORS['dark'],
                            "marginBottom": "1.5rem",
                        }
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Label(
                                        "Class",
                                        style={
                                            "display": "block",
                                            "fontSize": "0.875rem",
                                            "fontWeight": "500",
                                            "color": COLORS['text'],
                                            "marginBottom": "0.5rem",
                                        }
                                    ),
                                    dcc.Dropdown(
                                        id="class-dropdown",
                                        options=[
                                            {"label": c, "value": c}
                                            for c in sorted(df["Class"].dropna().unique())
                                        ],
                                        value=default_class,
                                        clearable=False,
                                        style={
                                            "fontSize": "0.875rem",
                                        },
                                    ),
                                ],
                                style={"flex": "1", "marginRight": "1rem"},
                            ),
                            html.Div(
                                [
                                    html.Label(
                                        "Topic",
                                        style={
                                            "display": "block",
                                            "fontSize": "0.875rem",
                                            "fontWeight": "500",
                                            "color": COLORS['text'],
                                            "marginBottom": "0.5rem",
                                        }
                                    ),
                                    dcc.Dropdown(
                                        id="topic-dropdown",
                                        clearable=False,
                                        style={
                                            "fontSize": "0.875rem",
                                        },
                                    ),
                                ],
                                style={"flex": "1", "marginRight": "1rem"},
                            ),
                            html.Div(
                                [
                                    html.Label(
                                        "Question",
                                        style={
                                            "display": "block",
                                            "fontSize": "0.875rem",
                                            "fontWeight": "500",
                                            "color": COLORS['text'],
                                            "marginBottom": "0.5rem",
                                        }
                                    ),
                                    dcc.Dropdown(
                                        id="question-dropdown",
                                        clearable=False,
                                        style={
                                            "fontSize": "0.875rem",
                                        },
                                    ),
                                ],
                                style={"flex": "2"},
                            ),
                        ],
                        style={"display": "flex", "gap": "1rem", "marginBottom": "1.5rem"},
                    ),
                    html.Div(
                        [
                            html.Label(
                                "Age Group Granularity",
                                style={
                                    "display": "block",
                                    "fontSize": "0.875rem",
                                    "fontWeight": "500",
                                    "color": COLORS['text'],
                                    "marginBottom": "0.5rem",
                                }
                            ),
                            dcc.RadioItems(
                                id="age-mode-radio",
                                options=[
                                    {"label": " More Detail (7 groups)", "value": "more"},
                                    {"label": " Less Detail (3 groups)", "value": "less"},
                                ],
                                value="more",
                                inline=True,
                                style={
                                    "fontSize": "0.875rem",
                                },
                                inputStyle={"marginRight": "0.5rem", "marginLeft": "0"},
                                labelStyle={"marginRight": "1.5rem"},
                            ),
                        ],
                    ),
                ],
                style={"padding": "1.5rem"},
            ),
            html.Div(
                id="question-info",
                style={
                    "padding": "1rem 1.5rem",
                    "backgroundColor": COLORS['light'],
                    "borderTop": f"1px solid {COLORS['border']}",
                    "borderRadius": "0 0 8px 8px",
                }
            ),
        ],
        style={
            "backgroundColor": "white",
            "borderRadius": "12px",
            "boxShadow": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
            "marginBottom": "2rem",
            "border": f"1px solid {COLORS['border']}",
        }
    )

def create_chart_card(title, graph_id, icon="📊"):
    """Create a card container for a chart"""
    return html.Div(
        [
            html.Div(
                [
                    html.Span(icon, style={"fontSize": "1.5rem", "marginRight": "0.75rem"}),
                    html.H3(
                        title,
                        style={
                            "fontSize": "1.25rem",
                            "fontWeight": "600",
                            "color": COLORS['dark'],
                            "margin": "0",
                        }
                    ),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "padding": "1.25rem 1.5rem",
                    "borderBottom": f"1px solid {COLORS['border']}",
                }
            ),
            html.Div(
                [
                    dcc.Graph(id=graph_id, config={"displayModeBar": True, "displaylogo": False}),
                ],
                style={"padding": "1rem"},
            ),
        ],
        style={
            "backgroundColor": "white",
            "borderRadius": "12px",
            "boxShadow": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
            "marginBottom": "2rem",
            "border": f"1px solid {COLORS['border']}",
        }
    )

# =========================
# 11. Main layout
# =========================
app.layout = html.Div(
    [
        create_header(),
        html.Div(
            [
                html.Div(
                    [
                        create_filter_card(),
                    ],
                    style={"maxWidth": "1400px", "margin": "0 auto", "padding": "0 2rem"},
                ),
                html.Div(
                    [
                        create_chart_card("Overall Analysis", "overall-graph", "📈"),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        create_chart_card("Gender Analysis", "gender-graph", "👥"),
                                    ],
                                    style={"flex": "1"},
                                ),
                                html.Div(
                                    [
                                        create_chart_card("Age Analysis", "age-graph", "🎂"),
                                    ],
                                    style={"flex": "1"},
                                ),
                            ],
                            style={"display": "flex", "gap": "2rem"},
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        create_chart_card("Education Analysis", "education-graph", "🎓"),
                                    ],
                                    style={"flex": "1"},
                                ),
                                html.Div(
                                    [
                                        create_chart_card("Income Analysis", "income-graph", "💰"),
                                    ],
                                    style={"flex": "1"},
                                ),
                            ],
                            style={"display": "flex", "gap": "2rem"},
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Span("🗺️", style={"fontSize": "1.5rem", "marginRight": "0.75rem"}),
                                                html.H3(
                                                    "Geographic Analysis",
                                                    style={
                                                        "fontSize": "1.25rem",
                                                        "fontWeight": "600",
                                                        "color": COLORS['dark'],
                                                        "margin": "0",
                                                    }
                                                ),
                                            ],
                                            style={
                                                "display": "flex",
                                                "alignItems": "center",
                                                "padding": "1.25rem 1.5rem",
                                                "borderBottom": f"1px solid {COLORS['border']}",
                                            }
                                        ),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.Label(
                                                            "Select Response to Display:",
                                                            style={
                                                                "display": "block",
                                                                "fontSize": "0.875rem",
                                                                "fontWeight": "500",
                                                                "color": COLORS['text'],
                                                                "marginBottom": "0.5rem",
                                                            }
                                                        ),
                                                        dcc.Dropdown(
                                                            id="map-response-dropdown",
                                                            clearable=False,
                                                            style={
                                                                "fontSize": "0.875rem",
                                                            },
                                                        ),
                                                    ],
                                                    style={"padding": "1rem 1.5rem", "borderBottom": f"1px solid {COLORS['border']}"},
                                                ),
                                                html.Div(
                                                    [
                                                        dcc.Graph(id="location-graph", config={"displayModeBar": True, "displaylogo": False}),
                                                    ],
                                                    style={"padding": "1rem"},
                                                ),
                                                html.Div(
                                                    id="map-stats-panel",
                                                    style={
                                                        "padding": "1rem 1.5rem",
                                                        "backgroundColor": COLORS['light'],
                                                        "borderTop": f"1px solid {COLORS['border']}",
                                                        "borderRadius": "0 0 12px 12px",
                                                    }
                                                ),
                                            ]
                                        ),
                                    ],
                                    style={
                                        "backgroundColor": "white",
                                        "borderRadius": "12px",
                                        "boxShadow": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
                                        "marginBottom": "2rem",
                                        "border": f"1px solid {COLORS['border']}",
                                    }
                                ),
                            ],
                        ),
                        create_chart_card("Temporal Analysis", "year-graph", "📅"),
                    ],
                    style={"maxWidth": "1400px", "margin": "0 auto", "padding": "0 2rem"},
                ),
            ],
            style={"paddingBottom": "3rem"},
        ),
    ],
    style={"minHeight": "100vh", "backgroundColor": COLORS['light']},
)

# =========================
# 12. Callbacks
# =========================
@app.callback(
    Output("topic-dropdown", "options"),
    Output("topic-dropdown", "value"),
    Input("class-dropdown", "value"),
)
def update_topic_dropdown(selected_class):
    sub = df[df["Class"] == selected_class]
    topics = sorted(sub["Topic"].dropna().unique())
    options = [{"label": t, "value": t} for t in topics]
    value = topics[0] if topics else None
    return options, value

@app.callback(
    Output("question-dropdown", "options"),
    Output("question-dropdown", "value"),
    Input("class-dropdown", "value"),
    Input("topic-dropdown", "value"),
)
def update_question_dropdown(selected_class, selected_topic):
    sub = df[
        (df["Class"] == selected_class) &
        (df["Topic"] == selected_topic)
    ]
    questions = sorted(sub["Question"].dropna().unique())
    options = [{"label": q, "value": q} for q in questions]
    value = questions[0] if questions else None
    return options, value

@app.callback(
    Output("question-info", "children"),
    Input("question-dropdown", "value"),
)
def update_question_info(selected_question):
    if not selected_question:
        return html.P("Select a question to view details", style={"color": COLORS['text-light']})
    
    sub = df[df["Question"] == selected_question]
    if sub.empty:
        return html.P("No information available", style={"color": COLORS['text-light']})
    
    total_samples = int(sub["Sample_Size"].sum())
    num_responses = sub["Response"].nunique()
    num_years = sub["Year"].nunique()
    num_states = sub["Locationabbr"].nunique()
    year_range = f"{int(sub['Year'].min())}-{int(sub['Year'].max())}"
    
    return html.Div(
        [
            html.Div(
                [
                    html.Strong("Selected Question:", style={"color": COLORS['dark']}),
                    html.P(selected_question, style={"margin": "0.5rem 0 0 0", "color": COLORS['text']}),
                ],
                style={"marginBottom": "1rem"},
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Strong(f"{total_samples:,}", style={"fontSize": "1.25rem", "color": COLORS['primary']}),
                            html.Span("Total Samples", style={"fontSize": "0.75rem", "color": COLORS['text-light'], "display": "block"}),
                        ],
                        style={"textAlign": "center", "padding": "0.5rem"},
                    ),
                    html.Div(
                        [
                            html.Strong(str(num_responses), style={"fontSize": "1.25rem", "color": COLORS['secondary']}),
                            html.Span("Responses", style={"fontSize": "0.75rem", "color": COLORS['text-light'], "display": "block"}),
                        ],
                        style={"textAlign": "center", "padding": "0.5rem"},
                    ),
                    html.Div(
                        [
                            html.Strong(year_range, style={"fontSize": "1.25rem", "color": COLORS['success']}),
                            html.Span("Year Range", style={"fontSize": "0.75rem", "color": COLORS['text-light'], "display": "block"}),
                        ],
                        style={"textAlign": "center", "padding": "0.5rem"},
                    ),
                    html.Div(
                        [
                            html.Strong(str(num_states), style={"fontSize": "1.25rem", "color": COLORS['warning']}),
                            html.Span("States/Territories", style={"fontSize": "0.75rem", "color": COLORS['text-light'], "display": "block"}),
                        ],
                        style={"textAlign": "center", "padding": "0.5rem"},
                    ),
                ],
                style={
                    "display": "flex",
                    "justifyContent": "space-around",
                    "padding": "0.5rem",
                    "backgroundColor": "white",
                    "borderRadius": "8px",
                }
            ),
        ]
    )

@app.callback(
    Output("map-response-dropdown", "options"),
    Output("map-response-dropdown", "value"),
    Input("class-dropdown", "value"),
    Input("topic-dropdown", "value"),
    Input("question-dropdown", "value"),
)
def update_map_response_dropdown(sel_class, sel_topic, sel_question):
    """Update response dropdown options for map"""
    sub = df[
        (df["Class"] == sel_class) &
        (df["Topic"] == sel_topic) &
        (df["Question"] == sel_question) &
        (df["Break_Out_Category"] == BREAKOUT_OVERALL)
    ].copy()
    
    if sub.empty:
        return [], None
    
    responses = sorted(sub["Response"].dropna().unique())
    options = [{"label": r, "value": r} for r in responses]
    
    # Default to "Yes" if available, otherwise first response
    default_value = "Yes" if "Yes" in responses else (responses[0] if responses else None)
    
    return options, default_value

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
def update_all_panels(sel_class, sel_topic, sel_question, age_mode, map_response):
    sub = df[
        (df["Class"] == sel_class) &
        (df["Topic"] == sel_topic) &
        (df["Question"] == sel_question)
    ].copy()
    
    if sub.empty:
        empty_fig = make_bar_with_ci(pd.DataFrame(), "x", "No data")
        empty_stats = html.P("No data available", style={"color": COLORS['text-light']})
        return (empty_fig,) * 6 + (empty_stats,)
    
    fig_overall = make_overall_panel(sub)
    fig_gender = make_gender_panel(sub)
    fig_age = make_age_panel(sub, mode=age_mode)
    fig_edu = make_education_panel(sub)
    fig_income = make_income_panel(sub)
    fig_year = make_year_panel(sub)
    
    # Enhanced map with response selector
    fig_loc, responses, stats = make_location_map(sub, selected_response=map_response)
    
    # Create statistics panel
    if stats:
        stats_panel = html.Div(
            [
                html.H4(
                    "Geographic Statistics",
                    style={
                        "fontSize": "1rem",
                        "fontWeight": "600",
                        "color": COLORS['dark'],
                        "marginBottom": "1rem",
                    }
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Strong(f"{stats['mean']:.1f}%", style={"fontSize": "1.1rem", "color": COLORS['primary']}),
                                html.Span("Mean", style={"fontSize": "0.75rem", "color": COLORS['text-light'], "display": "block", "marginTop": "0.25rem"}),
                            ],
                            style={"textAlign": "center", "padding": "0.75rem", "flex": "1"},
                        ),
                        html.Div(
                            [
                                html.Strong(f"{stats['median']:.1f}%", style={"fontSize": "1.1rem", "color": COLORS['secondary']}),
                                html.Span("Median", style={"fontSize": "0.75rem", "color": COLORS['text-light'], "display": "block", "marginTop": "0.25rem"}),
                            ],
                            style={"textAlign": "center", "padding": "0.75rem", "flex": "1", "borderLeft": f"1px solid {COLORS['border']}"},
                        ),
                        html.Div(
                            [
                                html.Strong(f"{stats['min_state']}", style={"fontSize": "1rem", "color": COLORS['success']}),
                                html.Span(f"Lowest ({stats['min_value']:.1f}%)", style={"fontSize": "0.75rem", "color": COLORS['text-light'], "display": "block", "marginTop": "0.25rem"}),
                            ],
                            style={"textAlign": "center", "padding": "0.75rem", "flex": "1", "borderLeft": f"1px solid {COLORS['border']}"},
                        ),
                        html.Div(
                            [
                                html.Strong(f"{stats['max_state']}", style={"fontSize": "1rem", "color": COLORS['warning']}),
                                html.Span(f"Highest ({stats['max_value']:.1f}%)", style={"fontSize": "0.75rem", "color": COLORS['text-light'], "display": "block", "marginTop": "0.25rem"}),
                            ],
                            style={"textAlign": "center", "padding": "0.75rem", "flex": "1", "borderLeft": f"1px solid {COLORS['border']}"},
                        ),
                        html.Div(
                            [
                                html.Strong(f"{stats['std']:.1f}%", style={"fontSize": "1rem", "color": COLORS['info']}),
                                html.Span("Std Dev", style={"fontSize": "0.75rem", "color": COLORS['text-light'], "display": "block", "marginTop": "0.25rem"}),
                            ],
                            style={"textAlign": "center", "padding": "0.75rem", "flex": "1", "borderLeft": f"1px solid {COLORS['border']}"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "space-around",
                        "padding": "0.5rem",
                        "backgroundColor": "white",
                        "borderRadius": "8px",
                    }
                ),
            ]
        )
    else:
        stats_panel = html.P("No statistics available", style={"color": COLORS['text-light']})
    
    return (
        fig_overall,
        fig_gender,
        fig_age,
        fig_edu,
        fig_income,
        fig_loc,
        fig_year,
        stats_panel,
    )

# =========================
# 13. Entry point
# =========================
if __name__ == "__main__":
    print("\n" + "="*80)
    print("BRFSS Dashboard - Starting Server".center(80))
    print("="*80)
    print(f"\n📊 Dataset: {len(df):,} records")
    print(f"📅 Year Range: {int(df['Year'].min())}-{int(df['Year'].max())}")
    print(f"📋 Questions: {df['Question'].nunique()}")
    print(f"✅ Quality Filter: Min Sample Size = {MIN_SAMPLE_SIZE}")
    print("\n" + "="*80)
    print("Server starting on http://127.0.0.1:8050")
    print("="*80 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=8050)
