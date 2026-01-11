# Step 1: QuestionID Merging
# Merges duplicate QuestionIDs for identical questions

import pandas as pd

def pick_shortest_id(s: pd.Series):
    """
    Select a representative ID from multiple QuestionIDs:
    Choose the shortest ID, or lexicographically smallest if same length.
    """
    s = s.dropna().astype(str).drop_duplicates()
    if s.empty:
        return None
    return sorted(s, key=lambda x: (len(x), x))[0]

def clean_step1(input_file="dataset.csv", output_file="cleaned_data_question_merged.csv"):
    """Execute Step 1: QuestionID merging"""
    print(f"📥 Step 1: Reading data from {input_file}")
    df = pd.read_csv(input_file)
    print(f"Original data shape: {df.shape}")
    
    # Drop unnecessary columns
    cols_to_drop = [
        "Locationdesc", "Display_order", "Data_value_unit", "Data_value_type",
        "Data_Value_Footnote_Symbol", "Data_Value_Footnote", "DataSource", "LocationID"
    ]
    df = df.drop(columns=cols_to_drop, errors="ignore")
    print(f"After dropping columns: {df.shape}")
    
    # Merge QuestionIDs
    df["Question_stripped"] = df["Question"].astype(str).str.strip()
    qid_map = (
        df.groupby("Question_stripped")["QuestionID"]
        .agg(pick_shortest_id)
        .reset_index()
        .rename(columns={"QuestionID": "QuestionID_unified"})
    )
    
    print(f"Unique questions (by text): {qid_map.shape[0]}")
    
    df = df.merge(qid_map, on="Question_stripped", how="left")
    df["QuestionID_original"] = df["QuestionID"]
    df["QuestionID"] = df["QuestionID_unified"]
    df = df.drop(columns=["Question_stripped", "QuestionID_unified"])
    
    print(f"After merging QuestionIDs: {df.shape}")
    
    # Export
    df.to_csv(output_file, index=False)
    print(f"✅ Step 1 complete: {output_file}")
    
    return df

if __name__ == "__main__":
    clean_step1()

