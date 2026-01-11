import pandas as pd

# 1. 读取你的大数据集
df = pd.read_csv("dataset.csv")   # 修改为你的文件名

# 2. 要删除的列列表
cols_to_drop = [
    "Locationdesc",
    "Display_order",
    "Data_value_unit",
    "Data_value_type",
    "Data_Value_Footnote_Symbol",
    "Data_Value_Footnote",
    "DataSource",
    "LocationID"
]

# 3. 删除无用列
df = df.drop(columns=cols_to_drop, errors="ignore")  # ignore 确保缺失列不会报错

print("删除无用列后，数据维度：", df.shape)

# =============================
# 4. 合并“相同 Question 文本”的 QuestionID
#    规则：同一个 Question 文本，选“QuestionID 字符串长度最短”的作为统一 ID
# =============================

def pick_shortest_id(s: pd.Series):
    """
    在同一组 Question 下面的多个 QuestionID 中，
    选择一个“代表 ID”：长度最短，如果长度相同就按字典序最小。
    """
    s = s.dropna().astype(str).drop_duplicates()
    if s.empty:
        return None
    # 先按长度，再按字典序排序
    return sorted(s, key=lambda x: (len(x), x))[0]


# 4.1 建一个去掉首尾空格的 Question 文本（不改原始 Question，只用于分组）
df["Question_stripped"] = df["Question"].astype(str).str.strip()

# 4.2 对每个 Question_stripped 分组，挑一个统一的 QuestionID
qid_map = (
    df.groupby("Question_stripped")["QuestionID"]
      .agg(pick_shortest_id)
      .reset_index()
      .rename(columns={"QuestionID": "QuestionID_unified"})
)

print("唯一问题数量（按文本分组）：", qid_map.shape[0])

# 4.3 把统一的 QuestionID merge 回原数据
df = df.merge(qid_map, on="Question_stripped", how="left")

# 4.4 备份原始 QuestionID，方便以后检查
df["QuestionID_original"] = df["QuestionID"]

# 4.5 用统一后的 ID 覆盖 QuestionID
df["QuestionID"] = df["QuestionID_unified"]

# 4.6 清理临时列
df = df.drop(columns=["Question_stripped", "QuestionID_unified"])

print("合并相同 Question 后，数据维度：", df.shape)

# =============================
# 5. 导出结果
# =============================

# 5.1 主数据：删列 + 合并 QuestionID 后的版本
df.to_csv("cleaned_data_question_merged.csv", index=False)

# 5.2 Question → 统一 QuestionID 的映射表，方便你人工检查
question_map = (
    df[["Question", "QuestionID"]]
    .drop_duplicates()
    .sort_values("Question")
    .reset_index(drop=True)
)
question_map.to_csv("question_to_qid_unified.csv", index=False)

print("✅ 清洗完成：")
print("  - cleaned_data_question_merged.csv")
print("  - question_to_qid_unified.csv（供人工检查 Question ↔ QuestionID 合并情况）")
