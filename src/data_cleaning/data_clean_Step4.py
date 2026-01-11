import pandas as pd

# ===== 路径设置 =====
input_path = "cleaned_data_breakout_merged.csv"   # 上一步的结果（Step3 输出）
output_path = "cleaned_data_final.csv"            # 数值清洗后的最终版

print(f"📥 正在读取数据: {input_path}")
df = pd.read_csv(input_path)
print("原始数据维度：", df.shape)

# ===== 1. 数值列转换为 float =====
num_cols = [
    "Sample_Size",
    "Data_value",
    "Confidence_limit_Low",
    "Confidence_limit_High",
]

missing = [c for c in num_cols if c not in df.columns]
if missing:
    raise ValueError(f"数据集中缺少这些需要转为数值的列: {missing}")

# 使用 to_numeric，无法转换的变为 NaN
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print("✅ 已将数值列转换为 float")

# ===== 2. 过滤无效样本和无效 Data_value =====
before = df.shape[0]

# 2.1 只保留 Sample_Size > 0 的行（有实际样本）
mask_sample = df["Sample_Size"] > 0

# 2.2 只保留 0 <= Data_value <= 100 且非 NaN 的行（合法百分比）
mask_datavalue = df["Data_value"].between(0, 100)

valid_mask = mask_sample & mask_datavalue
df = df[valid_mask].copy()

after = df.shape[0]
dropped = before - after

print(f"✅ 已过滤无效样本 / 百分比行，共删除 {dropped} 行")
print("  过滤后数据维度：", df.shape)

# ===== 3. 生成 proportion 和 persons =====
# proportion = Data_value / 100  (0–1 概率)
df["proportion"] = df["Data_value"] / 100.0

# persons = Sample_Size * proportion  (估计人数)
df["persons"] = df["Sample_Size"] * df["proportion"]

print("✅ 已生成 proportion 和 persons 列")

# ===== 4. 导出结果 =====
df.to_csv(output_path, index=False)
print(f"💾 已保存数值清洗后的数据到: {output_path}")
print("🎉 Step4 数值清洗完成")
