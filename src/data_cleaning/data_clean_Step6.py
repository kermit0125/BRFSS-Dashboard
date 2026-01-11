# data_clean_Step6.py
# 作用：
#   在 Step1-5 清洗好的基础上，进行额外的数据质量检查和清理：
#   1. 文本字段的进一步标准化（Class, Topic, Question, Response, Break_Out）
#   2. 缺失值和空字符串处理
#   3. 数据一致性检查（置信区间合理性、数值范围）
#   4. 地理位置数据清理和标准化
#   5. 年份范围验证
#   6. Break_Out_Category 一致性检查
#   7. 异常值检测和处理
#   8. 最终数据完整性验证
#
#   输出：
#   - cleaned_data_final_enhanced.csv
#   - cleaned_data_final_enhanced.parquet
#   - data_quality_report.txt（数据质量报告）

import pandas as pd
import numpy as np
import re
from pathlib import Path

# ===== 1. 路径设置 =====
input_path_csv = "cleaned_data_final.csv"  # Step5 的结果
output_path_csv = "cleaned_data_final_enhanced.csv"
output_path_parquet = "cleaned_data_final_enhanced.parquet"
quality_report_path = "data_quality_report.txt"

print(f"📥 正在读取 Step5 输出数据: {input_path_csv}")
df = pd.read_csv(input_path_csv)
print("Step5 数据维度：", df.shape)

# ===== 2. 文本字段标准化函数 =====
def normalize_text(text):
    """标准化文本：去除多余空格、统一换行符、处理特殊字符"""
    if pd.isna(text) or text == "":
        return None
    text = str(text)
    # 去除首尾空格
    text = text.strip()
    # 将多个连续空格替换为单个空格
    text = re.sub(r'\s+', ' ', text)
    # 去除首尾标点符号（可选，根据需求）
    # text = re.sub(r'^[^\w]+|[^\w]+$', '', text)
    return text if text else None

def clean_class_topic_question(text):
    """清理 Class, Topic, Question 文本"""
    if pd.isna(text) or text == "":
        return None
    text = str(text).strip()
    # 统一处理常见的变体
    text = re.sub(r'\s+', ' ', text)
    # 去除末尾的句号（如果有）
    text = re.sub(r'\.+$', '', text)
    return text if text else None

# ===== 3. 文本字段标准化 =====
print("\n🔤 开始文本字段标准化...")

text_cols = ["Class", "Topic", "Question", "Response", "Break_Out", "Break_Out_Category"]
for col in text_cols:
    if col in df.columns:
        before_nulls = df[col].isna().sum()
        df[col] = df[col].apply(normalize_text)
        after_nulls = df[col].isna().sum()
        if after_nulls > before_nulls:
            print(f"  ⚠️ {col}: 空字符串转换为 NaN，新增 {after_nulls - before_nulls} 个")

# 特别处理 Class, Topic, Question
for col in ["Class", "Topic", "Question"]:
    if col in df.columns:
        df[col] = df[col].apply(clean_class_topic_question)

print("✅ 文本字段标准化完成")

# ===== 4. 缺失值处理 =====
print("\n🔍 检查缺失值...")
missing_report = []
for col in df.columns:
    missing_count = df[col].isna().sum()
    missing_pct = (missing_count / len(df)) * 100
    if missing_count > 0:
        missing_report.append(f"  {col}: {missing_count} ({missing_pct:.2f}%)")

if missing_report:
    print("发现缺失值:")
    for line in missing_report[:10]:  # 只显示前10个
        print(line)
    if len(missing_report) > 10:
        print(f"  ... 还有 {len(missing_report) - 10} 个字段有缺失值")

# 关键字段缺失值处理
critical_cols = ["Question", "Response", "Year", "Locationabbr"]
for col in critical_cols:
    if col in df.columns:
        before = len(df)
        df = df[df[col].notna()].copy()
        after = len(df)
        if before > after:
            print(f"  ⚠️ 删除 {col} 为空的 {before - after} 行")

print("✅ 缺失值处理完成")

# ===== 5. 数据一致性检查 =====
print("\n📊 进行数据一致性检查...")

# 5.1 置信区间合理性检查
if "Confidence_limit_Low" in df.columns and "Confidence_limit_High" in df.columns:
    # 检查 Low <= High
    invalid_ci = df["Confidence_limit_Low"] > df["Confidence_limit_High"]
    if invalid_ci.any():
        print(f"  ⚠️ 发现 {invalid_ci.sum()} 行置信区间不合理 (Low > High)")
        # 交换不合理的置信区间
        mask = invalid_ci
        df.loc[mask, ["Confidence_limit_Low", "Confidence_limit_High"]] = \
            df.loc[mask, ["Confidence_limit_High", "Confidence_limit_Low"]].values
    
    # 检查 Data_value 是否在置信区间内（允许一定误差）
    if "Data_value" in df.columns:
        outside_ci = (
            (df["Data_value"] < df["Confidence_limit_Low"] - 0.1) |
            (df["Data_value"] > df["Confidence_limit_High"] + 0.1)
        )
        if outside_ci.any():
            print(f"  ⚠️ 发现 {outside_ci.sum()} 行 Data_value 超出置信区间（允许±0.1%误差）")

