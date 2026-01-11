# data_clean_Step5.py
# 作用：
#   在 Step1–4 清洗好的基础上，把“合并了 QuestionID / ResponseID / BreakoutID 后
#   仍然存在的重复行”按问题+维度聚合成一行，
#   用样本量 + persons 重新计算 Data_value 和 95% 置信区间。
#
#   输出：
#   - cleaned_data_agg.csv
#   - cleaned_data_final.parquet（Dash 直接用这一份）

import pandas as pd
import numpy as np

# ===== 1. 路径设置 =====
input_path_csv = "cleaned_data_final.csv"          # Step4 的结果
output_path_csv = "cleaned_data_agg.csv"           # 聚合后的 CSV
output_path_parquet = "cleaned_data_final.parquet" # 聚合后的 parquet（给 Dash 用）

print(f"📥 正在读取 Step4 输出数据: {input_path_csv}")
df = pd.read_csv(input_path_csv)
print("Step4 数据维度：", df.shape)

# ===== 2. 确保关键数值列是 float，顺便做一层 sanity check =====
num_cols = ["Sample_Size", "Data_value", "proportion", "persons"]
for col in num_cols:
    if col not in df.columns:
        raise ValueError(f"数据集中缺少列: {col}")
    df[col] = pd.to_numeric(df[col], errors="coerce")

print("✅ 已确认 Sample_Size / Data_value / proportion / persons 为数值类型")

# 再保险：只保留
#  - Sample_Size > 0
#  - 0 <= proportion <= 1
# 这样可以防止以后 Step4 改动时出现脏行
before = df.shape[0]
df = df[(df["Sample_Size"] > 0) & df["proportion"].between(0, 1)].copy()
after = df.shape[0]
print(f"✅ Step5 额外过滤异常行 {before - after} 条，剩余 {after} 条用于聚合")

# ===== 3. 定义“唯一一行”的键 =====
# 这些列完全确定了一条 CDC 汇总行的语义：
#   - 问题层面：Class / Topic / Question / QuestionID / QuestionID_original
#   - 回答层面：Response / ResponseID
#   - 维度层面：Break_Out_Category / Break_Out / BreakoutID / BreakOutCategoryID
#   - 分组层面：Year / Locationabbr / GeoLocation
group_cols = [
    "Year",
    "Locationabbr",
    "Class",
    "Topic",
    "Question",
    "Response",
    "Break_Out_Category",
    "Break_Out",
    "ClassId",
    "TopicId",
    "QuestionID",
    "QuestionID_original",
    "ResponseID",
    "BreakoutID",
    "BreakOutCategoryID",
    "GeoLocation",
]

missing_group_cols = [c for c in group_cols if c not in df.columns]
if missing_group_cols:
    raise ValueError(f"数据集中缺少这些分组列（请检查前面步骤）: {missing_group_cols}")

# ===== 4. 对每个 (Year, State, Question, Response, Breakout...) 做人数聚合 =====
# 思路和老师 workflow 中的 aggregation strategy 一致：
#   - persons = Sample_Size * proportion 已在 Step4 计算好
#   - 对人数和样本数做 sum
#   - 用总人数 / 总样本数 得到新的比例，再用二项分布近似重算置信区间
agg = (
    df.groupby(group_cols, as_index=False)
      .agg(
          total_sample=("Sample_Size", "sum"),
          total_persons=("persons", "sum"),
      )
)

print("✅ 按 group_cols 聚合后数据维度：", agg.shape)

# ===== 5. 根据聚合后的样本量 + 人数，重算比例和 95% CI =====
# p_hat 是 0–1 的比例
agg["p_hat"] = agg["total_persons"] / agg["total_sample"]

# 样本量 <= 0 时设为 NaN，避免除零（理论上不会发生，因为前面已过滤）
agg.loc[agg["total_sample"] <= 0, "p_hat"] = np.nan

# 二项近似的标准误差
z = 1.96  # 约 95% CI
agg["se"] = np.sqrt(agg["p_hat"] * (1 - agg["p_hat"]) / agg["total_sample"])

# 重新计算 Data_value 和置信区间（单位：百分比 0–100）
agg["Data_value"] = agg["p_hat"] * 100.0
agg["Confidence_limit_Low"] = (agg["p_hat"] - z * agg["se"]) * 100.0
agg["Confidence_limit_High"] = (agg["p_hat"] + z * agg["se"]) * 100.0

# 把置信区间裁剪在 [0, 100] 之间，避免极端小样本导致轻微越界
agg["Confidence_limit_Low"] = agg["Confidence_limit_Low"].clip(lower=0, upper=100)
agg["Confidence_limit_High"] = agg["Confidence_limit_High"].clip(lower=0, upper=100)

# 把总样本数 / 总人数 / p_hat 重命名成和之前一致的列名
agg = agg.rename(
    columns={
        "total_sample": "Sample_Size",
        "total_persons": "persons",
        "p_hat": "proportion",
    }
)

# ===== 6. 按 Dash 代码用的列顺序整理 =====
final_cols = [
    "Year",
    "Locationabbr",
    "Class",
    "Topic",
    "Question",
    "Response",
    "Break_Out",
    "Break_Out_Category",
    "Sample_Size",
    "Data_value",
    "Confidence_limit_Low",
    "Confidence_limit_High",
    "ClassId",
    "TopicId",
    "BreakoutID",
    "BreakOutCategoryID",
    "QuestionID",
    "ResponseID",
    "GeoLocation",
    "QuestionID_original",
    "proportion",
    "persons",
]

missing_final_cols = [c for c in final_cols if c not in agg.columns]
if missing_final_cols:
    raise ValueError(f"聚合结果中缺少列: {missing_final_cols}")

agg = agg[final_cols]

print("✅ 最终列顺序整理完毕，维度：", agg.shape)
print(agg.head())

# ===== 7. 导出 CSV 和 parquet =====
agg.to_csv(output_path_csv, index=False)
print(f"💾 已保存聚合后的 CSV 到: {output_path_csv}")

agg.to_parquet(output_path_parquet, index=False)
print(f"💾 已保存聚合后的 parquet 到: {output_path_parquet}")

print("🎉 Step5：数据聚合 + 置信区间重算 完成。")
