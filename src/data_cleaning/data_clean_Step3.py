import pandas as pd
import os

# ========= 1. 路径设置 =========
input_path = "cleaned_data_response_merged.csv"          # 上一步结果（Question+Response 已清洗）
output_path = "cleaned_data_breakout_merged.csv"         # Breakout 清洗后的主数据
mapping_summary_path = "breakout_mapping_summary.csv"    # 审查用的映射表

print(f"📥 正在读取数据: {input_path}")
df = pd.read_csv(input_path)
print("原始数据维度：", df.shape)

# ========= 2. 你的 mapping 定义 =========

BREAKOUT_AGE_FINE = {
    # 18-24
    "AGE01": "18-24", "AGE20": "18-24", "AGE12": "18-24",

    # 25-34
    "AGE02": "25-34", "AGE21": "25-34", "AGE13": "25-34",

    # 35-44
    "AGE03": "35-44", "AGE22": "35-44", "AGE14": "35-44",

    # 45-54
    "AGE04": "45-54", "AGE23": "45-54", "AGE06": "45-54", "AGE15": "45-54",

    # 55-64
    "AGE05": "55-64", "AGE24": "55-64", "AGE07": "55-64", "AGE16": "55-64",

    # 65-74
    "AGE08": "65-74", "AGE25": "65-74", "AGE10": "65-74", "AGE17": "65-74",

    # 75+
    "AGE11": "75+", "AGE09": "75+", "AGE18": "75+", "AGE19": "75+", "AGE26": "70-80",
}

INCOME_MERGE_CANONICAL = {
    # Version A (7 buckets)
    "INCOME01": "<$15k",
    "INCOME02": "$15k-$24k",
    "INCOME03": "$25k-$34k",
    "INCOME04": "$35k-$49k",
    "INCOME05": "$50k+",
    "INCOME06": "$50k+",
    "INCOME07": "$50k+",

    # Version B (5 buckets)
    "INCOME1": "<$15k",
    "INCOME2": "$15k-$24k",
    "INCOME3": "$25k-$34k",
    "INCOME4": "$35k-$49k",
    "INCOME5": "$50k+",
}

BREAKOUT_CANONICAL = {
    # ------------------------------------
    # Overall
    # ------------------------------------
    "BO1": "Overall",

    # ------------------------------------
    # Education
    # ------------------------------------
    "EDUCA1": "Less than H.S.",
    "EDUCA2": "H.S. or G.E.D.",
    "EDUCA3": "Some post-H.S.",
    "EDUCA4": "College graduate",

    # ------------------------------------
    # Sex
    # ------------------------------------
    "SEX1": "Male",
    "SEX2": "Female",

    # ------------------------------------
    # Race – unified mapping
    # ------------------------------------
    # White
    "RACE01": "White",
    "RACE1":  "White",

    # Black
    "RACE02": "Black",
    "RACE2":  "Black",

    # Hispanic
    "RACE08": "Hispanic",
    "RACE3":  "Hispanic",

    # Multiracial
    "RACE07": "Multiracial",
    "RACE5":  "Multiracial",

    # Other (all other non-Hispanic categories)
    "RACE03": "Other",
    "RACE04": "Other",
    "RACE05": "Other",
    "RACE06": "Other",
    "RACE4":  "Other",
}

# ========= 3. 检查必需列 =========
for col in ["BreakoutID", "Break_Out"]:
    if col not in df.columns:
        raise ValueError(f"数据集中缺少列: {col}")

# ========= 4. 在 df 外备份原始 Breakout 列（只用于 summary，不写回主数据） =========
breakout_id_original = df["BreakoutID"].copy()
breakout_text_original = df["Break_Out"].copy()

# ========= 5. 构造一个「BreakoutID → 规范文本」的大字典 =========
# 注意：后面 update 的映射会覆盖前面的同名 key，但目前这些 key 不重叠
BREAKOUT_TEXT_MAP = {}
BREAKOUT_TEXT_MAP.update(BREAKOUT_CANONICAL)
BREAKOUT_TEXT_MAP.update(BREAKOUT_AGE_FINE)
BREAKOUT_TEXT_MAP.update(INCOME_MERGE_CANONICAL)

# 先清理一下原始文本的空白
df["Break_Out"] = df["Break_Out"].astype(str).str.strip()

# 用 BreakoutID 映射到规范文本
canonical_from_id = df["BreakoutID"].map(BREAKOUT_TEXT_MAP)

# 如果某个 BreakoutID 在 mapping 里有定义，就用规范文本；
# 否则就保留原始 Break_Out 文本
df["Break_Out"] = canonical_from_id.combine_first(df["Break_Out"])

print("✅ 已根据 AGE/INCOME/GENERAL 映射规范化 Break_Out 文本")
print("  例：AGExx → 18-24 等，INCOMExx → 五个收入档，RACExx/SEX/EDUCA/BO1 统一")

print("清洗后数据维度：", df.shape)

# ========= 6. 导出主数据（Question + Response + Breakout 都清洗后的版本） =========
df.to_csv(output_path, index=False)
print(f"💾 已保存 Breakout 清洗后的数据到: {output_path}")

# ========= 7. 生成一个 mapping summary，方便你检查变化 =========
breakout_mapping_summary = (
    pd.DataFrame({
        "BreakoutID": breakout_id_original,
        "Break_Out_original": breakout_text_original,
        "Break_Out": df["Break_Out"],
    })
    .drop_duplicates()
    .sort_values(["BreakoutID", "Break_Out"])
    .reset_index(drop=True)
)

try:
    breakout_mapping_summary.to_csv(mapping_summary_path, index=False)
    print(f"💾 已保存 Breakout 映射汇总表到: {mapping_summary_path}")
except PermissionError:
    alt_path = "breakout_mapping_summary_new.csv"
    breakout_mapping_summary.to_csv(alt_path, index=False)
    print("⚠️ 无法写入 breakout_mapping_summary.csv，可能被其他程序占用。")
    print(f"👉 已改为保存到: {alt_path}")

print("🎉 Breakout 清洗完成。")