# 5.2 数值范围检查
if "Data_value" in df.columns:
    invalid_range = ~df["Data_value"].between(0, 100)
    if invalid_range.any():
        print(f"  ⚠️ 发现 {invalid_range.sum()} 行 Data_value 超出 [0, 100] 范围")
        df = df[~invalid_range].copy()

if "Sample_Size" in df.columns:
    invalid_size = df["Sample_Size"] <= 0
    if invalid_size.any():
        print(f"  ⚠️ 发现 {invalid_size.sum()} 行 Sample_Size <= 0")
        df = df[~invalid_size].copy()

if "proportion" in df.columns:
    invalid_prop = ~df["proportion"].between(0, 1)
    if invalid_prop.any():
        print(f"  ⚠️ 发现 {invalid_prop.sum()} 行 proportion 超出 [0, 1] 范围")
        df = df[~invalid_prop].copy()

print("✅ 数据一致性检查完成")

# ===== 6. 地理位置数据清理 =====
print("\n🗺️ 清理地理位置数据...")

if "Locationabbr" in df.columns:
    # 去除空格和标准化
    df["Locationabbr"] = df["Locationabbr"].astype(str).str.strip().str.upper()
    # 处理常见的变体
    location_fixes = {
        "DC": "DC",  # District of Columbia
        "PR": "PR",  # Puerto Rico
        "GU": "GU",  # Guam
        "VI": "VI",  # U.S. Virgin Islands
    }
    # 检查是否有无效的州代码
    valid_states = set([
        'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
        'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
        'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
        'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
        'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
        'DC', 'PR', 'GU', 'VI', 'AS', 'MP'  # 包括领土
    ])
    
    invalid_locations = ~df["Locationabbr"].isin(valid_states)
    if invalid_locations.any():
        invalid_count = invalid_locations.sum()
        print(f"  ⚠️ 发现 {invalid_count} 行无效的 Locationabbr")
        print(f"  无效值示例: {df.loc[invalid_locations, 'Locationabbr'].unique()[:5].tolist()}")
        # 可以选择删除或保留（根据需求）
        # df = df[~invalid_locations].copy()

print("✅ 地理位置数据清理完成")

# ===== 7. 年份范围验证 =====
print("\n📅 验证年份范围...")

if "Year" in df.columns:
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    min_year = df["Year"].min()
    max_year = df["Year"].max()
    print(f"  年份范围: {min_year} - {max_year}")
    
    # BRFSS 数据通常从 1984 年开始，检查异常年份
    invalid_years = (df["Year"] < 1980) | (df["Year"] > 2030)
    if invalid_years.any():
        print(f"  ⚠️ 发现 {invalid_years.sum()} 行异常年份")
        df = df[~invalid_years].copy()

print("✅ 年份验证完成")

# ===== 8. Break_Out_Category 一致性检查 =====
print("\n📋 检查 Break_Out_Category 一致性...")

if "Break_Out_Category" in df.columns and "Break_Out" in df.columns:
    # 检查 Break_Out_Category 和 Break_Out 的对应关系
    category_mapping = {
        "Overall": ["Overall"],
        "Sex": ["Male", "Female"],
        "Age Group": ["18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+", 
                     "18-34", "35-64", "65+", "70-80"],
        "Education Attained": ["Less than H.S.", "H.S. or G.E.D.", 
                               "Some post-H.S.", "College graduate"],
        "Household Income": ["<$15k", "$15k-$24k", "$25k-$34k", "$35k-$49k", "$50k+"],
        "Race/Ethnicity": ["White", "Black", "Hispanic", "Multiracial", "Other"],
    }
    
    # 检查不一致的情况（这里只是报告，不强制修改）
    inconsistencies = []
    for category, valid_breaks in category_mapping.items():
        sub_df = df[df["Break_Out_Category"] == category]
        if len(sub_df) > 0:
            invalid_breaks = sub_df[~sub_df["Break_Out"].isin(valid_breaks + [None, ""])]
            if len(invalid_breaks) > 0:
                unique_invalid = invalid_breaks["Break_Out"].unique()
                inconsistencies.append(f"  {category}: {unique_invalid[:3].tolist()}")
    
    if inconsistencies:
        print("  ⚠️ 发现不一致的 Break_Out_Category 和 Break_Out 组合:")
        for line in inconsistencies[:5]:
            print(line)

print("✅ Break_Out_Category 检查完成")

# ===== 9. 异常值检测 =====
print("\n🔬 检测异常值...")

