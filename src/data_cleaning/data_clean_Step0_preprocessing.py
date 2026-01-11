# data_clean_Step0_preprocessing.py
# 作用：
#   在 Step1 之前进行的预处理步骤，处理原始数据中的常见问题：
#   1. Class/Topic 文本的变体统一（大小写、缩写、拼写错误）
#   2. Response 文本的进一步标准化（处理更多变体）
#   3. Break_Out_Category 的标准化
#   4. GeoLocation 字段的处理
#   5. 处理特殊字符和编码问题
#
#   注意：这个步骤应该在 Step1 之前运行，或者可以合并到 Step1 中

import pandas as pd
import numpy as np
import re

# ===== 1. 路径设置 =====
input_path = "dataset.csv"  # 原始数据
output_path = "dataset_preprocessed.csv"  # 预处理后的数据

print(f"📥 正在读取原始数据: {input_path}")
df = pd.read_csv(input_path, low_memory=False)
print("原始数据维度：", df.shape)

# ===== 2. Class 文本标准化 =====
print("\n🔤 标准化 Class 文本...")

if "Class" in df.columns:
    # 常见的 Class 变体映射（根据实际数据调整）
    class_normalizations = {
        # 处理大小写变体
        "health status": "Health Status",
        "HEALTH STATUS": "Health Status",
        "Health status": "Health Status",
        
        # 处理缩写
        "Hlth Status": "Health Status",
        "Health Stat": "Health Status",
        
        # 可以根据实际数据添加更多映射
    }
    
    df["Class"] = df["Class"].astype(str).str.strip()
    df["Class"] = df["Class"].replace(class_normalizations)
    
    # 统一首字母大写
    df["Class"] = df["Class"].str.title()

print("✅ Class 文本标准化完成")

# ===== 3. Topic 文本标准化 =====
print("\n🔤 标准化 Topic 文本...")

if "Topic" in df.columns:
    # 常见的 Topic 变体映射
    topic_normalizations = {
        # 处理常见的拼写变体
        "General Health": "General Health",
        "general health": "General Health",
        "GENERAL HEALTH": "General Health",
        
        # 可以根据实际数据添加更多映射
    }
    
    df["Topic"] = df["Topic"].astype(str).str.strip()
    df["Topic"] = df["Topic"].replace(topic_normalizations)
    
    # 统一首字母大写
    df["Topic"] = df["Topic"].str.title()

print("✅ Topic 文本标准化完成")

# ===== 4. Question 文本的进一步清理 =====
print("\n🔤 清理 Question 文本...")

if "Question" in df.columns:
    # 去除多余的空格和换行符
    df["Question"] = df["Question"].astype(str).str.strip()
    df["Question"] = df["Question"].str.replace(r'\s+', ' ', regex=True)
    df["Question"] = df["Question"].str.replace(r'\n+', ' ', regex=True)
    df["Question"] = df["Question"].str.replace(r'\t+', ' ', regex=True)
    
    # 统一处理问号
    df["Question"] = df["Question"].str.replace(r'\?+', '?', regex=True)
    
    # 去除首尾的标点符号（保留问号）
    # df["Question"] = df["Question"].str.replace(r'^[^\w\?]+|[^\w\?]+$', '', regex=True)

print("✅ Question 文本清理完成")

# ===== 5. Response 文本的进一步标准化 =====
print("\n🔤 标准化 Response 文本...")

if "Response" in df.columns:
    # 处理常见的 Response 变体（补充 Step2 中的映射）
    response_normalizations = {
        # Yes/No 变体
        "yes": "Yes",
        "YES": "Yes",
        "Y": "Yes",
        "no": "No",
        "NO": "No",
        "N": "No",
        
        # 处理 "Don't know" 变体
        "Don't know": "Don't know",
        "Don't Know": "Don't know",
        "Dont know": "Don't know",
        "DON'T KNOW": "Don't know",
        "Unknown": "Don't know",
        "Not sure": "Don't know",
        
        # 处理 "Refused" 变体
        "Refused": "Refused",
        "REFUSED": "Refused",
        "Refuse": "Refused",
        
        # 处理空白和特殊值
        "": None,
        "nan": None,
        "None": None,
        "N/A": None,
        "n/a": None,
    }
    
    df["Response"] = df["Response"].astype(str).str.strip()
    df["Response"] = df["Response"].replace(response_normalizations)
    
    # 将 "nan" 字符串转换为真正的 NaN
    df["Response"] = df["Response"].replace(["nan", "None", ""], None)

