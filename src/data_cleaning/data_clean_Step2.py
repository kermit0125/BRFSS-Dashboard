import pandas as pd
import os

# ===== 1. 路径设置 =====
input_path = "cleaned_data_question_merged.csv"        # 上一步的结果（Question 已统一）
output_path = "cleaned_data_response_merged.csv"       # 合并 response 后的新数据
mapping_summary_path = "response_mapping_summary.csv"  # 用来审查改动的映射表

print(f"📥 正在读取数据: {input_path}")
df = pd.read_csv(input_path)
print("原始数据维度：", df.shape)

# ===== 2. ResponseID 合并字典 =====
RESPONSE_ID_MERGE = {
    # Employment corrections
    "RESP025": "RESP137",   # Emplyd  -> Employed
    "RESP026": "RESP172",   # Self emplyd -> Self-employed
    "RESP029": "RESP141",   # Homemkr -> Homemaker

    # Income high brackets collapse
    "RESP230": "RESP020",   # $100,000-199,999  -> $50,000+
    "RESP231": "RESP020",   # $200,000+         -> $50,000+
    "RESP232": "RESP020",   # $50,000-99,999    -> $50,000+

    # Race/Ethnicity old → new
    "RESP196": "RESP199",   # Asian/Pacific/Other   → consolidated
    "RESP197": "RESP199",
    "RESP198": "RESP199",

    "RESP200": "RESP008",   # Multiracial consolidation

    # Race categories unify
    "RESP194": "RESP005",   # White
    "RESP195": "RESP006",   # Black
}

# 文本人工覆盖
RESPONSE_TEXT_OVERRIDE = {
    "White, non-Hispanic": "White",
    "Black, non-Hispanic": "Black",
    "Asian, non-Hispanic": "Asian",
    "Multiracial, non-Hispanic": "Multiracial",
}

# ===== 3. 检查必需列 =====
for col in ["Response", "ResponseID"]:
    if col not in df.columns:
        raise ValueError(f"数据集中缺少列: {col}")

# ===== 🌟 4. 在 df 外面备份“原始列”（不写回 df） =====
response_id_original = df["ResponseID"].copy()
response_original = df["Response"].copy()

# ===== 5. 应用 ResponseID 映射 =====
df["ResponseID"] = df["ResponseID"].replace(RESPONSE_ID_MERGE)
print("✅ 已根据 RESPONSE_ID_MERGE 更新 ResponseID")

# ===== 6. 为每个 ResponseID 统一 Response 文本 =====
tmp = (
    df[["ResponseID", "Response"]]
    .dropna(subset=["ResponseID", "Response"])
)

def most_frequent(series: pd.Series):
    vc = series.value_counts()
    return vc.index[0]

canonical_response = (
    tmp.groupby("ResponseID", as_index=False)["Response"]
       .agg(most_frequent)
       .rename(columns={"Response": "Response_canonical"})
)

print("✅ 已为每个 ResponseID 计算 canonical Response 文本")
print("  唯一 ResponseID 数量：", canonical_response.shape[0])

df = df.merge(canonical_response, on="ResponseID", how="left")

# 如果 canonical 存在，就用它替换；否则保持原样
df["Response"] = df["Response_canonical"].combine_first(df["Response"])

# 人工覆盖 White/Black non-Hispanic
df["Response"] = df["Response"].replace(RESPONSE_TEXT_OVERRIDE)

# 清理临时列
df = df.drop(columns=["Response_canonical"])

print("✅ 已统一 Response 文本（含 White/Black 特殊处理）")
print("  合并完成后数据维度：", df.shape)

# ===== 7. 导出主数据（❗不包含 original 两列） =====
df.to_csv(output_path, index=False)
print(f"💾 已保存合并 Response 后的数据到: {output_path}")

# ===== 8. 用“外部备份的原始列”生成映射表，但不改 df 结构 =====
response_mapping_summary = (
    pd.DataFrame({
        "ResponseID_original": response_id_original,
        "Response_original": response_original,
        "ResponseID": df["ResponseID"],
        "Response": df["Response"],
    })
    .drop_duplicates()
    .sort_values(["ResponseID_original", "ResponseID"])
    .reset_index(drop=True)
)

try:
    response_mapping_summary.to_csv(mapping_summary_path, index=False)
    print(f"💾 已保存 Response 映射汇总表到: {mapping_summary_path}")
except PermissionError:
    alt_path = "response_mapping_summary_new.csv"
    response_mapping_summary.to_csv(alt_path, index=False)
    print("⚠️ 无法写入 response_mapping_summary.csv，可能被其他程序占用。")
    print(f"👉 已改为保存到: {alt_path}")

print("🎉 ResponseID & Response 清洗完成。")