if "Data_value" in df.columns and "Sample_Size" in df.columns:
    # 检测极端小的样本量
    small_samples = df["Sample_Size"] < 30  # 通常认为样本量小于30不够可靠
    if small_samples.any():
        print(f"  ⚠️ 发现 {small_samples.sum()} 行样本量 < 30（可能不够可靠）")
    
    # 检测极端大的置信区间宽度（可能表示数据不稳定）
    if "Confidence_limit_Low" in df.columns and "Confidence_limit_High" in df.columns:
        ci_width = df["Confidence_limit_High"] - df["Confidence_limit_Low"]
        wide_ci = ci_width > 50  # 置信区间宽度超过50%
        if wide_ci.any():
            print(f"  ⚠️ 发现 {wide_ci.sum()} 行置信区间宽度 > 50%（数据可能不稳定）")

print("✅ 异常值检测完成")

# ===== 10. 最终数据完整性验证 =====
print("\n✅ 最终数据完整性验证...")

required_cols = [
    "Year", "Locationabbr", "Class", "Topic", "Question", "Response",
    "Break_Out", "Break_Out_Category",
    "Sample_Size", "Data_value",
    "Confidence_limit_Low", "Confidence_limit_High",
    "proportion", "persons",
]

missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    print(f"  ⚠️ 缺少必需列: {missing_cols}")
else:
    print("  ✅ 所有必需列都存在")

# 检查关键字段是否还有缺失值
critical_missing = {}
for col in ["Question", "Response", "Year", "Locationabbr"]:
    if col in df.columns:
        missing = df[col].isna().sum()
        if missing > 0:
            critical_missing[col] = missing

if critical_missing:
    print(f"  ⚠️ 关键字段仍有缺失值: {critical_missing}")
else:
    print("  ✅ 关键字段无缺失值")

print(f"\n最终数据维度: {df.shape}")
print(f"最终数据行数: {len(df):,}")

# ===== 11. 生成数据质量报告 =====
print("\n📝 生成数据质量报告...")

report_lines = [
    "=" * 60,
    "BRFSS 数据质量报告",
    "=" * 60,
    f"\n生成时间: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}",
    f"\n数据维度: {df.shape[0]:,} 行 × {df.shape[1]} 列",
    "\n" + "=" * 60,
    "\n1. 缺失值统计:",
]

for col in df.columns:
    missing = df[col].isna().sum()
    if missing > 0:
        pct = (missing / len(df)) * 100
        report_lines.append(f"   {col}: {missing:,} ({pct:.2f}%)")

report_lines.extend([
    "\n" + "=" * 60,
    "\n2. 数值字段统计:",
])

numeric_cols = df.select_dtypes(include=[np.number]).columns
for col in numeric_cols[:10]:  # 只显示前10个数值列
    report_lines.append(f"   {col}:")
    report_lines.append(f"     均值: {df[col].mean():.2f}")
    report_lines.append(f"     中位数: {df[col].median():.2f}")
    report_lines.append(f"     最小值: {df[col].min():.2f}")
    report_lines.append(f"     最大值: {df[col].max():.2f}")

report_lines.extend([
    "\n" + "=" * 60,
    "\n3. 分类字段唯一值数量:",
])

categorical_cols = ["Class", "Topic", "Question", "Response", "Break_Out_Category", "Locationabbr"]
for col in categorical_cols:
    if col in df.columns:
        unique_count = df[col].nunique()
        report_lines.append(f"   {col}: {unique_count} 个唯一值")

report_lines.extend([
    "\n" + "=" * 60,
    "\n4. 年份分布:",
])

if "Year" in df.columns:
    year_counts = df["Year"].value_counts().sort_index()
    report_lines.append(f"   年份范围: {df['Year'].min()} - {df['Year'].max()}")
    report_lines.append(f"   总年份数: {year_counts.shape[0]}")
    report_lines.append(f"   数据最多的年份: {year_counts.idxmax()} ({year_counts.max():,} 行)")

report_lines.extend([
    "\n" + "=" * 60,
    "\n报告结束",
    "=" * 60,
])

with open(quality_report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))

print(f"  💾 数据质量报告已保存到: {quality_report_path}")

# ===== 12. 导出最终数据 =====
print("\n💾 导出最终数据...")

df.to_csv(output_path_csv, index=False)
print(f"  ✅ CSV 已保存到: {output_path_csv}")

df.to_parquet(output_path_parquet, index=False)
print(f"  ✅ Parquet 已保存到: {output_path_parquet}")

print("\n🎉 Step6：数据质量增强和验证 完成！")
print(f"\n📊 最终统计:")
print(f"   - 数据行数: {len(df):,}")
print(f"   - 数据列数: {df.shape[1]}")
print(f"   - 唯一问题数: {df['Question'].nunique() if 'Question' in df.columns else 'N/A'}")
print(f"   - 年份范围: {df['Year'].min()}-{df['Year'].max() if 'Year' in df.columns else 'N/A'}")