print("✅ Response 文本标准化完成")

# ===== 6. Break_Out_Category 标准化 =====
print("\n🔤 标准化 Break_Out_Category...")

if "Break_Out_Category" in df.columns:
    # 常见的 Break_Out_Category 变体
    category_normalizations = {
        "Overall": "Overall",
        "overall": "Overall",
        "OVERALL": "Overall",
        
        "Sex": "Sex",
        "sex": "Sex",
        "SEX": "Sex",
        "Gender": "Sex",  # 统一使用 Sex
        
        "Age Group": "Age Group",
        "age group": "Age Group",
        "AGE GROUP": "Age Group",
        "Age": "Age Group",
        "Age Groups": "Age Group",
        
        "Education Attained": "Education Attained",
        "education attained": "Education Attained",
        "Education": "Education Attained",
        "Education Level": "Education Attained",
        
        "Household Income": "Household Income",
        "household income": "Household Income",
        "Income": "Household Income",
        "Income Level": "Household Income",
        
        "Race/Ethnicity": "Race/Ethnicity",
        "race/ethnicity": "Race/Ethnicity",
        "Race": "Race/Ethnicity",
        "Ethnicity": "Race/Ethnicity",
    }
    
    df["Break_Out_Category"] = df["Break_Out_Category"].astype(str).str.strip()
    df["Break_Out_Category"] = df["Break_Out_Category"].replace(category_normalizations)

print("✅ Break_Out_Category 标准化完成")

# ===== 7. GeoLocation 字段处理 =====
print("\n🗺️ 处理 GeoLocation 字段...")

if "GeoLocation" in df.columns:
    # 清理 GeoLocation 字段
    df["GeoLocation"] = df["GeoLocation"].astype(str).str.strip()
    # 将空字符串转换为 NaN
    df["GeoLocation"] = df["GeoLocation"].replace(["", "nan", "None"], None)

print("✅ GeoLocation 处理完成")

# ===== 8. 处理特殊字符和编码问题 =====
print("\n🔧 处理特殊字符和编码问题...")

# 处理常见的编码问题
text_cols = ["Class", "Topic", "Question", "Response", "Break_Out", "Break_Out_Category"]
for col in text_cols:
    if col in df.columns:
        # 替换常见的错误编码字符
        df[col] = df[col].astype(str).str.replace('â€™', "'", regex=False)  # 智能引号
        df[col] = df[col].astype(str).str.replace('â€œ', '"', regex=False)  # 左引号
        df[col] = df[col].astype(str).str.replace('â€', '"', regex=False)   # 右引号
        df[col] = df[col].astype(str).str.replace('â€"', '-', regex=False)  # em dash
        df[col] = df[col].astype(str).str.replace('â€"', '--', regex=False)  # en dash

print("✅ 特殊字符处理完成")

# ===== 9. 数值字段的初步清理 =====
print("\n🔢 清理数值字段...")

numeric_cols = ["Sample_Size", "Data_value", "Confidence_limit_Low", "Confidence_limit_High"]
for col in numeric_cols:
    if col in df.columns:
        # 将字符串类型的数值转换为数值类型
        df[col] = pd.to_numeric(df[col], errors="coerce")
        # 将负数转换为 NaN（如果不应有负数）
        if col in ["Sample_Size"]:
            df.loc[df[col] < 0, col] = np.nan

print("✅ 数值字段清理完成")

# ===== 10. 导出预处理后的数据 =====
print("\n💾 导出预处理后的数据...")
df.to_csv(output_path, index=False)
print(f"  ✅ 预处理后的数据已保存到: {output_path}")
print(f"  数据维度: {df.shape}")

print("\n🎉 Step0：数据预处理 完成！")
print("\n📝 下一步：运行 data_clean_Step1.py")

